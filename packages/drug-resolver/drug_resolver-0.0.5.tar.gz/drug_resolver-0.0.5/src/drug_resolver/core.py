import json
import re
import urllib.parse
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Tuple, Optional

import requests
import xmltodict
from drug_resolver import requests_wrapper
from drug_resolver.utils import find_nodes
from rdkit import Chem


class FDAApprovalStatus(str, Enum):
    APPROVED = "APPROVED"
    INVESTIGATIONAL = "INVESTIGATIONAL"
    NOT_APPROVED = "NOT_APPROVED"


@dataclass
class PUGLookupResponse:
    cid: Optional[str]
    sid: Optional[str]
    canonical_smiles: Optional[str]
    canonical_name: Optional[str] = None
    drug_class: Optional[list] = None

@cache
def is_valid_smiles_string(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return mol is not None


@cache
def canonicalize_smiles_string(smiles: str):
    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return smiles

    return Chem.MolToSmiles(mol)


def molecules_are_identical(smiles1: Optional[str], smiles2: Optional[str]) -> bool:
    """Tests if two Drugs have SMILES strings for identical molecules.

    In general one molecule has many distinct SMI strings.

    Uses RDKit to normalize.
    """
    if not smiles1 or not smiles2:
        return False

    if smiles1 == smiles2:
        return True

    if not is_valid_smiles_string(smiles1) or not is_valid_smiles_string(
            smiles2
    ):
        return False

    canonical_smi1 = canonicalize_smiles_string(smiles1)
    canonical_smi2 = canonicalize_smiles_string(smiles2)
    return canonical_smi1 == canonical_smi2


@dataclass
class ResolvedDrug:
    # "Canonical" name of the drug
    name: str
    # PubChem Compound ID for the drug
    pubchem_compound_id: Optional[str] = None
    # PubChem Substance ID for the drug
    pubchem_substance_id: Optional[str] = None
    # Smiles string for the drug (usually only available for compounds)
    smiles: Optional[str] = None
    # List of Pharmacological Classes associated with the drug
    drug_classes: Optional[list] = None
    # FDA Approval status of the drug
    fda_approval: Optional[FDAApprovalStatus] = None
    # PubChem parent compound, if applicable
    # A parent compound is conceptually the "important" part of the molecule when
    # the molecule has more than one covalent component.
    # Specifically, a parent component must have at least one carbon and contain at
    # least 70% of the heavy (non-hydrogen) atoms of all the unique covalent units
    # (ignoring stoichiometry). Note that this is a very empirical definition and
    # is subject to change. For example, the "parent" compound in tetracycline
    # hydrochloride (CID 54704426) and tetracycline metaphosphate (CID 54729668) is
    # tetracycline (CID 54675776).
    pubchem_parent_compound_id: Optional[str] = None

    def __eq__(self, other):
        if not isinstance(other, ResolvedDrug):
            return False

        return (
            self.pubchem_substance_id == other.pubchem_substance_id
            or self.pubchem_compound_id == other.pubchem_compound_id
            or molecules_are_identical(self.smiles, other.smiles)
            or self.pubchem_parent_compound_id == other.pubchem_parent_compound_id
            or self.pubchem_compound_id == other.pubchem_parent_compound_id
            or self.pubchem_parent_compound_id == other.pubchem_compound_id
        )


def replace_non_ascii_characters_with_space(keyword):
    # normalize weird hyphens that aren't an ascii hyphen so we don't lose them
    keyword = re.sub(r"[‐᠆﹣－⁃−]+", "-", keyword)

    return re.sub(r"[^\x00-\x7f]", " ", keyword).strip()


def replace_meaningless_ascii_characters_with_space(keyword):
    return re.sub(r"[^A-Za-z\d()\-+]", " ", keyword).strip()


def pug_rest_fuzzy_name_lookup(keyword) -> PUGLookupResponse:
    cleaned_keyword = replace_meaningless_ascii_characters_with_space(
        replace_non_ascii_characters_with_space(keyword)
    )

    cleaned_keyword_parts = re.split("\s+", cleaned_keyword)

    query = {
        "select": "*",
        "collection": "compound",
        "where": {"ands": [{"*": x} for x in cleaned_keyword_parts]},
        "order": ["relevancescore,desc"],
        "start": 1,
        "limit": 1,
        "width": 1000000,
        "listids": 0,
    }

    url = "https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi"

    res = requests_wrapper.get_cached_session().get(
        url, params={"query": json.dumps(query), "infmt": "json", "outfmt": "json"}
    )

    if res.ok:
        try:
            top_search_results = res.json()["SDQOutputSet"][0]["rows"]
        except KeyError:
            top_search_results = None
    else:
        top_search_results = None

    if not top_search_results:
        query["collection"] = "substance"

        res = requests_wrapper.get_cached_session().get(
            url, params={"query": json.dumps(query), "infmt": "json", "outfmt": "json"}
        )

        if res.ok:
            try:
                top_search_results = res.json()["SDQOutputSet"][0]["rows"]
            except KeyError:
                pass

        if not top_search_results:
            return PUGLookupResponse(cid=None, sid=None, canonical_smiles=None)

    top_search_result = top_search_results[0]

    if "cid" in top_search_result:
        cid = top_search_result["cid"]

    else:
        cid = None

    if "sid" in top_search_result:
        sid = top_search_result["sid"]

    else:
        sid = None

    canonical_name = None
    if cid:
        res = requests_wrapper.get_cached_session().get(
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/substance/{sid}/JSON/")

        if res.ok:
            canonical_name = res.json()["Record"]["RecordTitle"]
    elif sid:
        res = requests_wrapper.get_cached_session().get(
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/")

        if res.ok:
            canonical_name = res.json()["Record"]["RecordTitle"]

    if "isosmiles" in top_search_result:
        canonical_smiles = top_search_result["isosmiles"]
    else:
        canonical_smiles = None

    return PUGLookupResponse(cid=cid, sid=sid, canonical_smiles=canonical_smiles, canonical_name=canonical_name)


def get_parent_compound_cid(cid):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{str(int(float(cid)))}/JSON/"
    res = requests_wrapper.get_cached_session().get(url)
    if not res.ok:
        return None
    record = res.json()
    try:
        parent_compound_text = next(
            find_nodes(record, "TOCHeading", "Parent Compound")
        )["Information"][0]["Value"]["StringWithMarkup"][0]["String"]
    except StopIteration:
        return None

    return parent_compound_text.split(" ")[1]


def pug_rest_name_lookup(keyword) -> PUGLookupResponse:
    """
    Keyword search a drug name in the PubChem Compound and Substance databases
    """

    quoted_keyword = urllib.parse.quote(
        replace_non_ascii_characters_with_space(keyword), safe="~()*!.'"
    )

    compound_url = (
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        f"{quoted_keyword}/property/CanonicalSMILES,InChI/JSON"
    )

    substance_url = (
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/"
        f"{quoted_keyword}/JSON"
    )

    compound_response = requests_wrapper.get_cached_session().get(compound_url)

    try:
        substance_response = requests_wrapper.get_cached_session().get(substance_url)
    except requests.exceptions.RetryError:
        substance_response = requests.Response()
        substance_response.status_code = 500

    sid = None
    cid = None
    smiles = None
    canonical_name = None

    if substance_response.ok:
        try:
            sid = str(substance_response.json()["PC_Substances"][0]["sid"]["id"])
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/substance/{sid}/JSON/"
            res = requests_wrapper.get_cached_session().get(url)

            if res.ok:
                canonical_name = res.json()["Record"]["RecordTitle"]
        except KeyError:
            pass

    if compound_response.ok:
        try:
            cid = str(compound_response.json()["PropertyTable"]["Properties"][0]["CID"])
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/"
            res = requests_wrapper.get_cached_session().get(url)

            if res.ok:
                canonical_name = res.json()["Record"]["RecordTitle"]
        except KeyError:
            pass

        try:
            smiles = compound_response.json()["PropertyTable"]["Properties"][0][
                "CanonicalSMILES"
            ]
        except KeyError:
            pass

    return PUGLookupResponse(cid=cid, sid=sid, canonical_smiles=smiles, canonical_name=canonical_name)


def drug_class_lookup(cid):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/"
    res = requests_wrapper.get_cached_session().get(url)
    try:
        info = res.json()
        drug_split = next(find_nodes(info, "Name", "Pharmacological Classes"))["Value"][
            "StringWithMarkup"
        ][0]["String"]
        drug_class = drug_split.split(";")
        return frozenset(drug_class)
    except StopIteration:
        return None


def drug_pubchem_name_lookup(drug) -> Optional[str]:
    if drug.pubchem_compound_id:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{drug.pubchem_compound_id}/JSON/"
        res = requests_wrapper.get_cached_session().get(url)

        if res.ok:
            return res.json()["Record"]["RecordTitle"]

    if drug.pubchem_substance_id:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/substance/{drug.pubchem_substance_id}/JSON/"
        res = requests_wrapper.get_cached_session().get(url)

        if res.ok:
            return res.json()["Record"]["RecordTitle"]


def maybe_get_drug_info_from_sid(
        sid: str,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/substance/{sid}/JSON/"
    res = requests_wrapper.get_cached_session().get(url)

    try:
        cid = next(find_nodes(res.json()["Record"], "Name", "PubChem CID"))["Value"][
            "StringWithMarkup"
        ][0]["Markup"][0]["URL"].split("/")[-1]
    except StopIteration:
        return None, None, None

    drug_class = drug_class_lookup(cid)

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/"
    cid_res = requests_wrapper.get_cached_session().get(url)

    try:
        smiles = next(
            find_nodes(cid_res.json()["Record"], "TOCHeading", "Canonical SMILES")
        )["Information"][0]["Value"]["StringWithMarkup"][0]["String"]
    except StopIteration:
        return cid, drug_class, None

    return cid, drug_class, canonicalize_smiles_string(smiles)


def maybe_get_fda_approval_from_cid(id_string: str):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{id_string}/JSON/"
    cid_res = requests_wrapper.get_cached_session().get(url)

    if cid_res.ok:
        fda_records = list(
            find_nodes(cid_res.json()["Record"], "SourceName", "Drugs@FDA")
        )

        clinical_trial_records = list(
            find_nodes(cid_res.json()["Record"], "SourceName", "ClinicalTrials.gov")
        )

        if len(fda_records) > 0:
            return FDAApprovalStatus.APPROVED
        else:
            if len(clinical_trial_records) > 0:
                return FDAApprovalStatus.INVESTIGATIONAL
            else:
                return FDAApprovalStatus.NOT_APPROVED

    return None


def maybe_get_synonyms_from_sid(
        sid: str,
) -> list[str]:
    """Get synonyms from PubChem PUG REST API Substance Record using PubChem Substance ID

    Parameters
    ----------
    sid : str
        PubChem Substance ID

    Returns
    -------
    list[str]
        List of synonyms
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/substance/{sid}/JSON/"
    res = requests.get(url)

    try:
        syns = next(
            find_nodes(
                res.json()["Record"], "TOCHeading", "Depositor-Supplied Synonyms"
            )
        )["Information"][0]["Value"]["StringWithMarkup"]
        synonyms = [str(syn["String"]) for syn in syns]
        return synonyms
    except StopIteration:
        print("StopIteration")
        synonyms = list()

    return synonyms


def lookup_pubchem_sid_from_nsc_id(nsc_id):
    url = f"https://dtp.cancer.gov/dtpstandard/servlet/ChemData?queryHOLD=&searchtype=NSC&chemnameboolean=or&outputformat=xml&searchlist={nsc_id}&Submit=Submit"
    res = requests_wrapper.get_cached_session().get(url)

    xml_dict = xmltodict.parse(res.content)

    try:
        return next(find_nodes(xml_dict, "@title", "PubChemSID"))["#text"]
    except (KeyError, StopIteration) as e:
        return None


@cache
def resolve_drug(
        drug_description: str
) -> ResolvedDrug:
    """
    Resolve a string to a drug.

    :param drug_description: A string representing a drug name
    :return: ResolvedDrug
    """
    result: PUGLookupResponse = pug_rest_name_lookup(drug_description)

    if result.cid is None and result.sid is None:
        result: PUGLookupResponse = pug_rest_fuzzy_name_lookup(drug_description)

    return ResolvedDrug(
        smiles=(
            canonicalize_smiles_string(result.canonical_smiles)
            if result.canonical_smiles is not None
            else None
        ),
        pubchem_compound_id=result.cid,
        pubchem_substance_id=result.sid,
        drug_classes=drug_class_lookup(result.cid) if result.cid is not None else None,
        fda_approval=(
            maybe_get_fda_approval_from_cid(result.cid)
            if result.cid is not None
            else None
        ),
        name=result.canonical_name if result.canonical_name is not None else drug_description,
        pubchem_parent_compound_id=get_parent_compound_cid(result.cid) if result.cid is not None else None
    )



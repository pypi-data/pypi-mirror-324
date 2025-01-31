from unittest import mock

from drug_resolver import core


def test_pug_rest_name_lookup_only_compound_succeeds():
    mock_request_session = mock.MagicMock()

    with mock.patch(
        "drug_resolver.requests_wrapper.get_cached_session"
    ) as get_cached_session:
        get_cached_session.return_value = mock_request_session
        response_mock = mock.MagicMock()

        mock_request_session.get.return_value = response_mock

        response_mock.json.return_value = {
            "PropertyTable": {
                "Properties": [{"CID": "1", "CanonicalSMILES": "2", "InChI": "3"}]
            }
        }

        result = core.pug_rest_name_lookup("test")

        assert result == core.PUGLookupResponse(
            cid="1", canonical_smiles="2", sid=None
        )


def test_pug_rest_name_lookup_only_substance_succeeds():
    mock_request_session = mock.MagicMock()

    with mock.patch(
        "drug_resolver.requests_wrapper.get_cached_session"
    ) as get_cached_session:
        get_cached_session.return_value = mock_request_session
        response_mock = mock.MagicMock()

        mock_request_session.get.return_value = response_mock

        response_mock.json.return_value = {"PC_Substances": [{"sid": {"id": 1}}]}

        result = core.pug_rest_name_lookup("test")

        assert result == core.PUGLookupResponse(
            cid=None, canonical_smiles=None, sid="1"
        )


def test_different_molecules_are_not_called_identical():
    pyradine = core.ResolvedDrug(name="a", smiles="c1ccncc1")
    pyramidine = core.ResolvedDrug(name="b", smiles="n1cnccc1")
    assert not core.molecules_are_identical(pyradine.smiles, pyramidine.smiles)


def test_exact_same_smi_called_identical():
    pemetrexed = core.ResolvedDrug(
        name="1",
        smiles="Nc3nc2[nH]cc(CCc1ccc(C(=O)N[C@@H](CCC(=O)O)C(=O)O)cc1)c2c(=O)[nH]3"
    )
    pemetrexed2 = core.ResolvedDrug(
        name="2",
        smiles="Nc3nc2[nH]cc(CCc1ccc(C(=O)N[C@@H](CCC(=O)O)C(=O)O)cc1)c2c(=O)[nH]3",
    )
    assert core.molecules_are_identical(pemetrexed.smiles, pemetrexed2.smiles)


def test_same_mol_different_smi_is_called_identical():
    pyramidine0 = "n1cnccc1"
    pyramidine1 = "n2cnccc2"
    pyramidine2 = "c1ccncn1"
    pyramidine3 = "c1cncnc1"
    pyramidine4 = "c1ncncc1"
    pyramidine5 = "c1ncccn1"
    assert core.molecules_are_identical(pyramidine0, pyramidine1)
    assert core.molecules_are_identical(pyramidine0, pyramidine2)
    assert core.molecules_are_identical(pyramidine0, pyramidine3)
    assert core.molecules_are_identical(pyramidine0, pyramidine4)
    assert core.molecules_are_identical(pyramidine0, pyramidine5)


def test_missing_drug_info_is_not_identical():
    pyramidine = "c1ncccn1"
    unknown = None
    assert not core.molecules_are_identical(unknown, unknown)
    assert not core.molecules_are_identical(unknown, pyramidine)


def test_bad_smiles_are_not_identical():
    a = "c"
    b = "cc"
    assert not core.molecules_are_identical(a, b)


def test_drug_class_lookup_success():
    drug = core.PUGLookupResponse(cid="1", canonical_smiles="2", sid=None)
    cid = drug.cid

    mock_request_session = mock.MagicMock()

    with mock.patch(
        "drug_resolver.requests_wrapper.get_cached_session"
    ) as get_cached_session:
        get_cached_session.return_value = mock_request_session
        response_mock = mock.MagicMock()

        mock_request_session.get.return_value = response_mock

        response_mock.json.return_value = {
            "Description": 'Pharmacologic Class is a group of active moieties that share scientifically documented properties and is defined on the basis of any combination of three attributes of the active moiety: mechanism of action (MOA), physiologic effect (PE) and chemical structure (CS).  An FDA "Established Pharmacologic Class" (EPC) text phrase is a pharmacologic class associated with an approved indication of an active moiety that the FDA has determined to be scientifically valid and clinically meaningful.',
            "URL": "https://www.fda.gov/industry/structured-product-labeling-resources/pharmacologic-class",
            "DisplayControls": {
                "CreateTable": {
                    "FromInformationIn": "ThisSection",
                    "NumberOfColumns": 2,
                    "ColumnContents": ["Name", "Value"],
                }
            },
            "Information": [
                {
                    "ReferenceNumber": 22,
                    "Name": "Non-Proprietary Name",
                    "Value": {"StringWithMarkup": [{"String": "CISPLATIN"}]},
                },
                {
                    "ReferenceNumber": 22,
                    "Name": "Pharmacological Classes",
                    "Value": {
                        "StringWithMarkup": [
                            {
                                "String": "Platinum-containing Compounds [EXT]; Platinum-based Drug [EPC]",
                                "Markup": [
                                    {
                                        "Start": 0,
                                        "Length": 8,
                                        "URL": "https://pubchem.ncbi.nlm.nih.gov/element/Platinum",
                                        "Type": "PubChem Internal Link",
                                        "Extra": "Element-Platinum",
                                    },
                                    {
                                        "Start": 37,
                                        "Length": 8,
                                        "URL": "https://pubchem.ncbi.nlm.nih.gov/element/Platinum",
                                        "Type": "PubChem Internal Link",
                                        "Extra": "Element-Platinum",
                                    },
                                ],
                            }
                        ]
                    },
                },
            ],
        }

        result = core.drug_class_lookup(cid)
        assert result == frozenset(
            [
                "Platinum-containing Compounds [EXT]",
                " Platinum-based Drug [EPC]",
            ]
        )


def test_drug_class_lookup_fail():
    drug = core.PUGLookupResponse(cid="1", canonical_smiles="2", sid=None)
    cid = drug.cid

    mock_request_session = mock.MagicMock()

    with mock.patch(
        "drug_resolver.requests_wrapper.get_cached_session"
    ) as get_cached_session:
        get_cached_session.return_value = mock_request_session
        response_mock = mock.MagicMock()

        mock_request_session.get.return_value = response_mock

        response_mock.json.return_value = {
            "Record": {
                "RecordType": "SID",
                "RecordNumber": 472407780,
                "RecordTitle": "DOSTARLIMAB",
            }
        }

        result = core.drug_class_lookup(cid)
        assert result is None


def test_replace_meaningless_ascii_characters_with_space():
    assert core.replace_meaningless_ascii_characters_with_space("hello'") == "hello"
    assert (
        core.replace_meaningless_ascii_characters_with_space("hello_hello")
        == "hello hello"
    )
    assert (
        core.replace_meaningless_ascii_characters_with_space("drug1/drug2")
        == "drug1 drug2"
    )
    assert core.replace_meaningless_ascii_characters_with_space("(-)(+)") == "(-)(+)"


def test_replace_non_ascii_characters_with_space():
    assert core.replace_non_ascii_characters_with_space("hello－1😋 ") == "hello-1"

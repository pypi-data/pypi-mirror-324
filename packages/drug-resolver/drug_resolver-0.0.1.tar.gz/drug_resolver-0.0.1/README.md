# Drug Resolver

This package offers a simple way to resolve drug names to their corresponding PubChem CIDs entries.

This is useful for identifying unknown drug synonyms or matching drug synonyms across different datasets in an automated way.


## Installation

```sh
pip install drugresolver
```

## Usage

```python
from drug_resolver import resolve_drug

d1 = resolve_drug("tetracycline hcl")
print(d1)
"""
ResolvedDrug(
   name='Tetracycline hydrochloride', 
   pubchem_compound_id='54704426', 
   pubchem_substance_id='103591391', 
   smiles='CN(C)C1C(=O)C(C(N)=O)=C(O)C2(O)C(=O)C3=C(O)c4c(O)cccc4C(C)(O)C3CC12.Cl', 
   drug_classes=None, 
   fda_approval=<FDAApprovalStatus.APPROVED: 'APPROVED'>, 
   pubchem_parent_compound_id='54675776')
"""

d2 = resolve_drug("Sumycin")
print(d2)
"""
ResolvedDrug(
    name='Tetracycline', 
    pubchem_compound_id='54675776', 
    pubchem_substance_id='124766046', 
    smiles='CN(C)C1C(=O)C(C(N)=O)=C(O)C2(O)C(=O)C3=C(O)c4c(O)cccc4C(C)(O)C3CC12', 
    drug_classes=frozenset({'Established Pharmacologic Class [EPC] - Tetracycline-class Antimicrobial'}), 
    fda_approval=<FDAApprovalStatus.APPROVED: 'APPROVED'>, 
    pubchem_parent_compound_id=None)
"""

assert d1 == d2 # True
```

The equality operator between `ResolvedDrug` objects will return `True` under the following conditions:

- The `pubchem_compound_id` attribute is the same
- The `pubchem_substance_id` attribute is the same
- The `smiles` strings refer to the same molecule
- Two compounds share the same `pubchem_parent_compound_id` or the `pubchem_compound_id` is the same as the `pubchem_parent_compound_id` of the other compound.
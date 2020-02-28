"""
Retrieve a structure from Chemspider and convert it a local PDB file

Other services:
   PubChem, ChEBI - was able to find relevant compounds w/simple names
      (e.g. 'pmma', 'polyethylene'), but structure files were 2D and wrong

   Other services were not helpful -- couldn't find anything w/simple names

Copyright

LICENSE
"""

import openbabel as ob
from chemspipy import ChemSpider

def get_chemspider_structure(csid):
   """
   Get a molecular structure from ChemSpider, generate a PDB file of the 
   structure, and return the name of the PDB file
   """
   pdbpath = '{}.pdb'.format(csid)
   token = 'a03b1636-afc3-4204-9a2c-ede27680577c' # XXX

   cs = ChemSpider(token)
   cmpd = cs.get_compound(csid)

   conv = ob.OBConversion()
   conv.SetInAndOutFormats('mol', 'pdb')
   mol = ob.OBMol()
   conv.ReadString(mol, cmpd.mol_3d)
   mol.AddHydrogens()
   with open(pdbpath, 'w') as f:
      f.write(conv.WriteString(mol))
   return pdbpath

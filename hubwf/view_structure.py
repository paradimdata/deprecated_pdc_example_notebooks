"""
nglview wrapper

Copyright

LICENSE
"""

import nglview as nv

def view_ball_stick(structfile):
   """Return a nglview object to view structfile as a ball+stick model"""
   v = nv.show_structure_file(structfile)
   v.representations = [{'type': 'ball+stick', 'params': {}}]
   v.parameters = {'backgroundColor': 'black'}
   return v
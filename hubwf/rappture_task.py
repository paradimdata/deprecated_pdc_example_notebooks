"""
RapptureTask class

Copyright

LICENSE
"""

import os, glob
import xml.etree.ElementTree as et
import hublib.rappture as Rappture
from .task import Task

class RapptureTask(Task):
   def __init__(self, tool_name):
      Task.__init__(self)
      self._tool = Rappture.Tool(tool_name)
      xml = et.fromstring(str(self._tool.xml()))  # XXX duplicate inputs
      self._inxml = xml.find('input')
      self._outxml = None

   def _add_el_to_path(self, path, el):
      t = el.tag
      name = el.attrib.get('id', '(noid)')
      return '{0}.{1}({2})'.format(path, t, name) if len(path) > 0 else t

   def _search(self, xml, label, path, exact=False):
      """
      Search xml recursively, building path along the way; return the path
      for the element whose about.label text contains label
      """
      p = self._add_el_to_path(path, xml)
      k = None
      for el in xml:
         about_el = el.find('about')
         if about_el is not None:
            label_el = about_el.find('label')
            if label_el is not None:
               if exact: 
                  if label == label_el.text: 
                     k = self._add_el_to_path(p, el)
               elif label in label_el.text:
                  k = self._add_el_to_path(p, el)
         if k is None:
            k = self._search(el, label, p, exact)
      return k

   def set_input_value(self, key, value, exact=False):
      """Set the value of an input whose label contains key"""
      k = self._search(self._inxml, key, '', exact)
      self.inputs[k] = {'value': value, 'source': None}

   def set_input_source(self, key, srctask, outkey, exact=False):
      """
      Set the source of an input whose label contains key to the output 
      value whose label contains outkey in the indicated task
      """
      k = self._search(self._inxml, key, '', exact)
      self.inputs[k] = {'value': None, 'source': (srctask, outkey)}

   def _merge_xml(self, srcxml, path):
      p = self._add_el_to_path(path, srcxml)
      cel = srcxml.find('current')
      if cel is not None:
         self._tool['{0}.current'.format(p)] = cel.text
      for c in srcxml:
         self._merge_xml(c, p)

   def _handle_loader(self, key):
      """
      Search the tools' examples/ directory for a loader XML file with 
      about.label containing the value of key; when found, copy all input
      values in that file to self._tool
      """
      el = self._tool[key]
      exglob = el['example'].value
      rappture_dir = os.path.split(self._tool.tool)[0]
      p = os.path.join(rappture_dir, 'examples', exglob)
      for f in glob.glob(p):
         xml = et.parse(f)
         root = xml.getroot()
         about_el = root.find('about')
         if about_el is not None:
            label_el = about_el.find('label')
            if label_el is not None: 
               if self.inputs[key]['value'] in label_el.text:
                  # matched the loader file
                  self._merge_xml(root.find('input'), '')
                  break

   def _run(self):
      """Set current input values, run the tool, and extract outputs"""
      for k,d in self.inputs.items():
         if 'loader' in k:
            self._handle_loader(k)
         else:
            self._tool['{0}.current'.format(k)] = d['value']
      self._tool.run()
      xml = et.fromstring(str(self._tool.xml()))  # XXX duplicate outputs
      self._outxml = xml.find('output')
      # Don't set self.outputs

   def get_output_value(self, key, exact=False):
      """Return the value of an output whose label contains key"""
      k = self._search(self._outxml, key, '', exact)
      return self._tool['{0}.current'.format(k)].value

   def get_output_pdb(self, key, exact=False):
      """Return the PDB string of an output whose label contains key"""
      k = self._search(self._outxml, key, '', exact)
      return self._tool['{0}.components.molecule.pdb'.format(k)].value
"""
Task class

Copyright

LICENSE
"""

class Task(object):
   def __init__(self):
      self.inputs = {}
      self.outputs = {}
      self.post_proc = None

   def set_input_value(self, key, value):
      """Child classes may override"""
      self.inputs[key] = {'value': value, 'source': None}

   def set_input_source(self, key, srctask, outkey):
      """Child classes may override"""
      self.inputs[key] = {'value': None, 'source': (srctask, outkey)}

   def _run(self):
      """
      Execute the task using inputs, then set outputs.  Implemented by 
      child classes.
      """
      pass

   def run(self):
      """Set inputs, call _run() and then post_proc(), if defined"""
      for k,d in self.inputs.items():
         if d['source'] is not None:
            srctask = d['source'][0]
            outkey = d['source'][1]
            d['value'] = srctask.get_output_value(outkey)
      self._run()
      if self.post_proc is not None:
         self.post_proc()

   def get_output_value(self, key):
      """Child classes may override"""
      return self.outputs[key]['value']
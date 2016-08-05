"""A test class for the formatparser module"""
import unittest
import sys
import code
from code import formatparser as fpar

class formatparser_init(unittest.TestCase):
  def test_init_badfilename(self):
    testfilename = "fakefile"
    try:
      fp = fpar.formatparser(testfilename)
    except ValueError as ex:
      "Expected"
    except Exception as ex:
      if not ex.args == "Not implemented":
        raise
    else:
      self.assertEqual(fp.spec, "")
      self.assertEqual(fp.delim, "")
      self.assertEqual(fp.col_titles, list())
      self.assertEqual(fp.extran_chars, dict())
      self.assertEqual(fp.xfunc, None)
      self.assertEqual(fp.yfunc, None)
  def init_goodfilename(self):
    testfilename = "test/realfile"
    try:
      fp = fpar.formatparser(testfilename)
    
    except Exception as ex:  
      #Should not be any other type of error
      if not ex.args == "Not implemented":
        raise ex
    else:
      self.assertEqual(fp.spec, open(testfilename).readlines())
      self.assertEqual(fp.delim, ",")
      self.assertEqual(fp.col_titles, ["a", "columntwo", "c"])
      self.assertEqual(fp.extran_chars, {1: ["<", ">"]})
      self.assertEqual(fp.xfunc, lambda x: x[0])
      self.assertEqual(fp.yfunc, lambda x: x[1] * x[2])
      
class formatparser_readColumns(unittest.TestCase):
  fp = None
  def setUp(self):
    self.fp = fpar.formatparser('test/realfile')
    self.fp.delim = ","
    if self.fp is None:
      raise Exception("No format parser created")

  def test_simple_multivaldelimiter_detection(self):
    line = r"a,[Docs]3,catastrophe"

    titles, chars = self.fp.readColumns(line)
    self.assertEquals(titles, ["a", "Docs", "catastrophe"])
    self.assertEquals(chars, {})

  def test_complex_multivardelimiter_detection(self):
    line = r"\[a(),\[\[[b\]\]]2,mary had a little lamb"

    titles, chars = self.fp.readColumns(line)
    self.assertEquals(titles, ["a", "b", "mary had a little lamb"])
    self.assertEquals(chars, {"a":["["], "b":["[", "[", "]", "]"]})

  def test_no_value_delimiter(self):
    line = r"a;b;c;d;e;f;fdsafds as"

    titles, chars = self.fp.readColumns(line)
    self.assertEquals(titles, ["abcdeffdsafds as"])
    self.assertEquals(chars, {})

class formatparser_readFunc(unittest.TestCase):
  fp = None
  def setUp(self):
    #Contains 3 columns: a, columntwo, and c
    self.fp = fpar.formatparser('test/realfile')
    if self.fp is None:
      raise Exception("No format parser created")

  def testdict(self, dictionary=None):
    if not dictionary:
      return

    for key in dictionary.keys():
      func = self.fp.readFunc(key)
      expected = dictionary[key][0].format(fpar.COLUMN_VARIABLE_NAME, 
          *dictionary[key][1])
      self.assertEquals(func, expected)

  def test_simple_valid_column_function(self):
    line = '1'
    linesandargs = {
        '1' : ("{}[{}]",[1]),
        '0' : ("{}[{}]",[0]),
        '2' : ("{}[{}]",[2])}
    self.testdict(linesandargs)
    
  def test_simple_valid_col_op_function(self):
    linesandargs = {
        '- 1'   : ("-{}[{}]",[1]),
        '+ 1'   : ("+{}[{}]",[1]),
        '0 - 1' : ("{0}[{1}]-{0}[{2}]", [0, 1]),
        '1 + 2' : ("{0}[{1}]+{0}[{2}]", [1, 2]),
        '2 / 1' : ("{0}[{1}]/{0}[{2}]", [2, 1]),
        '1 * 1' : ("{0}[{1}]*{0}[{1}]", [1]),
        '1 + 2 // 0 - 1' : ("{0}[{1}]+{0}[{2}]//{0}[{3}]-{0}[{1}]", [1, 2, 0])}
    self.testdict(linesandargs)

  def test_complex_valid_col_op_function(self):
    linesandargs = {
        '1 + 2 // 0 - 1' : ("{0}[{1}]+{0}[{2}]//{0}[{3}]-{0}[{1}]",
                            [1, 2, 0]),
        '1 - 2 ** 0 ** 1' : ("{0}[{1}]-{0}[{2}]**{0}[{3}]**{0}[{1}]",
                            [1, 2, 0])}
    self.testdict(linesandargs)

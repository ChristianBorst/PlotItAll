"""formatparser - interprets a format specification for a data file
   A formatparser instance object must be created using the filename of a 
   format specification. The instance then functions as an API for 
   understanding the contents of an associated data file."""
import sys
import re

#The line order of the format specification file
DELIMITER_LINE = 0
FORMAT_LINE = 1
X_FUNCTION_LINE = 2
Y_FUNCTION_LINE = 3
#Denotation characters for where a column title spans multiple delimited values
MULTI_VALUE_DELIMITERS = ['[', ']']
#Denotation character for variable length of a multiple-valued column title
VARIABLE_MULTI_VALUE_DELIMITER = '*'
#MUST be the name of the variable holding all of the data's columns in plotitall
COLUMN_VARIABLE_NAME = 'columns' 

class formatparser():
  """spec - The actual specification file contents
   delim - The delimiter between columns of the data file
   col_titles - The human-readable titles of each column
   extran_chars - The characters to ignore in each particular column
   xfunc - A function of the data file's columns to perform for plotting on
      the x axis
   yfunc - A function of the data file's columns to perform for plotting on
      the y axis"""
  #Mutable local attributes
  spec = ""
  delim = ""
  col_titles = list()
  extran_chars = dict()
  xfunc = None
  yfunc = None

  def __init__(self, filename):
    """Initializes the instance object with the specification contents,
     delimiter, column titles, extraneous characters,
     the x-axis function, and the y-axis function."""
    try:
      self.spec = open(filename).readlines()
    except IOError as io:
      print("Invalid filename given, no such file found")
      raise ValueError()

    #TODO: Test that rstrip only removes the ending newline character
    self.delim = self.spec[DELIMITER_LINE].rstrip('\n') 
    self.col_titles, self.extran_chars = self.readColumns(self.spec[FORMAT_LINE])
    self.xfunc = self.readFunc(self.spec[X_FUNCTION_LINE])
    self.yfunc = self.readFunc(self.spec[Y_FUNCTION_LINE])

  def readColumns(self, line):
    """Reads the columns of the format specification and returns a pair of
     lists containing the column titles and the extraneous characters to 
     ignore in each column, respectively."""

    columntitles = []
    extranchars = {}
    #Split the line by the delimiter
    for col in line.split(self.delim):
      num_multi_vals = 1 #Set to -1 if variable
    # Find the location of any MUTLI_VALUE_DELIMITERS not preceeded by backslashes
      multis = [(l, r) for l in range(len(col)) \
                if col[l] == MULTI_VALUE_DELIMITERS[0] \
                if col[l-1] != "\\" \
                for r in range(len(col)) \
                if col[r] == MULTI_VALUE_DELIMITERS[1] \
                if col[r-1] != "\\"]
    # Store the number of values to associate with the MULTI_VALUE_DELIMITERS
    #  single column name, or variable if VARIABLE_MULTI_VALUE_DELIMITER used
      if multis:
        #location of the specified number of values
        try:
          spec_multi_vals = col[multis[0][1] + 1]
        except IndexError:
          raise ValueError("No value given after specifying multiple values "\
              + "for a column in {0}.".format(col))
        #Denote variable values, or set to specified number of values
        if spec_multi_vals == "*":
          num_multi_vals = -1
        elif spec_multi_vals.isdigit():
          num_multi_vals = spec_multi_vals
        else:
          raise ValueError("No value given after specifying multiple values " \
              + "for a column in {0}.")
    # Find any extraneous characters (prefixed by backslashes)
      extrans = [col[c] for c in range(len(col)) if col[c-1] == "\\"]
    # Finally, search for the column titles in what's left of the split item
      title = re.sub('[^a-zA-Z\ ]', '', col)

    # Insert the column titles in order into the list, make a dictionary item
    #  for each column with the extraneous characters associated
      if not title:
        raise ValueError("Invalid title supplied")
      columntitles.append(title)
      if extrans:
        extranchars[title] = extrans
    #Return the column titles and their associated extraneous characters
    return columntitles, extranchars

  def readFunc(self, line):
    """Reads a line specifying a function of columns and returns a function
     of the data to perform for plotting."""
    func = ""
    #Viable operators
    acceptedOps = ['+', '-', '*', '/', '//', \
                   '&', '|', '^', '~', '<<', '>>', \
                   '%', '**']
    for w in line.rstrip('\n').split():
      digit = False
      op = False
      #Find all column indicies in the line
      if w.isdigit():
        digit = True
        if not int(w) < len(self.col_titles):
          #If any indicies are out of range, throw a helpful error message 
          raise ValueError("Column index {0} is out of range.".format(w))
        func += "{0}[{1}]".format(COLUMN_VARIABLE_NAME, w)
      #Iteratively search for python operators to perform on the columns
      if w in acceptedOps:
        func += w
        op = True
      elif not digit: #w is not an operator nor a column index
        raise ValueError(
            "Invalid operator \"{0}\" to perform on the columns.".format(w))
      
      if not digit ^ op: #A digit must follow an operator, and vice versa
        raise ValueError("Cannot compose a function of columns without " \
                   + "operators, nor vice versa. Function: {0}".format(func))

    if not func:
      raise ValueError("No columns or operators to make a function from.")

    #Return the generated function
    return func

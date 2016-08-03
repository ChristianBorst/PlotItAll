# PlotItAll
A python program which automates the plotting of formatted data files using matplotlib.

Requires a format specifier file and the name of the formatted datafile, then deciphers the data in the file in order to have matplotlib make a graph. The finished graph will be written to the given output filename.

---
*nix usage: `./plotitall.py DATA_FILENAME FORMAT_SPECIFIER_NAME OUTPUT_FILENAME`

##Data:
The data to be used for plotting must be in a single file with a single format specified in the format specifier. If multiple files have the same format and simply need to be appended to each other, then instead of 

##Format Specifier:
The format specifier is a file given in a particular format which specifies how
the data to be plotted is arranged.

1. The first line of the file should be the delimiter between each column of data
  * e.g. "," or "; "
2. The second line should be a format string with the following properties:
  * Column titles may only contain alphabetical characters and spaces
  * Column titles should be separated by the delimiter given in line 1
  * Extraneous characters to be filtered out should be prefixed by a backslash (\\)
      * e.g. a column titled 'Data' surrounded by angle brackets (<'s and >'s) is denoted `\<Data\>`
      * Due to the next property, square brackets are reserved, and should not be used
  * A column whose data spans multiple contiguous delimited columns should be specified using square brackets and followed by a number of occurrances or an asterisk (\*) for variable occurrances
      * e.g. `[Data]3` will capture 3 values into one column titled Data
      * If the number of columns is variable an asterisk (\*) must be used, and the data must be distinguished by some extraneous characters
          * e.g. `[\<Data\>]*` will capture any number of values surrounded by angle brackets to a column titled Data
3. The third line of the file should specify a function of the columns to plot on the x axis using their 0-based indicies
  * e.g. "0" for a x value of the first column, or "2 * 4" for a function which multiplies the 3rd and 5th columns
4. The fourth line of the file should specify a function of the columns to plot on the y axis
  * e.g. "0" for a y value of the first column, or "2 * 4" for an y function which multiplies the 3rd and 5th columns

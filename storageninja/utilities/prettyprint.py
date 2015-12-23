""" Pretty Printer Wrapper """
import pprint

# Setup Pretty Printing
ppsetup = pprint.PrettyPrinter(indent=4)
pp = ppsetup.pprint
pf = ppsetup.pformat

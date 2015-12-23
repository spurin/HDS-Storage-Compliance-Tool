# ------------------------------------------------------------------------------
# Builtin Imports
# ------------------------------------------------------------------------------
import re

# ------------------------------------------------------------------------------
# standardise_wwn - standardises a wwn to 16 lowercase hexadecimal characters
# ------------------------------------------------------------------------------
def standardise_wwn(wwn):
    return re.sub(r'(\W+)', '', wwn).lower()

# ------------------------------------------------------------------------------
# true_or_false - stringifies 0 as false and 1 as true
# ------------------------------------------------------------------------------
def true_or_false(value):
    if value == '0':
        return 'false'
    elif value == '1':
        return 'true'
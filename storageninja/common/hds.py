# ------------------------------------------------------------------------------
# Builtin Imports
# ------------------------------------------------------------------------------
import re

# ------------------------------------------------------------------------------
# extract_portname - Standardises the portname
# ------------------------------------------------------------------------------
def extract_portname(portname):
    return re.sub(r'(-\d+$)', '', portname)

# ------------------------------------------------------------------------------
# remove_subversion - Removes the subversion from a version string, used for
# consistency between hds_cs_cli and serviceport output
# ------------------------------------------------------------------------------
def remove_subversion(value):
    return re.sub(r'(-\d\d$)', '', value)

# ------------------------------------------------------------------------------
# create_pdevid - Create a port dev id based on the objectID
# ------------------------------------------------------------------------------
def create_pdevid(dataset):
    dataset['pdevid'] = dataset['objectID'].split('.')[3]

# ------------------------------------------------------------------------------
# create_displayDevNum - Create an equivalent displayDevNum based on the 
# objectID
# ------------------------------------------------------------------------------
def create_displayDevNum(dataset):

    if re.match('^[A-Z]+\.R', dataset['objectID']) or re.match('^[A-Z]+\.HM', dataset['objectID']):

        # ------------------------------------------------------------------------------
        # Convert devNum to hex
        # ------------------------------------------------------------------------------
        value = str(hex(int(dataset['devNum']))[2:]).upper()

        # ------------------------------------------------------------------------------
        # Add leading 0's where applicable
        # ------------------------------------------------------------------------------
        while len(value) < 6:
            value = "0" + value

        # ------------------------------------------------------------------------------
        # Split with semicolons
        # ------------------------------------------------------------------------------
        value = value[0:2] + ':' + value[2:4] + ':' + value[4:6]

        # ------------------------------------------------------------------------------
        # Add a new record
        # ------------------------------------------------------------------------------
        dataset['displayDevNum'] = value

    elif re.match('^[A-Z]+\.AMS', dataset['objectID']) or re.match('^[A-Z]+\.HUS', dataset['objectID']) or re.match('^[A-Z]+\.D\d+', dataset['objectID']):

        value = int(dataset['devNum'])
        value = '{:,}'.format(value, ',d')
        # ------------------------------------------------------------------------------
        # Alternatives
        #value = '{:20,.2f}'.format(value, ',d')
        #value = format(value, ',d')
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        # Add a new record
        # ------------------------------------------------------------------------------
        dataset['displayDevNum'] = value

    elif re.match('^[A-Z]+\.USP', dataset['objectID']):

        # ------------------------------------------------------------------------------
        # Convert devNum to hex
        # ------------------------------------------------------------------------------
        value = str(hex(int(dataset['devNum']))[2:]).upper()

        # ------------------------------------------------------------------------------
        # Add leading 0's where applicable
        # ------------------------------------------------------------------------------
        while len(value) < 4:
            value = "0" + value

        # ------------------------------------------------------------------------------
        # Split with semicolons
        # ------------------------------------------------------------------------------
        value = value[0:2] + ':' + value[2:4]

        # ------------------------------------------------------------------------------
        # Add a new record
        # ------------------------------------------------------------------------------
        dataset['displayDevNum'] = value

    # ------------------------------------------------------------------------------
    # Fail back on devNum if unknown array
    # ------------------------------------------------------------------------------
    else:
        dataset['displayDevNum'] = dataset['devNum']

# ------------------------------------------------------------------------------
# create_displayPvolDevNum - Create an equivalent displayPvolDevNum based on the 
# pvolDevNum and pvolArrayType
# ------------------------------------------------------------------------------
def create_displayPvolDevNum(dataset):

    if re.match('R', dataset['pvolArrayType']) or re.match('^HM', dataset['pvolArrayType']):

        # ------------------------------------------------------------------------------
        # Convert devNum to hex
        # ------------------------------------------------------------------------------
        value = str(hex(int(dataset['pvolDevNum']))[2:]).upper()

        # ------------------------------------------------------------------------------
        # Add leading 0's where applicable
        # ------------------------------------------------------------------------------
        while len(value) < 6:
            value = "0" + value

        # ------------------------------------------------------------------------------
        # Split with semicolons
        # ------------------------------------------------------------------------------
        value = value[0:2] + ':' + value[2:4] + ':' + value[4:6]

        # ------------------------------------------------------------------------------
        # Add a new record
        # ------------------------------------------------------------------------------
        dataset['displayPvolDevNum'] = value

    elif re.match('^AMS', dataset['pvolArrayType']) or re.match('^HUS', dataset['pvolArrayType']) or re.match('^D\d+', dataset['objectID']):

        value = int(dataset['pvolDevNum'])
        value = '{:,}'.format(value, ',d')
        # ------------------------------------------------------------------------------
        # Alternatives
        #value = '{:20,.2f}'.format(value, ',d')
        #value = format(value, ',d')
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        # Add a new record
        # ------------------------------------------------------------------------------
        dataset['displayPvolDevNum'] = value

    elif re.match('^USP', dataset['pvolArrayType']):

        # ------------------------------------------------------------------------------
        # Convert devNum to hex
        # ------------------------------------------------------------------------------
        value = str(hex(int(dataset['pvolDevNum']))[2:]).upper()

        # ------------------------------------------------------------------------------
        # Add leading 0's where applicable
        # ------------------------------------------------------------------------------
        while len(value) < 4:
            value = "0" + value

        # ------------------------------------------------------------------------------
        # Split with semicolons
        # ------------------------------------------------------------------------------
        value = value[0:2] + ':' + value[2:4]

        # ------------------------------------------------------------------------------
        # Add a new record
        # ------------------------------------------------------------------------------
        dataset['displayPvolDevNum'] = value

    else:
        # ------------------------------------------------------------------------------
        # If the pvolObjectID is not available, it's an unknown array ...
        # Use the default format
        # ------------------------------------------------------------------------------
        value = int(dataset['pvolDevNum'])
        value = '{:,}'.format(value, ',d')

        dataset['displayPvolDevNum'] = value

# ------------------------------------------------------------------------------
# create_displaySvolDevNum - Create an equivalent displaySvolDevNum based on the 
# svolDevNum and svolArrayType
# ------------------------------------------------------------------------------
def create_displaySvolDevNum(dataset):

    if re.match('R', dataset['svolArrayType']) or re.match('^HM', dataset['svolArrayType']):

        # ------------------------------------------------------------------------------
        # Convert devNum to hex
        # ------------------------------------------------------------------------------
        value = str(hex(int(dataset['svolDevNum']))[2:]).upper()

        # ------------------------------------------------------------------------------
        # Add leading 0's where applicable
        # ------------------------------------------------------------------------------
        while len(value) < 6:
            value = "0" + value

        # ------------------------------------------------------------------------------
        # Split with semicolons
        # ------------------------------------------------------------------------------
        value = value[0:2] + ':' + value[2:4] + ':' + value[4:6]

        # ------------------------------------------------------------------------------
        # Add a new record
        # ------------------------------------------------------------------------------
        dataset['displaySvolDevNum'] = value

    elif re.match('^AMS', dataset['svolArrayType']) or re.match('^HUS', dataset['svolArrayType']) or re.match('^D\d+', dataset['objectID']):

        value = int(dataset['svolDevNum'])
        value = '{:,}'.format(value, ',d')
        # ------------------------------------------------------------------------------
        # Alternatives
        #value = '{:20,.2f}'.format(value, ',d')
        #value = format(value, ',d')
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        # Add a new record
        # ------------------------------------------------------------------------------
        dataset['displaySvolDevNum'] = value

    elif re.match('^USP', dataset['svolArrayType']):

        # ------------------------------------------------------------------------------
        # Convert devNum to hex
        # ------------------------------------------------------------------------------
        value = str(hex(int(dataset['svolDevNum']))[2:]).upper()

        # ------------------------------------------------------------------------------
        # Add leading 0's where applicable
        # ------------------------------------------------------------------------------
        while len(value) < 4:
            value = "0" + value

        # ------------------------------------------------------------------------------
        # Split with semicolons
        # ------------------------------------------------------------------------------
        value = value[0:2] + ':' + value[2:4]

        # ------------------------------------------------------------------------------
        # Add a new record
        # ------------------------------------------------------------------------------
        dataset['displaySvolDevNum'] = value

    else:
        # ------------------------------------------------------------------------------
        # If the svolObjectID is not available, it's an unknown array ...
        # Use the default format
        # ------------------------------------------------------------------------------
        value = int(dataset['svolDevNum'])
        value = '{:,}'.format(value, ',d')

        dataset['displaySvolDevNum'] = value

# ------------------------------------------------------------------------------
# set_rep_status - Used to give a more meaninful name to replication status
# where applicable
# ------------------------------------------------------------------------------
def set_rep_status(status):
    lookup_table = {
        '-1': 'Unknown',
        '0': 'Simplex',
        '1': 'Pair',
        '8': 'Copying',
        '9': 'Reverse-Copying',
        '16': 'Split',
        '17': 'Error',
        '18': 'Error in LUSE',
        '24': 'Suspending',
        '25': 'Deleting',
    }

    if status in lookup_table:
        return lookup_table[status]
    else:
        return status
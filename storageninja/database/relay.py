# ------------------------------------------------------------------------------
# Relay class - Used for relaying database commands to multiple database objects
# ------------------------------------------------------------------------------
class Relay(object):

    # ------------------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------------------
    def __init__(self, databases=[], schema=None):
        '''
        Constructor
        '''
        self.databases = databases
        self.schema = schema
        
    # ------------------------------------------------------------------------------
    # Insert Data
    # ------------------------------------------------------------------------------
    def insert_dict(self, data):
        for database in self.databases:
            database.insert_dict(self.schema, data)
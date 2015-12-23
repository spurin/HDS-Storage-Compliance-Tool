# ------------------------------------------------------------------------------
# Builtin Imports
# ------------------------------------------------------------------------------
import requests
import xmldataset
import logging
import inspect

# ------------------------------------------------------------------------------
# Collector Instance 
# ------------------------------------------------------------------------------
class Instance(object):

    # ------------------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------------------
    def __init__(self,
                 username='system',
                 password='password',
                 server=None,
                 api=7.0,
                 xml_schema=None,
                 xml_process=None,
                 ):

        # ------------------------------------------------------------------------------
        # Configure logging
        # ------------------------------------------------------------------------------
        self.logger = logging.getLogger(__name__)

        # ------------------------------------------------------------------------------
        # Local cache store
        # ------------------------------------------------------------------------------
        self.cached = {}
        self.username = username
        self.password = password
        self.server = 'http://' + server + ':2001/service/StorageManager'
        self.api = api
        self.xml_schema = xml_schema
        self.xml_process = xml_process

        # ------------------------------------------------------------------------------
        # XML Lookup Dictionary
        # ------------------------------------------------------------------------------
        self.custom_xml_lookup = {
            'hds_cs_getstoragearray': '',

            'hds_cs_getstoragearray_port': '''
          <Port />''',

            'hds_cs_getstoragearray_pool': '''
          <JournalPool />''',

            'hds_cs_getstoragearray_arraygroup': '''
          <ArrayGroup />''',

            'hds_cs_getstoragearray_ldev': '''
          <LDEV>
            <ObjectLabel />
          </LDEV>''',

            'hds_cs_getstoragearray_pdev': '''
          <PDEV />''',

            'hds_cs_getstoragearray_replicationinfo': '''
          <ReplicationInfo />''',

            'hds_cs_getstoragearray_hoststoragedomain_hsdsubinfo_path_wwn': '''
          <HostStorageDomain>
            <Path />
            <WorldWideName />
          </HostStorageDomain>''',

            'hds_cs_getstoragearray_portcontroller': '''
          <PortController />''',

            'hds_cs_getstoragearray_component': '''
          <Component />''',
        }

    # ------------------------------------------------------------------------------
    # The Service Port API requires object ID references within the query, make a 
    # one time call to generate a lookup table
    # ------------------------------------------------------------------------------
    def _get_serial_to_objectid(self, serial):

        # ------------------------------------------------------------------------------
        # If we do not have the serial numbers to object id's run and cache the entire 
        # lookup table for future use
        # ------------------------------------------------------------------------------
        if '_get_serial_to_objectid' not in self.cached:
            self.logger.info('Capturing lookup table of Serial Number to Model')

            self.cached['_get_serial_to_objectid'] = {}

            initial_response = self.hds_cs_getstoragearray()

            # ------------------------------------------------------------------------------
            # Process each key
            # ------------------------------------------------------------------------------
            for key in initial_response.keys():

                # ------------------------------------------------------------------------------
                # Process each entry
                # ------------------------------------------------------------------------------
                for entry in initial_response[key]:

                    # ------------------------------------------------------------------------------
                    # Store the serialNumber to objectID
                    # ------------------------------------------------------------------------------
                    self.cached['_get_serial_to_objectid'][int(entry['serialNumber'])] = entry['objectID']

        return self.cached['_get_serial_to_objectid'][serial]

    # ------------------------------------------------------------------------------
    # Wrappers around the generic method
    # ------------------------------------------------------------------------------
    def hds_cs_getstoragearray(self, serial=[]):
        return self._hds_cs_generic(serial=serial)

    def hds_cs_getstoragearray_port(self, serial=[]):
        return self._hds_cs_generic(serial=serial)

    def hds_cs_getstoragearray_pool(self, serial=[]):
        return self._hds_cs_generic(serial=serial)

    def hds_cs_getstoragearray_arraygroup(self, serial=[]):
        return self._hds_cs_generic(serial=serial)

    def hds_cs_getstoragearray_ldev(self, serial=[]):
        return self._hds_cs_generic(serial=serial)

    def hds_cs_getstoragearray_pdev(self, serial=[]):
        return self._hds_cs_generic(serial=serial)

    def hds_cs_getstoragearray_replicationinfo(self, serial=[]):
        return self._hds_cs_generic(serial=serial)

    def hds_cs_getstoragearray_hoststoragedomain_hsdsubinfo_path_wwn(self, serial=[]):
        return self._hds_cs_generic(serial=serial)

    def hds_cs_getstoragearray_portcontroller(self, serial=[]):
        return self._hds_cs_generic(serial=serial)

    def hds_cs_getstoragearray_component(self, serial=[]):
        return self._hds_cs_generic(serial=serial)

    # ------------------------------------------------------------------------------
    # Generic handler for all other collection methods
    # ------------------------------------------------------------------------------
    def _hds_cs_generic(self, serial=[]):

        # ------------------------------------------------------------------------------
        # If a single serial is provided coerce to a list for standardised processing
        # ------------------------------------------------------------------------------
        if isinstance(serial, int):
            serial = [serial]

        # ------------------------------------------------------------------------------
        # Collect all if no serials were provided, alternatively, if multiple were 
        # provided collect all and filter later
        # ------------------------------------------------------------------------------
        if len(serial) == 0 or len(serial) > 1:
            all_option = ' option="all"'
            objectid = ''

        else:
            serial_objectid = self._get_serial_to_objectid(serial[0])
            all_option = ''
            objectid = ' objectID="%s"' % serial_objectid

        # ------------------------------------------------------------------------------
        # Capture the calling method's name and use that to correlate to the schema
        # and the custom xml information
        # ------------------------------------------------------------------------------
        caller = inspect.stack()[1][3]
        xml_schema = getattr(self.xml_schema, caller)
        custom_request = self.custom_xml_lookup[caller]

        # ------------------------------------------------------------------------------
        # Log execution
        # ------------------------------------------------------------------------------
        if objectid != '':
            self.logger.info('Collecting %s for%s' % (caller, objectid))
        else:
            self.logger.info('Collecting %s for all' % caller)

        # ------------------------------------------------------------------------------
        # n.b. XML for individual arrays is not practical for this request as the same
        # request needs to be made to gather objectID, instead parse all and limit to
        # arrays in scope
        # ------------------------------------------------------------------------------
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<HiCommandServerMessage>
  <APIInfo version="''' + self.api + '''" />
  <Request>
    <StorageManager>
      <Get target="StorageArray"''' + all_option + '''>
        <StorageArray''' + objectid + '''>''' + custom_request + '''
        </StorageArray>
      </Get>
    </StorageManager>
  </Request>
</HiCommandServerMessage>'''

        # ------------------------------------------------------------------------------
        # Add XML header
        # ------------------------------------------------------------------------------
        headers = {'Content-Type': 'application/xml'}

        # ------------------------------------------------------------------------------
        # Capture a response
        # ------------------------------------------------------------------------------
        response = requests.post(self.server, data=xml, headers=headers, auth=(self.username, self.password))

        # ------------------------------------------------------------------------------
        # If there was an exception raise
        # ------------------------------------------------------------------------------
        response.raise_for_status()

        # ------------------------------------------------------------------------------
        # Parse the XML as an initial_response subject to processing
        # ------------------------------------------------------------------------------
        initial_response = xmldataset.parse_using_profile(response.text, xml_schema, process=self.xml_process)

        # ------------------------------------------------------------------------------
        # Return response
        # ------------------------------------------------------------------------------
        return initial_response

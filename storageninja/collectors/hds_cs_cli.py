# ------------------------------------------------------------------------------
# Builtin Imports
# ------------------------------------------------------------------------------
import xmldataset
import logging
import inspect
import os

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
                 api='7.0',
                 xml_schema=None,
                 xml_process=None,
                 hicommand_binary=None,
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
        self.server = server
        self.hicommand_binary = hicommand_binary
        self.api = api
        self.xml_schema = xml_schema
        self.xml_process = xml_process

        # ------------------------------------------------------------------------------
        # Custom lookup
        # ------------------------------------------------------------------------------
        self.custom_command = {
            'hds_cs_getstoragearray': 'GetStorageArray',
            'hds_cs_getstoragearray_port': 'GetStorageArray subtarget=Port',
            'hds_cs_getstoragearray_pool': 'GetStorageArray subtarget=Pool',
            'hds_cs_getstoragearray_arraygroup': 'GetStorageArray subtarget=ArrayGroup',
            'hds_cs_getstoragearray_ldev': 'GetStorageArray subtarget=LDEV',
            'hds_cs_getstoragearray_pdev': 'GetStorageArray subtarget=PDEV',
            'hds_cs_getstoragearray_replicationinfo': 'GetStorageArray subtarget=ReplicationInfo',
            'hds_cs_getstoragearray_hoststoragedomain_hsdsubinfo_path_wwn': 'GetStorageArray subtarget=HostStorageDomain hsdsubinfo=PATH,WWN',
            'hds_cs_getstoragearray_portcontroller': 'GetStorageArray subtarget=PortController',
            'hds_cs_getstoragearray_component': 'GetStorageArray subtarget=Component',
        }

    # ------------------------------------------------------------------------------
    # The Service Port API requires object ID references within the query, make a 
    # one time call to generate a lookup table
    # ------------------------------------------------------------------------------
    def _get_serial_to_model(self, serial):

        # ------------------------------------------------------------------------------
        # If we do not have the serial numbers to object id's run and cache the entire 
        # lookup table for future use
        # ------------------------------------------------------------------------------
        if '_get_serial_to_model' not in self.cached:
            self.logger.info('Capturing lookup table of Serial Number to Model')

            self.cached['_get_serial_to_model'] = {}

            initial_response = self.hds_cs_getstoragearray()

            # Process each key
            for key in initial_response.keys():
                # Process each entry
                for entry in initial_response[key]:
                    # Store the serialNumber to objectID
                    self.cached['_get_serial_to_model'][int(entry['serialNumber'])] = entry['arrayType']

        return self.cached['_get_serial_to_model'][serial]

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
            array_specific = ''

        # ------------------------------------------------------------------------------
        # Populate single command information
        # ------------------------------------------------------------------------------
        else:
            array_specific = "serialnum=%s model=%s" % (serial[0], self._get_serial_to_model(serial[0]))

        # ------------------------------------------------------------------------------
        # Capture the calling method's name and use that to correlate to the schema
        # and the custom xml information
        # ------------------------------------------------------------------------------
        caller = inspect.stack()[1][3]
        xml_schema = getattr(self.xml_schema, caller)

        # ------------------------------------------------------------------------------
        # Populate the HiCommand command
        # ------------------------------------------------------------------------------
        custom_command = "%s http://%s:2001/service -u %s -p %s %s %s -f xml" % (
            self.hicommand_binary, self.server, self.username, self.password, self.custom_command[caller], array_specific)

        # ------------------------------------------------------------------------------
        # Log execution
        # ------------------------------------------------------------------------------
        if array_specific != '':
            self.logger.info('Collecting %s for %s' % (caller, array_specific))
        else:
            self.logger.info('Collecting %s for all' % caller)

        # ------------------------------------------------------------------------------
        # Capture XML
        # ------------------------------------------------------------------------------
        xml = os.popen(custom_command).read()

        # ------------------------------------------------------------------------------
        # Parse the XML as an initial_response subject to processing
        # ------------------------------------------------------------------------------
        try:
            initial_response = xmldataset.parse_using_profile(xml, xml_schema, process=self.xml_process)
        except Exception as e:
            print("DEBUG xml parsing exception - %s" % e)
            raise SystemExit

        # ------------------------------------------------------------------------------
        # Return response
        # ------------------------------------------------------------------------------
        return initial_response

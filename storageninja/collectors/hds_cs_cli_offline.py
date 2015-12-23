# ------------------------------------------------------------------------------
# Builtin Imports
# ------------------------------------------------------------------------------
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
                 directory=None,
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
        self.xml_schema = xml_schema
        self.xml_process = xml_process

        # ------------------------------------------------------------------------------
        # Store directory
        # ------------------------------------------------------------------------------
        self.directory = directory

        # ------------------------------------------------------------------------------
        # Custom lookup
        # ------------------------------------------------------------------------------
        self.custom_command = {
            'hds_cs_getstoragearray': 'GetStorageArray.xml',
            'hds_cs_getstoragearray_port': 'GetStorageArray_subtarget_port.xml',
            'hds_cs_getstoragearray_pool': 'GetStorageArray_subtarget_pool.xml',
            'hds_cs_getstoragearray_arraygroup': 'GetStorageArray_subtarget_arraygroup.xml',
            'hds_cs_getstoragearray_ldev': 'GetStorageArray_subtarget_ldev.xml',
            'hds_cs_getstoragearray_pdev': 'GetStorageArray_subtarget_pdev.xml',
            'hds_cs_getstoragearray_replicationinfo': 'GetStorageArray_subtarget_replicationinfo.xml',
            'hds_cs_getstoragearray_hoststoragedomain_hsdsubinfo_path_wwn': 'GetStorageArray_subtarget_hoststoragedomain_hsdsubinfo_path_wwn.xml',
            'hds_cs_getstoragearray_portcontroller': 'GetStorageArray_subtarget_portcontroller.xml',
            'hds_cs_getstoragearray_component': 'GetStorageArray_subtarget_component.xml',
        }

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
        # Capture the calling method's name and use that to correlate to the schema
        # and the custom xml information
        # ------------------------------------------------------------------------------
        caller = inspect.stack()[1][3]
        xml_schema = getattr(self.xml_schema, caller)

        # ------------------------------------------------------------------------------
        # Log execution
        # ------------------------------------------------------------------------------
        self.logger.info('Collecting %s for %s' % (caller, serial))

        # ------------------------------------------------------------------------------
        # Read entire file
        # ------------------------------------------------------------------------------
        with open(self.directory + '/' + str(serial) + '/' + self.custom_command[caller], 'r') as content_file:
            xml = content_file.read()

        # ------------------------------------------------------------------------------
        # Parse the XML as an initial_response subject to processing
        # ------------------------------------------------------------------------------
        try:
            initial_response = xmldataset.parse_using_profile(xml, xml_schema, process=self.xml_process)
        except Exception as e:
            print("Error - xml parsing exception - %s" % e)
            raise SystemExit

        # ------------------------------------------------------------------------------
        # Return response
        # ------------------------------------------------------------------------------
        return initial_response
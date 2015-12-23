# ------------------------------------------------------------------------------
# Built-in Imports
# ------------------------------------------------------------------------------
import yaml  # @UnresolvedImport
import codecs  # @UnresolvedImport
import logging
from collections import OrderedDict

# ------------------------------------------------------------------------------
# Internal Imports
# ------------------------------------------------------------------------------
from storageninja.utilities.prettyprint import pf

# ------------------------------------------------------------------------------
# Ordered yaml loader courtesy of
# http://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
# ------------------------------------------------------------------------------
def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def load_configuration_file(filename=None, filetype='yaml'):

    # ------------------------------------------------------------------------------
    # Configure logging
    # ------------------------------------------------------------------------------
    logger = logging.getLogger(__name__)

    # ------------------------------------------------------------------------------
    # Load the configuration file
    # ------------------------------------------------------------------------------
    configuration_file_handler = None
    try:
        # ------------------------------------------------------------------------------
        # Load the configuration file
        #
        # codecs.open used as opposed to open to allow utf-8 parsing
        # ------------------------------------------------------------------------------
        configuration_file_handler = codecs.open(filename, 'r', 'utf-8')
    except Exception as error:
        raise Exception("Failed to open %s: %s" % (filename, error))

    if filetype == 'yaml':
        # ------------------------------------------------------------------------------
        # Parse the configuration with yaml
        # ------------------------------------------------------------------------------
        configuration = None
        try:

            # Capture the configuration file text
            configuration_file_text = configuration_file_handler.read()

            # Capture a raw configuration for logging purposes
            configuration_raw = yaml.load(configuration_file_text)
            logger.debug('Loaded the following configuration - \n%s' % pf(configuration_raw))

            # Capture an ordered configuration
            configuration = ordered_load(configuration_file_text, yaml.SafeLoader)

        except Exception as error:
            raise Exception("Failed to parse %s: %s" % (filename, error))

        return configuration

    else:
        raise Exception("Yaml is only supported option")

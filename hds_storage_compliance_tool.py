"""Storage Compliance Tool"""

# ------------------------------------------------------------------------------
# Compatibility Imports
# ------------------------------------------------------------------------------
from __future__ import absolute_import

# ------------------------------------------------------------------------------
# Builtin Imports
# ------------------------------------------------------------------------------
import sys
import logging

# ------------------------------------------------------------------------------
# Internal Imports
# ------------------------------------------------------------------------------
from storageninja.common.any import standardise_wwn, true_or_false
from storageninja.common.hds import extract_portname, remove_subversion, create_pdevid, create_displayDevNum, create_displayPvolDevNum, create_displaySvolDevNum, set_rep_status
from storageninja.database.instance.wrapper import Database
from storageninja.database.relay import Relay
from storageninja.utilities.config import load_configuration_file
from storageninja.utilities.custom_logging import setup_logging
from storageninja.utilities.prettyprint import pf
from storageninja.utilities.globalshared import globalshared
import storageninja.collectors.hds_cs_cli
import storageninja.collectors.hds_cs_cli_offline
import storageninja.collectors.hds_cs_serviceport
# ------------------------------------------------------------------------------
# When storageninja.database.schema.hds_cs is imported, the classes within
# inherit a shared Base class, providing details of the necessary schema.
# 
# Subsequently, the same Base class is used within the Database class, thus
# providing the necessary information for creating and dropping tables
# ------------------------------------------------------------------------------
import storageninja.database.schema.hds_cs
import storageninja.xml.schema.hds_cs_cli
import storageninja.xml.schema.hds_cs_serviceport

# ------------------------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------------------------
def main():

    # ------------------------------------------------------------------------------
    # Setup custom logging
    # ------------------------------------------------------------------------------
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': '%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            },
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'colored',
                'stream': 'ext://sys.stderr'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': True
            },
            # We don't want to see messages from requests.packages.urllib3.connectionpool unless
            # there is a problem
            'requests.packages.urllib3.connectionpool': {
                'handlers': ['default'],
                'level': 'WARN',
                'propagate': True
            },
        }
    }

    # ------------------------------------------------------------------------------
    # Setup logging and configure a logger
    # ------------------------------------------------------------------------------
    setup_logging(level='DEBUG', config=logging_config)    # Set this back to INFO when live!
    logger = logging.getLogger('storage_compliance_tool')
    logger.info('Starting Storage Compliance Tool')

    # ------------------------------------------------------------------------------
    # Load the configuration file
    # ------------------------------------------------------------------------------
    try:
        logger.debug('Attempting to load configuration file hds_storage_compliance_tool.config')
        configuration = load_configuration_file(filename='hds_storage_compliance_tool.config', filetype='yaml')
        logger.debug('Successfully loaded configuration file hds_storage_compliance_tool.config')
    except Exception as e:
        logger.error('Failed to load configuration file hds_storage_compliance_tool.config - %s' % e)
        raise SystemExit

    # ------------------------------------------------------------------------------
    # Create an internal database instance, use an override value if provided 
    # or otherwise use sqlite memory
    # ------------------------------------------------------------------------------
    logger.debug('Setting up internal database')
    try:
        internal_database_string = configuration['__internal__']['internal_database_string']
        logger.debug(
            'Using internal_database_string override - %s' %
            configuration['__internal__']['internal_database_string'])
    except:
        internal_database_string = 'sqlite:///:memory:'
        logger.debug('Using internal_database_string - %s' % internal_database_string)
    internal_database = Database(dbname=internal_database_string)

    # ------------------------------------------------------------------------------
    # Create a database list to pass to the relay
    # ------------------------------------------------------------------------------
    databases = [internal_database]

    # ------------------------------------------------------------------------------
    # Create a database relay and use the databases list
    # ------------------------------------------------------------------------------
    logger.debug('Attempting to create a database relay')
    try:
        db_relay = Relay(databases=databases, schema=storageninja.database.schema.hds_cs)
        logger.debug('Successfully create database relay')
    except Exception as e:
        logger.error('Failed to create database relay')
        raise SystemExit

    # ------------------------------------------------------------------------------
    # Add optional database stores where applicable
    # ------------------------------------------------------------------------------
    try:
        if '__internal__' in configuration:
            if 'other_database_strings' in configuration['__internal__']:
                for database_string in configuration['__internal__']['other_database_strings']:
                    logger.debug('Setting up other_database - %s' % database_string)
                    db_object = Database(dbname=database_string)
                    databases.append(db_object)
                    logger.debug(
                        'Successfully configured other_database and added to database relay - %s' %
                        database_string)
    except Exception as e:
        logger.error('Failed to configure other_database - %s' % e)
        raise SystemExit

    # ------------------------------------------------------------------------------
    # Recreate tables in all databases ( see comments on Base in header )
    # ------------------------------------------------------------------------------
    logger.debug('Attempting to refresh tables in all databases')
    try:
        for database in databases:
            database.drop_tables()
            database.create_tables()
            logger.debug('Refreshed database store')
        logger.debug('Successfully refreshed tables in all databases')
    except Exception as e:
        logger.error('Failed to refresh tables in all databases - %s' % e)
        raise SystemExit

    # ------------------------------------------------------------------------------
    # Process collectors as per the configuration file
    # ------------------------------------------------------------------------------
    if 'collectors' in configuration:
        logger.debug('Processing collectors')

        # ------------------------------------------------------------------------------
        # Configure Store for HDS Collectors
        # ------------------------------------------------------------------------------
        hds_collectors = []

        # ------------------------------------------------------------------------------
        # Create a process definition for specific handling, these methods are used
        # by xmldataset to perform manipulation of the HDS data for consistency purposes
        # ------------------------------------------------------------------------------
        hds_cs_serviceport_process_definition = {'standardise_wwn': standardise_wwn,
                                                 'extract_portname': extract_portname,
                                                 'create_displayDevNum': create_displayDevNum,
                                                 'true_or_false': true_or_false,
                                                 'create_pdevid': create_pdevid,
                                                 'create_displayPvolDevNum': create_displayPvolDevNum,
                                                 'create_displaySvolDevNum': create_displaySvolDevNum,
                                                 'set_rep_status': set_rep_status,
                                                 'remove_subversion': remove_subversion}

        # ------------------------------------------------------------------------------
        # Process the configuration file and create an instance object for all required
        # collectors, at the moment this consists of hds_cs_cli ( Generic Command Suite
        # Command Line ), hds_cs_serviceport ( HTTP requests to the Command Suite 
        # serviceport on 2001 ) and hds_cs_cli_offline ( Generic Command Suite Command
        # Line captured to XML output files and logically stored in a directory 
        # structure.  Instances are polymorphic and accept the same parameters once
        # created as an object
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        # Process each hds_cs_cli collector
        # ------------------------------------------------------------------------------
        if 'hds_cs_cli' in configuration['collectors']:
            for instance in configuration['collectors']['hds_cs_cli']:
                logger.debug('Processing hds_cs_cli collectors')

                # ------------------------------------------------------------------------------
                # Create a collection object
                # ------------------------------------------------------------------------------
                try:
                    logger.debug('Attempting to create a storageninja.collectors.hds_cs_cli object')
                    collector = storageninja.collectors.hds_cs_cli.Instance(
                        xml_schema=storageninja.xml.schema.hds_cs_cli,
                        xml_process=hds_cs_serviceport_process_definition,
                        hicommand_binary=instance['hicommand_binary'],
                        server=instance['server'],
                        username=instance['username'],
                        password=instance['password'],
                    )
                    logger.debug('Successfully created a storageninja.collectors.hds_cs_cli object')
                except Exception as e:
                    logger.error('Failed to create a storageninja.collectors.hds_cs_cli object - %s' % e)
                    raise SystemExit

                # ------------------------------------------------------------------------------
                # Store the serial numbers associated with this object
                # ------------------------------------------------------------------------------
                collector.serial_numbers = instance['serial_numbers']
                logger.debug('Associated serial numbers with hds_cs_cli collection object - \n%s' %
                             pf(instance['serial_numbers']))

                # ------------------------------------------------------------------------------
                # Store the collector object
                # ------------------------------------------------------------------------------
                hds_collectors.append(collector)
                logger.debug('Stored hds_cs_cli collection object - \n%s' % pf(instance['serial_numbers']))

        # ------------------------------------------------------------------------------
        # Process each hds_cs_serviceport collector
        # ------------------------------------------------------------------------------
        if 'hds_cs_serviceport' in configuration['collectors']:
            for instance in configuration['collectors']['hds_cs_serviceport']:
                logger.debug('Processing hds_cs_serviceport collectors')

                # ------------------------------------------------------------------------------
                # Create a collection object
                # ------------------------------------------------------------------------------
                try:
                    logger.debug('Attempting to create a storageninja.collectors.hds_cs_serviceport object')
                    collector = storageninja.collectors.hds_cs_serviceport.Instance(
                        xml_schema=storageninja.xml.schema.hds_cs_serviceport,
                        xml_process=hds_cs_serviceport_process_definition,
                        api=instance['api'],
                        server=instance['server'],
                        username=instance['username'],
                        password=instance['password'],
                    )
                    logger.debug('Successfully created a storageninja.collectors.hds_cs_serviceport object')
                except Exception as e:
                    logger.error('Failed to create a storageninja.collectors.hds_cs_serviceport object - %s' % e)
                    raise SystemExit

                # ------------------------------------------------------------------------------
                # Store the serial numbers associated with this object
                # ------------------------------------------------------------------------------
                collector.serial_numbers = instance['serial_numbers']
                logger.debug('Associated serial numbers with hds_cs_serviceport collection object - \n%s' %
                             pf(instance['serial_numbers']))

                # ------------------------------------------------------------------------------
                # Store the collector object
                # ------------------------------------------------------------------------------
                hds_collectors.append(collector)
                logger.debug('Stored hds_cs_cli collection object - \n%s' % pf(instance['serial_numbers']))

        # ------------------------------------------------------------------------------
        # Process each hds_cs_cli_offline collector ( Used for evaluation only )
        # ------------------------------------------------------------------------------
        if 'hds_cs_cli_offline' in configuration['collectors']:
            for instance in configuration['collectors']['hds_cs_cli_offline']:
                logger.debug('Processing hds_cs_cli_offline collectors')

                # ------------------------------------------------------------------------------
                # Create a collection object
                # ------------------------------------------------------------------------------
                try:
                    logger.debug('Attempting to create a storageninja.collectors.hds_cs_cli_offline object')
                    collector = storageninja.collectors.hds_cs_cli_offline.Instance(
                        xml_schema=storageninja.xml.schema.hds_cs_cli,
                        xml_process=hds_cs_serviceport_process_definition,
                        directory=instance['directory']
                    )
                    logger.debug('Successfully created a storageninja.collectors.hds_cs_cli_offline object')
                except Exception as e:
                    logger.error('Failed to create a storageninja.collectors.hds_cs_cli_offline object - %s' % e)
                    raise SystemExit

                # ------------------------------------------------------------------------------
                # Store the serial numbers associated with this object
                # ------------------------------------------------------------------------------
                collector.serial_numbers = instance['serial_numbers']
                logger.debug('Associated serial numbers with hds_cs_cli collection object - \n%s' %
                             pf(instance['serial_numbers']))

                # ------------------------------------------------------------------------------
                # Store the collector object
                # ------------------------------------------------------------------------------
                hds_collectors.append(collector)
                logger.debug('Stored hds_cs_cli collection object - \n%s' % pf(instance['serial_numbers']))

        # ------------------------------------------------------------------------------
        # Process each hds_collector object and collect
        # ------------------------------------------------------------------------------
        for instance in hds_collectors:

            # ------------------------------------------------------------------------------
            # Collect Data for HDS serials using the database relay
            # so that all outputs receive the same information
            # ------------------------------------------------------------------------------
            for serial in instance.serial_numbers:

                # ------------------------------------------------------------------------------
                # Collect All Information
                # ------------------------------------------------------------------------------
                db_relay.insert_dict(instance.hds_cs_getstoragearray(serial=serial))
                db_relay.insert_dict(instance.hds_cs_getstoragearray_port(serial=serial))
                db_relay.insert_dict(instance.hds_cs_getstoragearray_pool(serial=serial))
                db_relay.insert_dict(instance.hds_cs_getstoragearray_arraygroup(serial=serial))
                db_relay.insert_dict(instance.hds_cs_getstoragearray_ldev(serial=serial))
                db_relay.insert_dict(instance.hds_cs_getstoragearray_pdev(serial=serial))
                db_relay.insert_dict(instance.hds_cs_getstoragearray_replicationinfo(serial=serial))
                db_relay.insert_dict(
                    instance.hds_cs_getstoragearray_hoststoragedomain_hsdsubinfo_path_wwn(
                        serial=serial))
                db_relay.insert_dict(instance.hds_cs_getstoragearray_portcontroller(serial=serial))
                db_relay.insert_dict(instance.hds_cs_getstoragearray_component(serial=serial))

    # ------------------------------------------------------------------------------
    # Create a holder for output objects.  An output object is a polymorphic object
    # that abides to a standard set of methods allowing the output to be changed
    # accordingly, i.e. Screen, HTML, Email, Text
    # ------------------------------------------------------------------------------
    outputs = []

    # ------------------------------------------------------------------------------
    # Create an output object for each output definition in the configuration file
    # ------------------------------------------------------------------------------
    for output in configuration['outputs']:

        # ------------------------------------------------------------------------------
        # Import the output module based on string
        # ------------------------------------------------------------------------------
        __import__('storageninja.outputs.' + output)
        output_module = sys.modules['storageninja.outputs.' + output]

        # ------------------------------------------------------------------------------
        # Process each output parameter
        # ------------------------------------------------------------------------------
        for output_entry in configuration['outputs'][output]:

            # ------------------------------------------------------------------------------
            # Create an object using the output module, passing the parameters
            # as init params
            # ------------------------------------------------------------------------------
            output_object = output_module.OutputClass(**output_entry)

            # ------------------------------------------------------------------------------
            # Add the output object to the outputs store
            # ------------------------------------------------------------------------------
            outputs.append(output_object)

    # ------------------------------------------------------------------------------
    # Process top level reports
    # ------------------------------------------------------------------------------
    for report_module_name in configuration['reports']:

        # ------------------------------------------------------------------------------
        # Import the report module based on the string name supplied in the 
        # configuration file
        # ------------------------------------------------------------------------------
        __import__('storageninja.reports.' + report_module_name)
        report_module = sys.modules['storageninja.reports.' + report_module_name]

        # ------------------------------------------------------------------------------
        # Process each report
        # ------------------------------------------------------------------------------
        for report_method_name in configuration['reports'][report_module_name]:
            logger.debug('Processing report - %s' % report_method_name)

            # ------------------------------------------------------------------------------
            # Capture method
            # ------------------------------------------------------------------------------
            report_method = getattr(report_module, report_method_name)

            # ------------------------------------------------------------------------------
            # Lookup the return data information for the method in question
            # from the report module, this is passed on to the output object to
            # provide hints for processing, for example this may be 'sqlalchemy_query'
            # ------------------------------------------------------------------------------
            data_information = report_module.return_information[report_method_name]

            # ------------------------------------------------------------------------------
            # Process each report entry
            # ------------------------------------------------------------------------------
            for report_entry in configuration['reports'][report_module_name][report_method_name]:

                # ------------------------------------------------------------------------------
                # Pass the report entry to the report_method, passing parameters ( un-necessary
                # parameters are ignored by report_method under kwargs )
                # ------------------------------------------------------------------------------
                report_output = report_method(session=internal_database.DBSession, **report_entry)

                # ------------------------------------------------------------------------------
                # Add report_output to each output object
                # ------------------------------------------------------------------------------
                for output in outputs:
                    output.add_entry(
                        data=report_output,
                        data_information=data_information,
                        report_parameters=report_entry)

    # ------------------------------------------------------------------------------
    # Call the corresponding dispatch method for each output
    # ------------------------------------------------------------------------------
    for output in outputs:
        output.dispatch()

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

#!/usr/local/bin/python2.7
# encoding: utf-8

import sys
import os
import shelve
import gzi

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # try:
    # Setup argument parser
    parser = ArgumentParser(add_help=False)
    parser.add_argument("-h", "--hicommand", dest="hicommand", required=True, help="HiCommand Binary Path")
    parser.add_argument("-f", "--filename", dest="filename", required=True, help="Output Filename")

    # Process arguments
    args = vars(parser.parse_args())

    commands = {
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

    # Create an offline store
    d = shelve.open(args['filename'])

    for command in commands.keys():
        print("Executing " + args['hicommand'] + " " + commands[command])
        d[command] = os.popen(args['hicommand'] + " " + commands[command]).read()

    # Close shelve
    d.close()

    f_in = open(args['filename'], 'rb')
    f_out = gzip.open(args['filename'] + '.gz', 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()

if __name__ == "__main__":
    sys.exit(main())

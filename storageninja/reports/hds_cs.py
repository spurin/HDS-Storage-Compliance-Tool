# ------------------------------------------------------------------------------
# Builtin Imports
# ------------------------------------------------------------------------------
from sqlalchemy import and_, or_, func
from sqlalchemy.sql import label

# ------------------------------------------------------------------------------
# Internal Imports
# ------------------------------------------------------------------------------
from storageninja.database.schema.hds_cs import HDS_CS_STORAGEARRAY, HDS_CS_COMPONENT, HDS_CS_HSD, HDS_CS_HSD_PATH, HDS_CS_LDEV, HDS_CS_REPLICATIONINFO

# ------------------------------------------------------------------------------
# Return information lookup table
# ------------------------------------------------------------------------------
return_information = {
    'hds_cs_storagearray': {'type': 'sqlalchemy_query'},
    'hds_cs_invalid_components': {'type': 'sqlalchemy_query'},
    'hds_cs_vvol_pool_clpr': {'type': 'sqlalchemy_query'},
    'hds_cs_empty_hsd': {'type': 'sqlalchemy_query'},
    'hds_cs_unassigned_vvol': {'type': 'sqlalchemy_query'},
    'hds_cs_unbound_vvol': {'type': 'sqlalchemy_query'},
    'hsd_cs_hsd_incorrect_hostmode': {'type': 'sqlalchemy_query'},
    'hsd_cs_non_paired_rep': {'type': 'sqlalchemy_query'},
    'hsd_cs_incorrect_rep_path': {'type': 'sqlalchemy_query'},
    'hsd_cs_rep_different_source_dest': {'type': 'sqlalchemy_query'},
}


def hds_cs_storagearray(session=None, serialNumber='%', **kwargs):
    return session.query(label('Array Name', HDS_CS_STORAGEARRAY.arrayName),
                         label('Serial Number', HDS_CS_STORAGEARRAY.serialNumber),
                         label('Array Type', HDS_CS_STORAGEARRAY.arrayType),
                         label('Cache MB', HDS_CS_STORAGEARRAY.cacheInMB),
                         label('Controller Version', HDS_CS_STORAGEARRAY.controllerVersion))\
        .filter(HDS_CS_STORAGEARRAY.serialNumber.like(serialNumber)).all()


def hds_cs_invalid_components(session=None, serialNumber='%', **kwargs):
    return session.query(label('Array Name', HDS_CS_STORAGEARRAY.arrayName),
                         label('Serial Number', HDS_CS_COMPONENT.serialNumber),
                         label('Component Name', HDS_CS_COMPONENT.componentName),
                         label('Description', HDS_CS_COMPONENT.description),
                         label('Component Value', HDS_CS_COMPONENT.value))\
        .outerjoin(HDS_CS_COMPONENT, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_COMPONENT.serialNumber)\
        .filter(and_(HDS_CS_STORAGEARRAY.serialNumber.like(serialNumber),
                     HDS_CS_COMPONENT.description != 'Normal')).all()


def hds_cs_empty_hsd(session=None, serialNumber='%', **kwargs):

    # ------------------------------------------------------------------------------
    # Subquery HSD's to Count
    # Ignore DomainID 0 as this relates to the default domainID on all ports
    # ------------------------------------------------------------------------------
    subq = session.query(HDS_CS_STORAGEARRAY.arrayName,
                         HDS_CS_HSD.serialNumber,
                         HDS_CS_HSD.nickname,
                         HDS_CS_HSD.portName,
                         label('customcount', func.count(HDS_CS_HSD_PATH.displayDevNum))).\
        outerjoin(HDS_CS_HSD, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_HSD.serialNumber).\
        outerjoin(HDS_CS_HSD_PATH,
                  and_(HDS_CS_HSD.serialNumber == HDS_CS_HSD_PATH.serialNumber,
                       HDS_CS_HSD.portID == HDS_CS_HSD_PATH.portID,
                       HDS_CS_HSD.domainID     == HDS_CS_HSD_PATH.domainID)).\
        filter(HDS_CS_HSD.domainID != '0').\
        group_by(HDS_CS_STORAGEARRAY.arrayName, HDS_CS_HSD.serialNumber, HDS_CS_HSD.nickname, HDS_CS_HSD.portName).\
        subquery()

    # ------------------------------------------------------------------------------
    # Return where the number of devices is 0
    # ------------------------------------------------------------------------------
    return session.query(subq.c.arrayName,
                         subq.c.serialNumber,
                         subq.c.nickname,
                         subq.c.portName).\
        filter(subq.c.customcount == '0').\
        order_by(subq.c.arrayName,
                 subq.c.nickname,
                 subq.c.portName).\
        all()

def hds_cs_vvol_pool_clpr(session=None, serialNumber='%', dpPoolID=None, clprNumber=None, **kwargs):

    return session.query(label('Array Name', HDS_CS_STORAGEARRAY.arrayName),
                         label('Serial Number', HDS_CS_LDEV.serialNumber),
                         label('Pool ID', HDS_CS_LDEV.dpPoolID),
                         label('CLPR Number', HDS_CS_LDEV.clprNumber),
                         label('Label', HDS_CS_LDEV.label),
                         label('LDEV', HDS_CS_LDEV.displayDevNum)).\
        outerjoin(HDS_CS_LDEV, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_LDEV.serialNumber).\
        filter(and_(HDS_CS_STORAGEARRAY.serialNumber.like(serialNumber),
                    HDS_CS_LDEV.dpType == 0,
                    HDS_CS_LDEV.dpPoolID == dpPoolID,
                    HDS_CS_LDEV.clprNumber != clprNumber)).all()


def hsd_cs_non_paired_rep(session=None, serialNumber='%', **kwargs):

    from sqlalchemy.orm import aliased
    HDS_CS_STORAGEARRAY_2 = aliased(HDS_CS_STORAGEARRAY)

    return session.query(label('PVol Array Name', HDS_CS_STORAGEARRAY.arrayName),
                         label('PVol Serial Number', HDS_CS_REPLICATIONINFO.pvolSerialNumber),
                         label('PVol LDEV', HDS_CS_REPLICATIONINFO.displayPvolDevNum),
                         label('PVol LDEV Label', HDS_CS_LDEV.label),
                         label('SVol Array Name', HDS_CS_STORAGEARRAY_2.arrayName),
                         label('SVol Serial Number', HDS_CS_REPLICATIONINFO.svolSerialNumber),
                         label('SVol LDEV', HDS_CS_REPLICATIONINFO.displaySvolDevNum),
                         label('Replication Type', HDS_CS_REPLICATIONINFO.replicationFunction),
                         label('Status', HDS_CS_REPLICATIONINFO.status)).\
        outerjoin(HDS_CS_REPLICATIONINFO, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_REPLICATIONINFO.pvolSerialNumber).\
        outerjoin(HDS_CS_LDEV, and_(HDS_CS_LDEV.serialNumber == HDS_CS_REPLICATIONINFO.pvolSerialNumber,
                                    HDS_CS_LDEV.displayDevNum == HDS_CS_REPLICATIONINFO.displayPvolDevNum)).\
        outerjoin(HDS_CS_STORAGEARRAY_2, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_REPLICATIONINFO.svolSerialNumber).\
        filter(and_(HDS_CS_REPLICATIONINFO.pvolSerialNumber.like(serialNumber),
                    HDS_CS_REPLICATIONINFO.status != 'Pair',
                    or_(HDS_CS_REPLICATIONINFO.replicationFunction == 'TrueCopySync',
                        HDS_CS_REPLICATIONINFO.replicationFunction == 'UniversalReplicator'))).all()

def hsd_cs_incorrect_rep_path(
        session=None,
        serialNumber='%',
        replicationFunction=None,
        remotePathGroupID=None,
        **kwargs):

    from sqlalchemy.orm import aliased
    HDS_CS_STORAGEARRAY_2 = aliased(HDS_CS_STORAGEARRAY)

    return session.query(label('PVol Array Name', HDS_CS_STORAGEARRAY.arrayName),
                         label('PVol Serial Number', HDS_CS_REPLICATIONINFO.pvolSerialNumber),
                         label('PVol LDEV', HDS_CS_REPLICATIONINFO.displayPvolDevNum),
                         label('PVol LDEV Label', HDS_CS_LDEV.label),
                         label('SVol Array Name', HDS_CS_STORAGEARRAY_2.arrayName),
                         label('SVol Serial Number', HDS_CS_REPLICATIONINFO.svolSerialNumber),
                         label('SVol LDEV', HDS_CS_REPLICATIONINFO.displaySvolDevNum),
                         label('Replication Type', HDS_CS_REPLICATIONINFO.replicationFunction),
                         label('Remote Path Group', HDS_CS_REPLICATIONINFO.remotePathGroupID),
                         label('Status', HDS_CS_REPLICATIONINFO.status)).\
        outerjoin(HDS_CS_REPLICATIONINFO, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_REPLICATIONINFO.pvolSerialNumber).\
        outerjoin(HDS_CS_LDEV, and_(HDS_CS_LDEV.serialNumber == HDS_CS_REPLICATIONINFO.pvolSerialNumber,
                                    HDS_CS_LDEV.displayDevNum == HDS_CS_REPLICATIONINFO.displayPvolDevNum)).\
        outerjoin(HDS_CS_STORAGEARRAY_2, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_REPLICATIONINFO.svolSerialNumber).\
        filter(and_(HDS_CS_STORAGEARRAY.serialNumber.like(serialNumber),
                    HDS_CS_REPLICATIONINFO.replicationFunction.like(replicationFunction),
                    HDS_CS_REPLICATIONINFO.remotePathGroupID.like(remotePathGroupID))).all()

def hsd_cs_rep_different_source_dest(session=None, serialNumber='%', replicationFunction=None, **kwargs):

    from sqlalchemy.orm import aliased
    HDS_CS_STORAGEARRAY_2 = aliased(HDS_CS_STORAGEARRAY)

    return session.query(label('PVol Array Name', HDS_CS_STORAGEARRAY.arrayName),
                         label('PVol Serial Number', HDS_CS_REPLICATIONINFO.pvolSerialNumber),
                         label('PVol LDEV', HDS_CS_REPLICATIONINFO.displayPvolDevNum),
                         label('SVol Array Name', HDS_CS_STORAGEARRAY_2.arrayName),
                         label('SVol Serial Number', HDS_CS_REPLICATIONINFO.svolSerialNumber),
                         label('SVol LDEV', HDS_CS_REPLICATIONINFO.displaySvolDevNum),
                         label('Replication Type', HDS_CS_REPLICATIONINFO.replicationFunction),
                         label('Remote Path Group', HDS_CS_REPLICATIONINFO.remotePathGroupID),
                         label('Status', HDS_CS_REPLICATIONINFO.status)).\
        outerjoin(HDS_CS_REPLICATIONINFO, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_REPLICATIONINFO.pvolSerialNumber).\
        outerjoin(HDS_CS_STORAGEARRAY_2, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_REPLICATIONINFO.svolSerialNumber).\
        filter(and_(HDS_CS_STORAGEARRAY.serialNumber.like(serialNumber),
                    HDS_CS_REPLICATIONINFO.pvolDevNum != HDS_CS_REPLICATIONINFO.svolDevNum,
                    HDS_CS_REPLICATIONINFO.replicationFunction.like(replicationFunction))).all()


def hsd_cs_hsd_incorrect_hostmode(
        session=None,
        serialNumber='%',
        hostMode=None,
        hostModeOption=None,
        nickname='%',
        **kwargs):

    return session.query(label('Array Name', HDS_CS_STORAGEARRAY.arrayName),
                         label('Host Storage Domain', HDS_CS_HSD.nickname),
                         label('Port Name', HDS_CS_HSD.portName),
                         label('Host Mode', HDS_CS_HSD.hostMode),
                         label('Host Mode Options', HDS_CS_HSD.hostModeOption)).\
        outerjoin(HDS_CS_HSD, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_HSD.serialNumber).\
        filter(and_(HDS_CS_HSD.serialNumber.like(serialNumber),
                    HDS_CS_HSD.nickname.like(nickname),
                    or_(HDS_CS_HSD.hostMode != hostMode,
                        HDS_CS_HSD.hostModeOption != hostModeOption))).all()


def hds_cs_unassigned_vvol(session=None, serialNumber='%', dpPoolID='%', **kwargs):

    output = session.query(label('Array Name', HDS_CS_STORAGEARRAY.arrayName),
                           label('Serial Number', HDS_CS_LDEV.serialNumber),
                           label('Pool ID', HDS_CS_LDEV.dpPoolID),
                           label('Size GB', HDS_CS_LDEV.sizeInKB),
                           label('Label', HDS_CS_LDEV.label),
                           label('LDEV', HDS_CS_LDEV.displayDevNum)).\
        outerjoin(HDS_CS_LDEV, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_LDEV.serialNumber).\
        group_by(HDS_CS_STORAGEARRAY.arrayName,
                 HDS_CS_LDEV.serialNumber,
                 HDS_CS_LDEV.dpPoolID,
                 HDS_CS_LDEV.displayDevNum).\
        filter(and_(HDS_CS_STORAGEARRAY.serialNumber.like(serialNumber),
                    HDS_CS_LDEV.dpType == 0,
                    HDS_CS_LDEV.path == 'false',
                    HDS_CS_LDEV.dpPoolID.like(dpPoolID))).all()

    # Manipulate the data, changing KB to GB
    for entry in output:
        entry.__dict__['Size GB'] = round(int(entry.__dict__['Size GB']) / 1024 / 1024, 2)

    # Return the output
    return output


def hds_cs_unbound_vvol(session=None, serialNumber='%', **kwargs):

    output = session.query(label('Array Name', HDS_CS_STORAGEARRAY.arrayName),
                           label('Serial Number', HDS_CS_LDEV.serialNumber),
                           label('Size GB', HDS_CS_LDEV.sizeInKB),
                           label('Label', HDS_CS_LDEV.label),
                           label('LDEV', HDS_CS_LDEV.displayDevNum)).\
        outerjoin(HDS_CS_LDEV, HDS_CS_STORAGEARRAY.serialNumber == HDS_CS_LDEV.serialNumber).\
        filter(and_(HDS_CS_STORAGEARRAY.serialNumber.like(serialNumber),
                    HDS_CS_LDEV.dpType == 0,
                    HDS_CS_LDEV.path == 'false',
                    HDS_CS_LDEV.dpPoolID == '-1')).all()

    # Manipulate the data, changing KB to GB
    for entry in output:
        entry.__dict__['Size GB'] = round(int(entry.__dict__['Size GB']) / 1024 / 1024, 2)

    # Return the output
    return output

# ------------------------------------------------------------------------------
# Builtin Imports
# ------------------------------------------------------------------------------
from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import Index

# ------------------------------------------------------------------------------
# Internal Imports
# ------------------------------------------------------------------------------
from storageninja.database.schema.shared_base import Base


class InternalFunctionality():

    # ------------------------------------------------------------------------------
    # http://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    # ... used as opposed to object__dict__ as we are not interested in sqlalchemy
    #     internal structures
    # ------------------------------------------------------------------------------
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class HDS_CS_STORAGEARRAY(Base, InternalFunctionality):
    __tablename__ = "hds_cs_storagearray"
    id = Column(Integer, primary_key=True)
    command_suite_version = Column(String(255))
    arrayName = Column(String(255))
    agentVersion = Column(String(255))
    allocatedCapacityInGB = Column(String(255))
    allocatedCapacityInKB = Column(String(255))
    arrayFamily = Column(String(255))
    arrayType = Column(String(255))
    autoFormatLU = Column(String(255))
    cacheInMB = Column(String(255))
    capacityInGB = Column(String(255))
    capacityInKB = Column(String(255))
    configUpdateStatus = Column(String(255))
    controllerVersion = Column(String(255))
    description = Column(String(255))
    displayArrayFamily = Column(String(255))
    displayArrayType = Column(String(255))
    distributedMode = Column(String(255))
    freeCapacityInGB = Column(String(255))
    freeCapacityInKB = Column(String(255))
    hihsmCapacityInGB = Column(String(255))
    hihsmCapacityInKB = Column(String(255))
    imAllocatedCapacity = Column(String(255))
    imFreeCapacity = Column(String(255))
    imHiHsmCapacity = Column(String(255))
    imOnDemandCapacity = Column(String(255))
    imTotalCapacity = Column(String(255))
    largestFreeSpaceInGB = Column(String(255))
    largestFreeSpaceInKB = Column(String(255))
    lastRefreshed = Column(String(255))
    mfAllocatedCapacity = Column(String(255))
    mfHiHsmCapacity = Column(String(255))
    mfOnDemandCapacity = Column(String(255))
    mfTotalCapacity = Column(String(255))
    mfUnallocatedCapacity = Column(String(255))
    multipathSupport = Column(String(255))
    numberOfAllocatedLUs = Column(String(255))
    numberOfAllocatedMfLDEVs = Column(String(255))
    numberOfControllers = Column(String(255))
    numberOfImAllocatedLUs = Column(String(255))
    numberOfImReservedLUs = Column(String(255))
    numberOfImUnallocatedLUs = Column(String(255))
    numberOfLUs = Column(String(255))
    numberOfMfLDEVs = Column(String(255))
    numberOfOpenAllocatedLUs = Column(String(255))
    numberOfOpenReservedLUs = Column(String(255))
    numberOfOpenUnallocatedLUs = Column(String(255))
    numberOfReservedLUs = Column(String(255))
    numberOfSpareDrives = Column(String(255))
    numberOfUnallocatedLUs = Column(String(255))
    numberOfUnallocatedMfLDEVs = Column(String(255))
    objectID = Column(String(255))
    onDemandCapacityInGB = Column(String(255))
    onDemandCapacityInKB = Column(String(255))
    openAllocatedActualCapacity = Column(String(255))
    openAllocatedCapacity = Column(String(255))
    openFreeCapacity = Column(String(255))
    openHiHsmCapacity = Column(String(255))
    openOnDemandCapacity = Column(String(255))
    openReservedActualCapacity = Column(String(255))
    openReservedCapacity = Column(String(255))
    openTotalCapacity = Column(String(255))
    openUnallocatedActualCapacity = Column(String(255))
    openUnallocatedCapacity = Column(String(255))
    productCode = Column(String(255))
    productName = Column(String(255))
    securityStatus = Column(String(255))
    sequenceNumber = Column(String(255))
    serialNumber = Column(String(255), index=True)
    sharedMemoryInMB = Column(String(255))
    slprStatus = Column(String(255))
    statusOfDBInconsistency = Column(String(255))
    totalFreeSpaceInGB = Column(String(255))
    totalFreeSpaceInKB = Column(String(255))

Index('hds_cs_storagearray.serialNumber', HDS_CS_STORAGEARRAY.serialNumber)


class HDS_CS_HSD_PATH(Base, InternalFunctionality):
    __tablename__ = "hds_cs_hsd_path"
    id = Column(Integer, primary_key=True)
    lun = Column(String(255))
    scsiID = Column(String(255))
    portName = Column(String(255))
    serialNumber = Column(String(255))
    portID = Column(String(255))
    displayDevNum = Column(String(255))
    devNum = Column(String(255))
    wwnSecurityValidity = Column(String(255))
    objectID = Column(String(255))
    domainID = Column(String(255))

Index(
    'hds_cs_hsd_path.serialNumber_portID_domainID',
    HDS_CS_HSD_PATH.serialNumber,
    HDS_CS_HSD_PATH.portID,
    HDS_CS_HSD_PATH.domainID)


class HDS_CS_ARRAYGROUP(Base, InternalFunctionality):
    __tablename__ = "hds_cs_arraygroup"
    id = Column(Integer, primary_key=True)
    diskType = Column(String(255))
    mfAllocatedCapacity = Column(String(255))
    substance = Column(String(255))
    mfTotalCapacity = Column(String(255))
    number = Column(String(255))
    totalFreeSpace = Column(String(255))
    openHiHsmCapacity = Column(String(255))
    diskSizeInKB = Column(String(255))
    openAllocatedActualCapacity = Column(String(255))
    openAllocatedCapacity = Column(String(255))
    mfUnallocatedCapacity = Column(String(255))
    encrypted = Column(String(255))
    raidType = Column(String(255))
    openOnDemandCapacity = Column(String(255))
    objectID = Column(String(255))
    largestFreeSpace = Column(String(255))
    freeCapacity = Column(String(255))
    protectionLevel = Column(String(255))
    controllerID = Column(String(255))
    dpPoolID = Column(String(255))
    imHiHsmCapacity = Column(String(255))
    imAllocatedCapacity = Column(String(255))
    mfHiHsmCapacity = Column(String(255))
    openTotalCapacity = Column(String(255))
    imFreeCapacity = Column(String(255))
    diskSize = Column(String(255))
    openFreeCapacity = Column(String(255))
    displayName = Column(String(255))
    imTotalCapacity = Column(String(255))
    volumeType = Column(String(255))
    allocatedCapacity = Column(String(255))
    slprNumber = Column(String(255))
    totalCapacity = Column(String(255))
    openUnallocatedActualCapacity = Column(String(255))
    chassis = Column(String(255))
    mfOnDemandCapacity = Column(String(255))
    hiHsmCapacity = Column(String(255))
    imOnDemandCapacity = Column(String(255))
    openUnallocatedCapacity = Column(String(255))
    onDemandCapacity = Column(String(255))
    openReservedActualCapacity = Column(String(255))
    clprNumber = Column(String(255))
    serialNumber = Column(String(255))
    openReservedCapacity = Column(String(255))


class HDS_CS_COMPONENT(Base, InternalFunctionality):
    __tablename__ = "hds_cs_component"
    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    componentName = Column(String(255))
    serialNumber = Column(String(255))
    value = Column(String(255))


class HDS_CS_HSD(Base, InternalFunctionality):
    __tablename__ = "hds_cs_hsd"
    id = Column(Integer, primary_key=True)
    hostMode2 = Column(String(255), nullable=True)
    hostMode = Column(String(255))
    displayName = Column(String(255))
    portID = Column(String(255))
    nickname = Column(String(255))
    serialNumber = Column(String(255), index=True)
    portName = Column(String(255))
    objectID = Column(String(255))
    domainType = Column(String(255))
    domainID = Column(String(255))
    hostModeOption = Column(String(255))

Index('hds_cs_hsd.serialNumber_portID_domainID', HDS_CS_HSD.serialNumber, HDS_CS_HSD.portID, HDS_CS_HSD.domainID)
Index(
    'hds_cs_hsd.serialNumber_nickname_hostMode_hostModeOption',
    HDS_CS_HSD.serialNumber,
    HDS_CS_HSD.nickname,
    HDS_CS_HSD.hostMode,
    HDS_CS_HSD.hostModeOption)


class HDS_CS_HSD_WWN(Base, InternalFunctionality):
    __tablename__ = "hds_cs_hsd_wwn"
    id = Column(Integer, primary_key=True)
    domainID = Column(String(255))
    serialNumber = Column(String(255))
    wwn = Column(String(255))
    nickname = Column(String(255))


class HDS_CS_LDEV(Base, InternalFunctionality):
    __tablename__ = "hds_cs_ldev"
    id = Column(Integer, primary_key=True)
    diskType = Column(String(255))
    mfUniversalReplicatorPoolID = Column(String(255))
    substance = Column(String(255))
    mfUniversalReplicatorVolumeType = Column(String(255))
    stripeSizeInKB = Column(String(255))
    raidType = Column(String(255))
    dpPoolID = Column(String(255))
    volumeType = Column(String(255))
    cacheResidencyMode = Column(String(255))
    devType = Column(String(255))
    volumeKind = Column(String(255))
    sizeInKB = Column(String(255))
    encrypted = Column(String(255))
    serialNumber = Column(String(255))
    threshold = Column(String(255))
    isComposite = Column(String(255))
    slotSizeInKB = Column(String(255))
    slprNumber = Column(String(255))
    objectID = Column(String(255))
    mfTrueCopyVolumeType = Column(String(255))
    status = Column(String(255))
    arrayGroup = Column(String(255))
    consumedSizeInKB = Column(String(255))
    devNum = Column(String(255))
    chassis = Column(String(255))
    isStandardLDEV = Column(String(255), index=True)
    dpTier1ConsumedCapacityInKB = Column(String(255))
    displayDevNum = Column(String(255))
    lba = Column(String(255))
    dpTier0ConsumedCapacityInKB = Column(String(255))
    systemDisk = Column(String(255))
    clprNumber = Column(String(255))
    dpType = Column(String(255))
    path = Column(String(255), index=True)
    mfShadowImageVolumeType = Column(String(255))
    cylinders = Column(String(255))
    guardMode = Column(String(255))
    onDemandDevice = Column(String(255))
    dpTier2ConsumedCapacityInKB = Column(String(255))
    label = Column(String(255))

Index('hds_cs_ldev.serialNumber_displayDevNum', HDS_CS_LDEV.serialNumber, HDS_CS_LDEV.displayDevNum)
Index(
    'hds_cs_ldev.serialNumber_dpType_dpPoolID_clprNumber',
    HDS_CS_LDEV.serialNumber,
    HDS_CS_LDEV.dpType,
    HDS_CS_LDEV.dpPoolID,
    HDS_CS_LDEV.clprNumber)


class HDS_CS_PDEV(Base, InternalFunctionality):
    __tablename__ = "hds_cs_pdev"
    id = Column(Integer, primary_key=True)
    diskType = Column(String(255))
    firmwareVersion = Column(String(255))
    model = Column(String(255))
    rpm = Column(String(255))
    densePosition = Column(String(255))
    denseNumber = Column(String(255))
    formFactor = Column(String(255))
    depth = Column(String(255))
    serialNumber = Column(String(255))
    role = Column(String(255))
    encrypted = Column(String(255))
    vendor = Column(String(255))
    diskModelSize = Column(String(255))
    objectID = Column(String(255))
    arrayGroup = Column(String(255))
    pdev_column = Column(String(255))
    pdevid = Column(String(255))
    chassis = Column(String(255))
    dkuType = Column(String(255))
    row = Column(String(255))
    capacityInKB = Column(String(255))


class HDS_CS_POOL(Base, InternalFunctionality):
    __tablename__ = "hds_cs_pool"
    id = Column(Integer, primary_key=True)
    combination = Column(String(255))
    diskType = Column(String(255))
    usageRate = Column(String(255))
    poolID = Column(String(255))
    capacityOfVVolsInKB = Column(String(255))
    monitoringMode = Column(String(255))
    capacityInKB = Column(String(255))
    freeCapacityInKB = Column(String(255))
    migrationInterval = Column(String(255))
    monitorStartTime = Column(String(255))
    status = Column(String(255))
    poolType = Column(String(255))
    poolFunction = Column(String(255))
    poolName = Column(String(255))
    serialNumber = Column(String(255))
    monitorEndTime = Column(String(255))
    numberOfPoolVols = Column(String(255))
    objectID = Column(String(255))
    overProvisioningLimit = Column(String(255))
    threshold = Column(String(255))
    rpm = Column(String(255))
    volAlertNotice = Column(String(255))
    numberOfVVols = Column(String(255))
    raidLevel = Column(String(255))
    threshold2 = Column(String(255))
    threshold2Mode = Column(String(255))
    overProvisioningPercent = Column(String(255))
    controllerID = Column(String(255))
    clprNumber = Column(String(255))
    overProvisioningWarning = Column(String(255))


class HDS_CS_PORT(Base, InternalFunctionality):
    __tablename__ = "hds_cs_port"
    id = Column(Integer, primary_key=True)
    portType = Column(String(255))
    portNumber = Column(String(255))
    lunSecurityEnabled = Column(String(255))
    slprNumber = Column(String(255))
    channelSpeed = Column(String(255))
    topology = Column(String(255))
    worldWidePortName = Column(String(255))
    portOption = Column(String(255))
    displayName = Column(String(255))
    controllerID = Column(String(255))
    portID = Column(String(255))
    portRole = Column(String(255))
    serialNumber = Column(String(255))
    keepAliveTime = Column(String(255))
    fibreAddress = Column(String(255))
    objectID = Column(String(255))


class HDS_CS_PORTCONTROLLER(Base, InternalFunctionality):
    __tablename__ = "hds_cs_portcontroller"
    id = Column(Integer, primary_key=True)
    card = Column(String(255))
    mode = Column(String(255))
    displayName = Column(String(255))
    controllerID = Column(String(255))
    serialNumber = Column(String(255))
    cluster = Column(String(255))
    type = Column(String(255))
    objectID = Column(String(255))


class HDS_CS_REPLICATIONINFO(Base, InternalFunctionality):
    __tablename__ = "hds_cs_replicationinfo"
    id = Column(Integer, primary_key=True)
    status = Column(String(255))
    fenceLevel = Column(String(255))
    muNumber = Column(String(255))
    pvolSerialNumber = Column(String(255))
    replicationFunction = Column(String(255))
    copyTrackSize = Column(String(255))
    pvolDevNum = Column(String(255))
    displayPvolDevNum = Column(String(255))
    svolPoolID = Column(String(255))
    pvolObjectID = Column(String(255))
    pvolPoolID = Column(String(255))
    svolArrayType = Column(String(255))
    pvolArrayType = Column(String(255))
    splitTime = Column(String(255))
    serialNumber = Column(String(255))
    svolSerialNumber = Column(String(255))
    svolDevNum = Column(String(255))
    remotePathGroupID = Column(String(255))
    displaySvolDevNum = Column(String(255))
    svolObjectID = Column(String(255))
    objectID = Column(String(255))

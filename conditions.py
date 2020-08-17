from Configuration.AlCa.GlobalTag import GlobalTag

from CondCore.CondDB.CondDB_cfi import *

#----------------------------------------------------------------------------------------------------

lhcInfoDefined = False

def UseLHCInfoLocal(process):
  global lhcInfoDefined
  lhcInfoDefined = True


def UseLHCInfoGT(process):
  global lhcInfoDefined
  lhcInfoDefined = True

  # these are not defined in local environment by default
  #del process.ctppsRPLHCInfoCorrectionsDataESSourceXML
  #del process.esPreferLocalLHCInfo


def UseLHCInfoFile(process, connection, tag):
  global lhcInfoDefined
  lhcInfoDefined = True

  del process.ctppsRPLHCInfoCorrectionsDataESSourceXML
  del process.esPreferLocalLHCInfo

  process.ctppsInterpolatedOpticalFunctionsESSource.lhcInfoLabel = ""
  process.ctppsProtons.lhcInfoLabel = ""
  
  process.CondDBALHCInfo = CondDB.clone( connect = connection )
  process.PoolDBESSource = cms.ESSource("PoolDBESSource",
    CondDBLHCInfo,
    DumpStat = cms.untracked.bool(False),
    toGet = cms.VPSet(cms.PSet(
      record = cms.string('LHCInfoRcd'),
      tag = cms.string(tag)
    )),
  )

#----------------------------------------------------------------------------------------------------

alignmentDefined = False

def UseAlignmentLocal(process):
  global alignmentDefined
  alignmentDefined = True

  if not hasattr(process, 'esPreferLocalAlignment'):
    raise ValueError("local alignment chosen, but process.esPreferLocalAlignment not defined")

def UseAlignmentGT(process):
  global alignmentDefined
  alignmentDefined = True

  if hasattr(process, 'esPreferLocalAlignment'):
    del process.ctppsRPAlignmentCorrectionsDataESSourceXML
    del process.esPreferLocalAlignment

def UseAlignmentFile(process, connection, tag):
  global alignmentDefined
  alignmentDefined = True

  if hasattr(process, 'esPreferLocalAlignment'):
    del process.ctppsRPAlignmentCorrectionsDataESSourceXML
    del process.esPreferLocalAlignment

  process.CondDBAlignment = CondDB.clone( connect = connection )
  process.PoolDBESSourceAlignment = cms.ESSource("PoolDBESSource",
    process.CondDBAlignment,
    #timetype = cms.untracked.string('runnumber'),
    toGet = cms.VPSet(cms.PSet(
      record = cms.string('RPRealAlignmentRecord'),
      tag = cms.string(tag)
    ))
  )
  
  process.esPreferDBFileAlignment = cms.ESPrefer("PoolDBESSource", "PoolDBESSourceAlignment")

def UseAlignmentDB(process, connection, tag):
  global alignmentDefined
  alignmentDefined = True

  if hasattr(process, 'esPreferLocalAlignment'):
    del process.ctppsRPAlignmentCorrectionsDataESSourceXML
    del process.esPreferLocalAlignment

  process.CondDBAlignment = CondDB.clone( connect = connection )
  process.PoolDBESSourceAlignment = cms.ESSource("PoolDBESSource",
      process.CondDBAlignment,
      #timetype = cms.untracked.string('runnumber'),
      toGet = cms.VPSet(cms.PSet(
          record = cms.string('RPRealAlignmentRecord'),
          tag = cms.string(tag)
      ))
  )
  
  process.esPreferDBFileAlignment = cms.ESPrefer("PoolDBESSource", "PoolDBESSourceAlignment")

#----------------------------------------------------------------------------------------------------

opticsDefined = False

def UseOpticsLocal(process):
  global opticsDefined
  opticsDefined = True

  if not hasattr(process, 'esPreferLocalOptics'):
    raise ValueError("local optics chosen, but process.esPreferLocalOptics not defined")

def UseOpticsGT(process):
  global opticsDefined
  opticsDefined = True

  if hasattr(process, 'esPreferLocalOptics'):
    del process.ctppsOpticalFunctionsESSource
    del process.esPreferLocalOptics

def UseOpticsFile(process, connection, tag):
  global opticsDefined
  opticsDefined = True

  if hasattr(process, 'esPreferLocalOptics'):
    del process.ctppsOpticalFunctionsESSource
    del process.esPreferLocalOptics

  process.CondDBOptics = CondDB.clone( connect = connection )
  process.PoolDBESSourceOptics = cms.ESSource("PoolDBESSource",
    process.CondDBOptics,
    DumpStat = cms.untracked.bool(False),
    toGet = cms.VPSet(cms.PSet(
      record = cms.string("CTPPSOpticsRcd"),
      tag = cms.string(tag)
    )),
  )
  
  process.esPreferDBFileOptics = cms.ESPrefer("PoolDBESSource", "PoolDBESSourceOptics")

def UseOpticsDB(process, connection, tag):
  global opticsDefined
  opticsDefined = True

  if hasattr(process, 'esPreferLocalOptics'):
    del process.ctppsOpticalFunctionsESSource
    del process.esPreferLocalOptics

  process.CondDBOptics = CondDB.clone( connect = connection )
  process.PoolDBESSourceOptics = cms.ESSource("PoolDBESSource",
      process.CondDBOptics,
      DumpStat = cms.untracked.bool(False),
      toGet = cms.VPSet(cms.PSet(
          record = cms.string('CTPPSOpticsRcd'),
          tag = cms.string(tag)
      )),
  )
  
  process.esPreferDBFileOptics = cms.ESPrefer("PoolDBESSource", "PoolDBESSourceOptics")

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------

def CheckConditions():
  # check choices
  if not lhcInfoDefined:
    raise ValueError("LHCInfo not defined")

  if not alignmentDefined:
    raise ValueError("alignment not defined")

  if not opticsDefined:
    raise ValueError("optics not defined")

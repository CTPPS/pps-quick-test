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


def UseAlignmentGT(process):
  global alignmentDefined
  alignmentDefined = True

  del process.ctppsRPAlignmentCorrectionsDataESSourceXML
  del process.esPreferLocalAlignment


def UseAlignmentFile(process, connection, tag):
  global alignmentDefined
  alignmentDefined = True

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


def UseOpticsGT(process):
  global opticsDefined
  opticsDefined = True

  del process.ctppsOpticalFunctionsESSource
  del process.esPreferLocalOptics


def UseOpticsFile(process, connection, tag):
  global opticsDefined
  opticsDefined = True

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

def SetConditions(process):
  # chose global tag
  process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
  #process.GlobalTag = GlobalTag(process.GlobalTag, "106X_dataRun2_2017_2018_Candidate_2019_12_02_18_57_30")
  process.GlobalTag = GlobalTag(process.GlobalTag, "106X_dataRun2_v24")
  #process.GlobalTag = GlobalTag(process.GlobalTag, "auto:run2_data")

  # chose LHCInfo
  UseLHCInfoGT(process)
  #UseLHCInfoLocal(process)
  #UseLHCInfoDB(process, "frontier://FrontierProd/CMS_CONDITIONS", "LHCInfoEndFill_prompt_v2")

  # chose alignment
  #UseAlignmentGT(process)
  #UseAlignmentLocal(process)
  #UseAlignmentFile(process, "sqlite_file:/afs/cern.ch/user/c/cmora/public/CTPPSDB/AlignmentSQlite/CTPPSRPRealAlignment_v13Jun19_v1.db", "PPSRPRealAlignment_v13Jun19")
  UseAlignmentDB(process, "frontier://FrontierProd/CMS_CONDITIONS", "CTPPSRPAlignment_real_offline_v7")

  # chose optics
  #UseOpticsGT(process)
  #UseOpticsLocal(process)
  #UseOpticsFile(process, "sqlite_file:/afs/cern.ch/user/w/wcarvalh/public/CTPPS/optical_functions/PPSOpticalFunctions_2016-2018_v7.db", "PPSOpticalFunctions_test")
  UseOpticsDB(process, "frontier://FrontierProd/CMS_CONDITIONS", "PPSOpticalFunctions_offline_v6")

  # check choices
  if not lhcInfoDefined:
    raise ValueError("LHCInfo not defined")

  if not alignmentDefined:
    raise ValueError("alignment not defined")

  if not opticsDefined:
    raise ValueError("optics not defined")

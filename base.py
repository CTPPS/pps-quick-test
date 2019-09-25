import FWCore.ParameterSet.Config as cms

def SetDefaults(process):
  # minimum of logs
  process.MessageLogger = cms.Service("MessageLogger",
    statistics = cms.untracked.vstring(),
    destinations = cms.untracked.vstring("cout"),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string("WARNING")
    )
  )

  # raw data source
  process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(),

    inputCommands = cms.untracked.vstring(
      'drop *',
      'keep FEDRawDataCollection_*_*_*'
    )
  )

  process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
  )

  # load default alignment settings
  process.load("CalibPPS.ESProducers.ctppsAlignment_cff")

  # raw-to-digi conversion
  process.load("EventFilter.CTPPSRawToDigi.ctppsRawToDigi_cff")

  # local RP reconstruction chain with standard settings
  process.load("RecoCTPPS.Configuration.recoCTPPS_cff")

  # declare global tag
  process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
  from Configuration.AlCa.GlobalTag import GlobalTag
  process.GlobalTag = GlobalTag(process.GlobalTag, "110X_dataRun2_v5")
  #process.GlobalTag = GlobalTag(process.GlobalTag, "106X_dataRun2_v11")
  #process.GlobalTag = GlobalTag(process.GlobalTag, "106X_dataRun2_testPPS_v1")
  #process.GlobalTag = GlobalTag(process.GlobalTag, "106X_dataRun2_v10")
  #process.GlobalTag = GlobalTag(process.GlobalTag, "auto:run2_data")

  # suppress local conditions sources
  #del process.ctppsRPAlignmentCorrectionsDataESSourceXML
  #del process.esPreferLocalAlignment

  #del process.ctppsOpticalFunctionsESSource
  #del process.esPreferLocalOptics

  # get optics from SQLite file
  ###   from CondCore.CondDB.CondDB_cfi import *
  ###   process.CondDBOptics = CondDB.clone( connect = 'sqlite_file:/afs/cern.ch/user/w/wcarvalh/public/CTPPS/optical_functions/PPSOpticalFunctions_2016-2018_v4.db' )
  ###   process.PoolDBESSourceOptics = cms.ESSource("PoolDBESSource",
  ###       process.CondDBOptics,
  ###       DumpStat = cms.untracked.bool(False),
  ###       toGet = cms.VPSet(cms.PSet(
  ###           record = cms.string('CTPPSOpticsRcd'),
  ###           tag = cms.string("PPSOpticalFunctions_test")
  ###       )),
  ###   )
  ###   
  ###   process.esPreferDBFileOptics = cms.ESPrefer("PoolDBESSource", "PoolDBESSourceOptics")

  # get optics from a DB tag
  ###   from CondCore.CondDB.CondDB_cfi import *
  ###   process.CondDBOptics = CondDB.clone( connect = 'frontier://FrontierProd/CMS_CONDITIONS' )
  ###   process.PoolDBESSourceOptics = cms.ESSource("PoolDBESSource",
  ###       process.CondDBOptics,
  ###       DumpStat = cms.untracked.bool(False),
  ###       toGet = cms.VPSet(cms.PSet(
  ###           record = cms.string('CTPPSOpticsRcd'),
  ###           tag = cms.string("PPSOpticalFunctions_offline_v3")
  ###       )),
  ###   )
  ###   
  ###   process.esPreferDBFileOptics = cms.ESPrefer("PoolDBESSource", "PoolDBESSourceOptics")
  ###   del process.esPreferLocalOptics

  # get alignment from SQLite file
  ###   from CondCore.CondDB.CondDB_cfi import *
  ###   process.CondDBAlignment = CondDB.clone( connect = 'sqlite_file:/afs/cern.ch/user/c/cmora/public/CTPPSDB/AlignmentSQlite/CTPPSRPRealAlignment_v13Jun19_v1.db' )
  ###   process.PoolDBESSourceAlignment = cms.ESSource("PoolDBESSource",
  ###       process.CondDBAlignment,
  ###       #timetype = cms.untracked.string('runnumber'),
  ###       toGet = cms.VPSet(cms.PSet(
  ###           record = cms.string('RPRealAlignmentRecord'),
  ###           tag = cms.string('PPSRPRealAlignment_v13Jun19')
  ###       ))
  ###   )
  ###   
  ###   process.esPreferDBFileAlignment = cms.ESPrefer("PoolDBESSource", "PoolDBESSourceAlignment")
  ###   del process.esPreferLocalAlignment

  # get alignment from a DB tag
  ###   from CondCore.CondDB.CondDB_cfi import *
  ###   process.CondDBAlignment = CondDB.clone( connect = 'frontier://FrontierProd/CMS_CONDITIONS' )
  ###   process.PoolDBESSourceAlignment = cms.ESSource("PoolDBESSource",
  ###       process.CondDBAlignment,
  ###       #timetype = cms.untracked.string('runnumber'),
  ###       toGet = cms.VPSet(cms.PSet(
  ###           record = cms.string('RPRealAlignmentRecord'),
  ###           tag = cms.string('CTPPSRPAlignment_real_offline_v2')
  ###       ))
  ###   )
  ###   
  ###   process.esPreferDBFileAlignment = cms.ESPrefer("PoolDBESSource", "PoolDBESSourceAlignment")
  ###   del process.esPreferLocalAlignment

  # get LHCInfo from DB tag
  ###   process.ctppsInterpolatedOpticalFunctionsESSource.lhcInfoLabel = ""
  ###   process.ctppsProtons.lhcInfoLabel = ""
  ###   
  ###   from CondCore.CondDB.CondDB_cfi import *
  ###   CondDB.connect = 'frontier://FrontierProd/CMS_CONDITIONS'
  ###   process.PoolDBESSource = cms.ESSource("PoolDBESSource",
  ###       CondDB,
  ###       DumpStat = cms.untracked.bool(False),
  ###       toGet = cms.VPSet(cms.PSet(
  ###           record = cms.string('LHCInfoRcd'),
  ###           tag = cms.string("LHCInfoEndFill_prompt_v2")
  ###       )),
  ###   )

  # reconstruction plotter
  process.ctppsProtonReconstructionPlotter = cms.EDAnalyzer("CTPPSProtonReconstructionPlotter",
      tagTracks = cms.InputTag("ctppsLocalTrackLiteProducer"),
      tagRecoProtonsSingleRP = cms.InputTag("ctppsProtons", "singleRP"),
      tagRecoProtonsMultiRP = cms.InputTag("ctppsProtons", "multiRP"),

      rpId_45_F = cms.uint32(0),
      rpId_45_N = cms.uint32(0),
      rpId_56_N = cms.uint32(0),
      rpId_56_F = cms.uint32(0),

      outputFile = cms.string("")
  )

  # load DQM framework
  process.load("DQM.Integration.config.environment_cfi")
  process.dqmEnv.subSystemFolder = "CTPPS"
  process.dqmEnv.eventInfoFolder = "EventInfo"
  process.dqmSaver.path = ""
  process.dqmSaver.tag = "CTPPS"

  # CTPPS DQM modules
  process.load("DQM.CTPPS.ctppsDQM_cff")

  # processing sequences
  process.path = cms.Path(
    process.ctppsRawToDigi
    * process.recoCTPPS
    * process.ctppsProtonReconstructionPlotter
    * process.ctppsDQM
  )

  process.end_path = cms.EndPath(
    process.dqmEnv +
    process.dqmSaver
  )

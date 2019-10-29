import FWCore.ParameterSet.Config as cms

from conditions import SetConditions

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

  # define conditions
  SetConditions(process)

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

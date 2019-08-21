import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TEST', eras.Run2_2018)

from base import *
SetDefaults(process)

#process.source.fileNames = cms.untracked.vstring("/store/data/Run2018C/ZeroBias/RAW/v1/000/319/450/00000/FE1EE87D-FA83-E811-91D5-FA163E4DBEC7.root")
process.source.fileNames = cms.untracked.vstring("root://eoscms.cern.ch//eos/cms/store/group/phys_pps/sw_test_input/FE1EE87D-FA83-E811-91D5-FA163E4DBEC7.root")

process.ctppsProtonReconstructionPlotter.rpId_45_F = 23
process.ctppsProtonReconstructionPlotter.rpId_45_N = 3
process.ctppsProtonReconstructionPlotter.rpId_56_N = 103
process.ctppsProtonReconstructionPlotter.rpId_56_F = 123
process.ctppsProtonReconstructionPlotter.outputFile = "2018C_reco_plots.root"

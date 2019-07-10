import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TEST', eras.Run2_2018)

from base import *
SetDefaults(process)

#process.source.fileNames = cms.untracked.vstring("/store/data/Run2018D/ZeroBias/RAW/v1/000/320/688/00000/601A721D-AD95-E811-B21A-FA163E28A50A.root")
process.source.fileNames = cms.untracked.vstring("root://eoscms.cern.ch//eos/cms/store/group/phys_pps/sw_test_input/601A721D-AD95-E811-B21A-FA163E28A50A.root")

process.ctppsProtonReconstructionPlotter.rpId_45_F = 23
process.ctppsProtonReconstructionPlotter.rpId_45_N = 3
process.ctppsProtonReconstructionPlotter.rpId_56_N = 103
process.ctppsProtonReconstructionPlotter.rpId_56_F = 123
process.ctppsProtonReconstructionPlotter.outputFile = "2018_reco_plots.root"

import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TEST', eras.Run2_2016)

from base import *
SetDefaults(process)

#process.source.fileNames = cms.untracked.vstring("/store/data/Run2016H/ZeroBias/RAW/v1/000/283/453/00000/3204EE5B-C298-E611-BC39-02163E01448F.root")
process.source.fileNames = cms.untracked.vstring("root://eoscms.cern.ch//eos/cms/store/group/phys_pps/sw_test_input/3204EE5B-C298-E611-BC39-02163E01448F.root")

process.ctppsProtonReconstructionPlotter.rpId_45_F = 3
process.ctppsProtonReconstructionPlotter.rpId_45_N = 2
process.ctppsProtonReconstructionPlotter.rpId_56_N = 102
process.ctppsProtonReconstructionPlotter.rpId_56_F = 103
process.ctppsProtonReconstructionPlotter.outputFile = "2016_postTS2_reco_plots.root"

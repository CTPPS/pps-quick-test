import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TEST', eras.Run2_2017)

from base import *
SetDefaults(process)

#process.source.fileNames = cms.untracked.vstring("/store/data/Run2017F/ZeroBias/RAW/v1/000/305/081/00000/001D08EE-C4B1-E711-B92D-02163E013864.root")
process.source.fileNames = cms.untracked.vstring("root://eoscms.cern.ch//eos/cms/store/group/phys_pps/sw_test_input/001D08EE-C4B1-E711-B92D-02163E013864.root")

process.ctppsProtonReconstructionPlotter.rpId_45_F = 23
process.ctppsProtonReconstructionPlotter.rpId_45_N = 3
process.ctppsProtonReconstructionPlotter.rpId_56_N = 103
process.ctppsProtonReconstructionPlotter.rpId_56_F = 123
process.ctppsProtonReconstructionPlotter.outputFile = "2017_postTS2_reco_plots.root"

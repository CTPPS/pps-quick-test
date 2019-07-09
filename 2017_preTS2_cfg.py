import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TEST', eras.Run2_2017)

from base import *
SetDefaults(process)

#process.source.fileNames = cms.untracked.vstring("/store/data/Run2017C/ZeroBias/RAW/v1/000/301/283/00000/8ED63519-2282-E711-9073-02163E01A3C6.root")
process.source.fileNames = cms.untracked.vstring("root://eostotem.cern.ch//eos/totem/user/j/jkaspar/8ED63519-2282-E711-9073-02163E01A3C6.root")

process.ctppsProtonReconstructionPlotter.rpId_45_F = 23
process.ctppsProtonReconstructionPlotter.rpId_45_N = 3
process.ctppsProtonReconstructionPlotter.rpId_56_N = 103
process.ctppsProtonReconstructionPlotter.rpId_56_F = 123
process.ctppsProtonReconstructionPlotter.outputFile = "2017_preTS2_reco_plots.root"

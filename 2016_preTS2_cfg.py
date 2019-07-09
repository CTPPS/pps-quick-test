import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TEST', eras.Run2_2016)

from base import *
SetDefaults(process)

#process.source.fileNames = cms.untracked.vstring("/store/data/Run2016B/ZeroBias/RAW/v2/000/275/371/00000/EAD70032-8836-E611-8C11-02163E014154.root")
process.source.fileNames = cms.untracked.vstring("root://eostotem.cern.ch//eos/totem/user/j/jkaspar/EAD70032-8836-E611-8C11-02163E014154.root")

process.ctppsProtonReconstructionPlotter.rpId_45_F = 3
process.ctppsProtonReconstructionPlotter.rpId_45_N = 2
process.ctppsProtonReconstructionPlotter.rpId_56_N = 102
process.ctppsProtonReconstructionPlotter.rpId_56_F = 103
process.ctppsProtonReconstructionPlotter.outputFile = "2016_preTS2_reco_plots.root"

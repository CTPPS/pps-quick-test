import root;
import pad_layout;

string periods[], p_runs[];
periods.push("2016_preTS2"); p_runs.push("275371");
periods.push("2016_postTS2"); p_runs.push("283453");

periods.push("2017_preTS2"); p_runs.push("301283");
periods.push("2017_postTS2"); p_runs.push("305081");

periods.push("2018"); p_runs.push("320688");
//periods.push("2018A"); p_runs.push("315489");
//periods.push("2018B"); p_runs.push("317435");
//periods.push("2018C"); p_runs.push("319450");
//periods.push("2018D"); p_runs.push("320822");

string plots[], pl_sectors[], pl_paths[];
plots.push("$\xi$"); pl_sectors.push("45"); pl_paths.push("multiRPPlots/arm0/h_xi");
plots.push("$\th^*_x\ung{rad}$"); pl_sectors.push("45"); pl_paths.push("multiRPPlots/arm0/h_th_x");
plots.push("$\th^*_y\ung{rad}$"); pl_sectors.push("45"); pl_paths.push("multiRPPlots/arm0/h_th_y");
plots.push("$|t|\ung{GeV^2}$"); pl_sectors.push("45"); pl_paths.push("multiRPPlots/arm0/h_t");
plots.push("n timing-RP tracks"); pl_sectors.push("45"); pl_paths.push("multiRPPlots/arm0/h_n_timing_RPs");

plots.push("$\xi$"); pl_sectors.push("56"); pl_paths.push("multiRPPlots/arm1/h_xi");
plots.push("$\th^*_x\ung{rad}$"); pl_sectors.push("56"); pl_paths.push("multiRPPlots/arm1/h_th_x");
plots.push("$\th^*_y\ung{rad}$"); pl_sectors.push("56"); pl_paths.push("multiRPPlots/arm1/h_th_y");
plots.push("$|t|\ung{GeV^2}$"); pl_sectors.push("56"); pl_paths.push("multiRPPlots/arm1/h_t");
plots.push("n timing-RP tracks"); pl_sectors.push("56"); pl_paths.push("multiRPPlots/arm1/h_n_timing_RPs");

string dirs[], d_labels[];
pen d_pens[];
dirs.push("version_2"); d_pens.push(red); d_labels.push("CMSSW_11_0_0_pre5, 110X_dataRun2_v3");

xSizeDef = 8cm;
ySizeDef = 8cm;

//----------------------------------------------------------------------------------------------------

NewPad(false);
for (int di : dirs.keys)
	AddToLegend(replace(dirs[di] + ": " + d_labels[di], "_", "\_"), d_pens[di]);
AttachLegend();

//----------------------------------------------------------------------------------------------------

for (int peri : periods.keys)
{
	NewRow();

	NewPadLabel("\vbox{\hbox{" + replace(periods[peri], "_", "\_") + "}\hbox{(subsample of run " + p_runs[peri] + ")}}");

	string f_old = "/afs/cern.ch/work/j/jkaspar/software/ctpps/development/ctpps_initial_proton_reconstruction_CMSSW_10_2_0/CMSSW_10_2_0/src/forward-test/reco_plots_" + periods[peri] + ".root";
	//string f_new = "DQM_V0001_CTPPS_R000" + p_runs[peri] + ".root";
	string f_new = "reco_plots_" + periods[peri] + ".root";

	for (int pli : plots.keys)
	{
		NewPad(plots[pli]);

		for (int diri : dirs.keys)
		{
			string f = dirs[diri] + "/" + periods[peri] + "_reco_plots.root";

			RootObject hist = RootGetObject(f, pl_paths[pli], error=false);
			if (!hist.valid)
				continue;

			draw(hist, "vl", d_pens[diri]);
		}

		AttachLegend("sector " + pl_sectors[pli]);
	}
}

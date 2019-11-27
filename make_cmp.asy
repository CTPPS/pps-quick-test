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
int pl_rebin[];
plots.push("$\xi$"); pl_sectors.push("45"); pl_paths.push("multiRPPlots/arm0/h_xi"); pl_rebin.push(2);
plots.push("$\th^*_x\ung{rad}$"); pl_sectors.push("45"); pl_paths.push("multiRPPlots/arm0/h_th_x"); pl_rebin.push(5);
plots.push("$\th^*_y\ung{rad}$"); pl_sectors.push("45"); pl_paths.push("multiRPPlots/arm0/h_th_y"); pl_rebin.push(5);
//plots.push("$|t|\ung{GeV^2}$"); pl_sectors.push("45"); pl_paths.push("multiRPPlots/arm0/h_t"); pl_rebin.push(2);
plots.push("n timing-RP tracks"); pl_sectors.push("45"); pl_paths.push("multiRPPlots/arm0/h_n_timing_RPs"); pl_rebin.push(1);

plots.push("$\xi$"); pl_sectors.push("56"); pl_paths.push("multiRPPlots/arm1/h_xi"); pl_rebin.push(2);
plots.push("$\th^*_x\ung{rad}$"); pl_sectors.push("56"); pl_paths.push("multiRPPlots/arm1/h_th_x"); pl_rebin.push(5);
plots.push("$\th^*_y\ung{rad}$"); pl_sectors.push("56"); pl_paths.push("multiRPPlots/arm1/h_th_y"); pl_rebin.push(5);
//plots.push("$|t|\ung{GeV^2}$"); pl_sectors.push("56"); pl_paths.push("multiRPPlots/arm1/h_t"); pl_rebin.push(2);
plots.push("n timing-RP tracks"); pl_sectors.push("56"); pl_paths.push("multiRPPlots/arm1/h_n_timing_RPs"); pl_rebin.push(1);

string dirs[], d_labels[];
pen d_pens[];

//dirs.push("version_1"); d_pens.push(red+dashed); d_labels.push("at 36baea99e0, GT 106X_dataRun2_v11, alignment local, optics local");
//dirs.push("version_2"); d_pens.push(blue); d_labels.push("at 36baea99e0, GT 106X_dataRun2_v11, alignment local, optics from Wagner's PPSOpticalFunctions_2016-2018_v5.db");

//dirs.push("version_3"); d_pens.push(blue); d_labels.push("at f2e490a377, GT 110X_dataRun2_v3, alignment local, optics local");
//dirs.push("version_4"); d_pens.push(red+dashed); d_labels.push("at f2e490a377, GT 110X_dataRun2_v3, alignment local, optics from GT");
//dirs.push("version_5"); d_pens.push(red+dashed); d_labels.push("at f2e490a377, GT 110X_dataRun2_v5, alignment local, optics local");
//dirs.push("version_6"); d_pens.push(red+dashed); d_labels.push("at 9e9b04c318, GT 110X_dataRun2_v5, alignment local, optics local");
dirs.push("version_7"); d_pens.push(blue); d_labels.push("at 4ac6dbca48, GT 110X_dataRun2_v5, alignment local, optics local");
//dirs.push("version_8"); d_pens.push(red+dashed); d_labels.push("at 4ac6dbca48, GT 110X_dataRun2_v5, alignment local, optics from Wagner's PPSOpticalFunctions_2016-2018_v7.db");
//dirs.push("version_9"); d_pens.push(red+dashed); d_labels.push("at 69fecefd, GT 110X_dataRun2_v5, CTPPSRPAlignment_real_offline_v5, PPSOpticalFunctions_offline_v5");

dirs.push("version_10"); d_pens.push(red+dashed); d_labels.push("at 94dca488447e8d1fcf483956ac1fbf99471c3359, GT 110X_dataRun2_v5, alignment local, optics local");

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

			hist.vExec("Rebin", pl_rebin[pli]);

			draw(hist, "vl", d_pens[diri]);
		}

		AttachLegend("sector " + pl_sectors[pli]);
	}
}

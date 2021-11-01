import root;
import pad_layout;

include "versions.asy";
include "common_code.asy";

string topDir = "../";

string periods[], p_runs[];
periods.push("2016_preTS2"); p_runs.push("275371");
periods.push("2016_postTS2"); p_runs.push("283453");

periods.push("2017_preTS2"); p_runs.push("301283");
periods.push("2017_postTS2"); p_runs.push("305081");

//periods.push("2017E_low_PU"); p_runs.push("303819");
//periods.push("2017H_W_mass"); p_runs.push("307082");

periods.push("2018"); p_runs.push("320688");
//periods.push("2018A"); p_runs.push("315489");
//periods.push("2018B"); p_runs.push("317435");
//periods.push("2018C"); p_runs.push("319450");
//periods.push("2018D"); p_runs.push("320822");

string pl_paths[], pl_titles[], pl_x_labels[];
int pl_rebin[];
real pl_x_mins[], pl_x_maxs[];
pl_paths.push("multiRPPlots/arm0/h_xi");                      pl_titles.push("sector 45: $\xi$");              pl_x_labels.push("$\xi$");              pl_rebin.push(2); pl_x_mins.push(0.); pl_x_maxs.push(0.25);
pl_paths.push("multiRPPlots/arm0/h_th_x");                    pl_titles.push("sector 45: $\th^*_x$");          pl_x_labels.push("$\th^*_x\ung{rad}$"); pl_rebin.push(15); pl_x_mins.push(-5e-4); pl_x_maxs.push(+5e-4);
pl_paths.push("multiRPPlots/arm0/h_th_y");                    pl_titles.push("sector 45: $\th^*_y$");          pl_x_labels.push("$\th^*_y\ung{rad}$"); pl_rebin.push(5); pl_x_mins.push(-5e-4); pl_x_maxs.push(+5e-4);
pl_paths.push("multiRPPlots/arm0/h_t");                       pl_titles.push("sector 45: $|t|$");              pl_x_labels.push("$|t|\ung{GeV^2}$");   pl_rebin.push(2); pl_x_mins.push(0.); pl_x_maxs.push(3.);
pl_paths.push("multiRPPlots/arm0/h_n_contrib_timing_tracks"); pl_titles.push("sector 45: n-timing RP tracks"); pl_x_labels.push("n timing-RP tracks"); pl_rebin.push(1); pl_x_mins.push(-0.5); pl_x_maxs.push(3.5);
pl_paths.push("multiRPPlots/arm0/h_time");                    pl_titles.push("sector 45: time");               pl_x_labels.push("time$\ung{ns}$");     pl_rebin.push(2); pl_x_mins.push(-2); pl_x_maxs.push(+2);

pl_paths.push("multiRPPlots/arm1/h_xi");                      pl_titles.push("sector 56: $\xi$");              pl_x_labels.push("$\xi$");              pl_rebin.push(2); pl_x_mins.push(0.); pl_x_maxs.push(0.25);
pl_paths.push("multiRPPlots/arm1/h_th_x");                    pl_titles.push("sector 56: $\th^*_x$");          pl_x_labels.push("$\th^*_x\ung{rad}$"); pl_rebin.push(15); pl_x_mins.push(-5e-4); pl_x_maxs.push(+5e-4);
pl_paths.push("multiRPPlots/arm1/h_th_y");                    pl_titles.push("sector 56: $\th^*_y$");          pl_x_labels.push("$\th^*_y\ung{rad}$"); pl_rebin.push(5); pl_x_mins.push(-5e-4); pl_x_maxs.push(+5e-4);
pl_paths.push("multiRPPlots/arm1/h_t");                       pl_titles.push("sector 56: $|t|$");              pl_x_labels.push("$|t|\ung{GeV^2}$");   pl_rebin.push(2); pl_x_mins.push(0.); pl_x_maxs.push(3.);
pl_paths.push("multiRPPlots/arm1/h_n_contrib_timing_tracks"); pl_titles.push("sector 56: n-timing RP tracks"); pl_x_labels.push("n timing-RP tracks"); pl_rebin.push(1); pl_x_mins.push(-0.5); pl_x_maxs.push(3.5);
pl_paths.push("multiRPPlots/arm1/h_time");                    pl_titles.push("sector 56: time");               pl_x_labels.push("time$\ung{ns}$");     pl_rebin.push(2); pl_x_mins.push(-2); pl_x_maxs.push(+2);


xSizeDef = 8cm;
ySizeDef = 8cm;

//----------------------------------------------------------------------------------------------------

NewPad(false);
for (int di : dirs.keys)
	//AddToLegend(replace(dirs[di] + ": " + d_labels[di], "_", "\_"), d_pens[di]);
	AddToLegend(replace(d_labels[di], "_", "\_"), d_pens[di]);
AttachLegend();

for (int pli : pl_paths.keys)
	NewPadLabel(pl_titles[pli]);

//----------------------------------------------------------------------------------------------------

for (int peri : periods.keys)
{
	// histogram comparison
	NewRow();

	NewPadLabel("\vbox{\hbox{" + replace(periods[peri], "_", "\_") + "}\hbox{(subsample of run " + p_runs[peri] + ")}}");

	for (int pli : pl_paths.keys)
	{
		NewPad("", "entries", xTicks=LeftTicks("{}"));
		scale(Linear, Linear(true));

		for (int diri : dirs.keys)
		{
			string f = topDir + dirs[diri] + "/reco:" + periods[peri] + "/reco_plots.root";

			RootObject hist = RootGetObject(f, pl_paths[pli], error=false);
			if (!hist.valid)
				continue;

			hist.vExec("Rebin", pl_rebin[pli]);

			draw(hist, "vl", d_pens[diri]);
		}

		xlimits(pl_x_mins[pli], pl_x_maxs[pli], Crop);
	}

	// histogram ratio
	NewRow();

	NewPad(false);

	for (int pli : pl_paths.keys)
	{
		NewPad(pl_x_labels[pli], "ratio", ySize = 3cm);
		scale(Linear, Linear(true));

		int ref_idx = 0;
		string f_ref = topDir + dirs[ref_idx] + "/reco:" + periods[peri] + "/reco_plots.root";
		RootObject hist_ref = RootGetObject(f_ref, pl_paths[pli], error=false);
		if (!hist_ref.valid)
			continue;

		hist_ref.vExec("Rebin", pl_rebin[pli]);

		for (int diri : dirs.keys)
		{
			string f = topDir + dirs[diri] + "/reco:" + periods[peri] + "/reco_plots.root";

			RootObject hist = RootGetObject(f, pl_paths[pli], error=false);
			if (!hist.valid)
				continue;
			
			hist.vExec("Rebin", pl_rebin[pli]);

			DrawRatio(hist, hist_ref, d_pens[diri]);

			// to define vertical range in case completely flat ratio
			dot((0, 1.01), invisible);
			dot((0, 0.99), invisible);
		}

		xlimits(pl_x_mins[pli], pl_x_maxs[pli], Crop);
	}

	// add vertical space
	NewRow();
	NewPadLabel("\vbox to 5mm{}");
}

GShipout(vSkip=0mm);

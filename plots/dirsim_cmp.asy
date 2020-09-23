import root;
import pad_layout;

include "versions.asy";

string topDir = "../";

string periods[];
periods.push("2016_preTS2");
periods.push("2016_postTS2");

periods.push("2017_preTS2");
periods.push("2017_postTS2");

periods.push("2018_preTS1");
periods.push("2018_TS1_TS2");
periods.push("2018_postTS2");

string plots[], pl_labels[], pl_files[], pl_paths[];
int pl_rebin[];
plots.push("$x$"); pl_labels.push("RP 3: simu $x$"); pl_files.push("tracks.root"); pl_paths.push("RP 3/h_x"); pl_rebin.push(5);
plots.push("$y$"); pl_labels.push("RP 3: simu $y$"); pl_files.push("tracks.root"); pl_paths.push("RP 3/h_y"); pl_rebin.push(5);
plots.push("$\xi$"); pl_labels.push("sector 45: reco $\xi$"); pl_files.push("protons.root"); pl_paths.push("multiRPPlots/arm0/h_xi"); pl_rebin.push(2);

plots.push("$x$"); pl_labels.push("RP 103: simu $x$"); pl_files.push("tracks.root"); pl_paths.push("RP 103/h_x"); pl_rebin.push(5);
plots.push("$y$"); pl_labels.push("RP 103: simu $y$"); pl_files.push("tracks.root"); pl_paths.push("RP 103/h_y"); pl_rebin.push(5);
plots.push("$\xi$"); pl_labels.push("sector 56: reco $\xi$"); pl_files.push("protons.root"); pl_paths.push("multiRPPlots/arm1/h_xi"); pl_rebin.push(2);

xSizeDef = 8cm;
ySizeDef = 8cm;

//----------------------------------------------------------------------------------------------------

NewPad(false);
for (int di : dirs.keys)
	//AddToLegend(replace(dirs[di] + ": " + d_labels[di], "_", "\_"), d_pens[di]);
	AddToLegend(replace(d_labels[di], "_", "\_"), d_pens[di]);
AttachLegend();

for (int pli : plots.keys)
	NewPadLabel("\vbox{\hbox{" + pl_labels[pli] + "}}");

//----------------------------------------------------------------------------------------------------

for (int peri : periods.keys)
{
	NewRow();

	NewPadLabel("\vbox{\hbox{" + replace(periods[peri], "_", "\_") + "}}");

	for (int pli : plots.keys)
	{
		NewPad(plots[pli]);

		for (int diri : dirs.keys)
		{
			string f = topDir + dirs[diri] + "/dirsim:" + periods[peri] + "/" + pl_files[pli];

			RootObject hist = RootGetObject(f, pl_paths[pli], error=true);
			if (!hist.valid)
				continue;

			hist.vExec("Rebin", pl_rebin[pli]);

			draw(hist, "vl", d_pens[diri]);
		}

		//AttachLegend(pl_labels[pli]);
	}
}

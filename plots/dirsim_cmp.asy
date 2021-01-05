import root;
import pad_layout;

include "versions.asy";

string topDir = "../";

string periods[];
periods.push("2016");
//periods.push("2016_preTS2");
periods.push("2016_postTS2");

periods.push("2017");
//periods.push("2017_preTS2");
periods.push("2017_postTS2");

periods.push("2018");
//periods.push("2018_preTS1");
//periods.push("2018_TS1_TS2");
periods.push("2018_postTS2");

periods.push("2021");

string plots[], pl_labels[], pl_files[], pl_paths[];
int pl_rebin[];
real pl_x_min[], pl_x_max[];

plots.push("xangle"); pl_labels.push("crossing angle"); pl_files.push("lhcInfo.root"); pl_paths.push("h_xangle"); pl_rebin.push(1); pl_x_min.push(80); pl_x_max.push(190);
plots.push("$\beta^*\ung{cm}$"); pl_labels.push("beta*"); pl_files.push("lhcInfo.root"); pl_paths.push("h_betaStar"); pl_rebin.push(1); pl_x_min.push(0.); pl_x_max.push(0.5);

plots.push("$x$"); pl_labels.push("RP 3: simu $x$"); pl_files.push("tracks.root"); pl_paths.push("RP 3/h_x"); pl_rebin.push(5); pl_x_min.push(-5); pl_x_max.push(25);
plots.push("$y$"); pl_labels.push("RP 3: simu $y$"); pl_files.push("tracks.root"); pl_paths.push("RP 3/h_y"); pl_rebin.push(5); pl_x_min.push(-10); pl_x_max.push(10);
plots.push("$\xi$"); pl_labels.push("sector 45: reco $\xi$"); pl_files.push("protons.root"); pl_paths.push("multiRPPlots/arm0/h_xi"); pl_rebin.push(2); pl_x_min.push(0); pl_x_max.push(0.25);

plots.push("$x$"); pl_labels.push("RP 103: simu $x$"); pl_files.push("tracks.root"); pl_paths.push("RP 103/h_x"); pl_rebin.push(5); pl_x_min.push(-5); pl_x_max.push(25);
plots.push("$y$"); pl_labels.push("RP 103: simu $y$"); pl_files.push("tracks.root"); pl_paths.push("RP 103/h_y"); pl_rebin.push(5); pl_x_min.push(-10); pl_x_max.push(10);
plots.push("$\xi$"); pl_labels.push("sector 56: reco $\xi$"); pl_files.push("protons.root"); pl_paths.push("multiRPPlots/arm1/h_xi"); pl_rebin.push(2); pl_x_min.push(0); pl_x_max.push(0.25);

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

			RootObject hist = RootGetObject(f, pl_paths[pli], error=false);
			if (!hist.valid)
				continue;

			hist.vExec("Rebin", pl_rebin[pli]);

			draw(hist, "vl", d_pens[diri]);
		}

		xlimits(pl_x_min[pli], pl_x_max[pli], Crop);

		//AttachLegend(pl_labels[pli]);
	}
}

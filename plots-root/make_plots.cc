#include "TFile.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TLatex.h"
#include "TLegend.h"

#include <vector>
#include <string>

#include "versions.h"

using namespace std;

//----------------------------------------------------------------------------------------------------

struct Period
{
	string tag;
	string label;
};

//----------------------------------------------------------------------------------------------------

struct Plot
{
    string file;
	string path;
	string axis_label;
	string column_label;
	int rebin;
};

//----------------------------------------------------------------------------------------------------

TH1D* GetHistogram(const string &file, const string &path)
{
	unique_ptr<TFile> f(TFile::Open(file.c_str()));
	if (!f)
		return nullptr;

	TH1D *h = (TH1D*) f->Get(path.c_str());
	if (!h)
		return nullptr;

	h->SetDirectory(nullptr);

	return h;
}

//----------------------------------------------------------------------------------------------------

void MakePlots(const string &dirPrefix, const vector<Version> &versions, const vector<Plot> &plots, const vector<Period> &periods, const string &fn)
{
	TCanvas *c = new TCanvas();
	c->SetCanvasSize(8000, 3000);

	// create sub pads
	c->Divide(plots.size() + 1, periods.size() + 1);

	// add version labels
	c->cd(1);
	auto *legend = new TLegend(0.4, 0.5);

	for (const auto &v : versions)
	{
		TH1D *h = new TH1D("", "", 1, 0., 1.);
		h->SetLineColor(v.color);
		h->SetLineStyle(v.style);
		legend->AddEntry(h, v.label.c_str());	
	}

	legend->Draw();

	// add row labels
	for (int pe_idx = 0; pe_idx < periods.size(); ++pe_idx)
	{
		const int ca_idx = (pe_idx+1) * (plots.size()+1) + 1;
		c->cd(ca_idx);

		const auto &pe = periods[pe_idx];

		TLatex *l = new TLatex(0, 0, ("#scale[2]{" + pe.tag + ", " + pe.label + "}").c_str());
		l->Draw();
	}

	// add column labels
	for (int pl_idx = 0; pl_idx < plots.size(); ++pl_idx)
	{
		const int ca_idx = pl_idx + 2;
		c->cd(ca_idx);

		const auto &pl = plots[pl_idx];

		TLatex *l = new TLatex(0, 0, ("#scale[2]{" + pl.column_label + "}").c_str());
		l->Draw();
	}

	// draw plots
	for (int pl_idx = 0; pl_idx < plots.size(); ++pl_idx)
	{
		for (int pe_idx = 0; pe_idx < periods.size(); ++pe_idx)
		{
			const int ca_idx = (pe_idx+1) * (plots.size()+1) + (pl_idx+1) + 1;
			c->cd(ca_idx); 

			bool first = true;
			for (const auto &v : versions)
			{
				const auto &pl = plots[pl_idx];

				TH1D *h = GetHistogram("../" + v.dir + "/" + dirPrefix + periods[pe_idx].tag + "/" + pl.file, pl.path);
				if (!h)
					continue;
				
				h->Rebin(pl.rebin);
				h->SetLineColor(v.color);
				h->SetLineStyle(v.style);

				if (first)
					h->SetTitle((";" + pl.axis_label).c_str());

				h->Draw((first) ? "" : "same");

				first = false;
			}
		}
	}

	c->SaveAs(fn.c_str());

	delete c;
}

//----------------------------------------------------------------------------------------------------

void MakeRecoPlots(const vector<Version> &versions, const string &extension)
{
    printf("* MakeRecoPlots\n");

	// define plots (columns)
	vector<Plot> plots;

	plots.push_back({"reco_plots.root", "multiRPPlots/arm0/h_xi", "#xi", "sector 45: #xi", 2});
	plots.push_back({"reco_plots.root", "multiRPPlots/arm0/h_th_x", "#theta^{*}_{x}   (rad)", "sector 45: #theta^{*}_{x}", 5});
	plots.push_back({"reco_plots.root", "multiRPPlots/arm0/h_th_y", "#theta^{*}_{y}   (rad)", "sector 45: #theta^{*}_{y}", 5});
	plots.push_back({"reco_plots.root", "multiRPPlots/arm0/h_n_contrib_timing_tracks", "n timing-RP tracks", "sector 45: n timing-RP tracks", 1});
	plots.push_back({"reco_plots.root", "multiRPPlots/arm0/h_time", "time   (ns)", "sector 45: time", 2});

	plots.push_back({"reco_plots.root", "multiRPPlots/arm1/h_xi", "#xi", "sector 56: #xi", 2});
	plots.push_back({"reco_plots.root", "multiRPPlots/arm1/h_th_x", "#theta^{*}_{x}   (rad)", "sector 56: #theta^{*}_{x}", 5});
	plots.push_back({"reco_plots.root", "multiRPPlots/arm1/h_th_y", "#theta^{*}_{y}   (rad)", "sector 56: #theta^{*}_{y}", 5});
	plots.push_back({"reco_plots.root", "multiRPPlots/arm1/h_n_contrib_timing_tracks", "n timing-RP tracks", "sector 56: n timing-RP tracks", 1});
	plots.push_back({"reco_plots.root", "multiRPPlots/arm1/h_time", "time   (ns)", "sector 56: time", 2});

	// define periods (rows)
	vector<Period> periods;

	periods.push_back({"2016_preTS2", "run 275371"});
	periods.push_back({"2016_postTS2", "run 283453"});

	periods.push_back({"2017_preTS2", "run 301283"});
	periods.push_back({"2017_postTS2", "run 305081"});

	//periods.push_back({"2017E_low_PU", "run 303819"});
	//periods.push_back({"2017H_W_mass", "run 307082"});

	periods.push_back({"2018", "run 320688"});
	//periods.push_back({"2018A", "run 315489"});
	//periods.push_back({"2018B", "run 317435"});
	//periods.push_back({"2018C", "run 319450"});
	//periods.push_back({"2018D", "run 320822"});

	// make output (plot grid)
	MakePlots("reco:", versions, plots, periods, "reco_cmp." + extension);
}

//----------------------------------------------------------------------------------------------------

void MakeDirSimPlots(const vector<Version> &versions, const string &extension)
{
    printf("* MakeDirSimPlots\n");

	// define plots (columns)
	vector<Plot> plots;

	plots.push_back({"lhcInfo.root", "h_xangle", "crossing angle", "crossing angle", 1});
	plots.push_back({"lhcInfo.root", "h_betaStar", "#beta^*", "beta star", 1});

	plots.push_back({"tracks.root", "RP 3/h_x", "x   (mm)", "RP 3: x", 5});
	plots.push_back({"tracks.root", "RP 3/h_y", "y   (mm)", "RP 3: y", 5});
	plots.push_back({"protons.root", "multiRPPlots/arm0/h_xi", "#xi_{multi})", "sector 45: #xi multi", 2});

	plots.push_back({"tracks.root", "RP 103/h_x", "x   (mm)", "RP 103: x", 5});
	plots.push_back({"tracks.root", "RP 103/h_y", "y   (mm)", "RP 103: y", 5});
	plots.push_back({"protons.root", "multiRPPlots/arm1/h_xi", "#xi_{multi})", "sector 56: #xi multi", 2});

	// define periods (rows)
	vector<Period> periods;

	periods.push_back({"2016", ""});
	periods.push_back({"2016_postTS2", ""});

	periods.push_back({"2017", ""});
	periods.push_back({"2017_postTS2", ""});

	periods.push_back({"2018", ""});
	periods.push_back({"2018_postTS2", ""});

	periods.push_back({"2021", ""});
	periods.push_back({"2022", ""});

	// make output (plot grid)
	MakePlots("dirsim:", versions, plots, periods, "dirsim_cmp." + extension);
}

//----------------------------------------------------------------------------------------------------

int make_plots()
{
    string extension = "png";

	MakeRecoPlots(versions, extension);
	MakeDirSimPlots(versions, extension);

	return 0;
}

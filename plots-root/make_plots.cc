#include "TFile.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TLatex.h"
#include "TLegend.h"

#include <vector>
#include <string>

using namespace std;

//----------------------------------------------------------------------------------------------------

struct Version
{
	string dir;
	string label;
	int color;
	int style;
};

//----------------------------------------------------------------------------------------------------

struct Period
{
	string tag;
	string label;
};

//----------------------------------------------------------------------------------------------------

struct Plot
{
	string path;
	string label;
	string sector;
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

void MakePlots(const vector<Version> &versions, const vector<Plot> &plots, const vector<Period> &periods, const string &fn)
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

		TLatex *l = new TLatex(0, 0, ("#scale[2]{sector " + pl.sector + ": " + pl.label + "}").c_str());
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

				TH1D *h = GetHistogram("../" + v.dir + "/reco:" + periods[pe_idx].tag + "/reco_plots.root", pl.path);
				if (!h)
					continue;
				
				h->Rebin(pl.rebin);
				h->SetLineColor(v.color);
				h->SetLineStyle(v.style);

				if (first)
					h->SetTitle((";" + pl.label).c_str());

				h->Draw((first) ? "" : "same");

				first = false;
			}
		}
	}

	c->SaveAs(fn.c_str());

	delete c;
}

//----------------------------------------------------------------------------------------------------

void MakeRecoPlots(const vector<Version> &versions)
{
	// define plots (columns)
	vector<Plot> plots;

	plots.push_back({"multiRPPlots/arm0/h_xi", "#xi", "45", 2});
	plots.push_back({"multiRPPlots/arm0/h_th_x", "#theta^{*}_{x}   (rad)", "45", 5});
	plots.push_back({"multiRPPlots/arm0/h_th_y", "#theta^{*}_{y}   (rad)", "45", 5});
	plots.push_back({"multiRPPlots/arm0/h_n_contrib_timing_tracks", "n timing-RP tracks", "45", 1});
	plots.push_back({"multiRPPlots/arm0/h_time", "time   (ns)", "45", 2});

	plots.push_back({"multiRPPlots/arm1/h_xi", "#xi", "56", 2});
	plots.push_back({"multiRPPlots/arm1/h_th_x", "#theta^{*}_{x}   (rad)", "56", 5});
	plots.push_back({"multiRPPlots/arm1/h_th_y", "#theta^{*}_{y}   (rad)", "56", 5});
	plots.push_back({"multiRPPlots/arm1/h_n_contrib_timing_tracks", "n timing-RP tracks", "56", 1});
	plots.push_back({"multiRPPlots/arm1/h_time", "time   (ns)", "56", 2});

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
	MakePlots(versions, plots, periods, "reco_cmp.png");
}

//----------------------------------------------------------------------------------------------------

int make_plots()
{
	// define versions
	vector<Version> versions = {
		{ "version_base", "base (at TODO)", 4, 1 },
		{ "version_db", "this PR (at TODO)", 2, 2 },
	};

	MakeRecoPlots(versions);

	return 0;
}

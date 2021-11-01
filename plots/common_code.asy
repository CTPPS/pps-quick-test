void DrawRatio(RootObject o_num, RootObject o_den, pen p)
{
	guide g;

	for (int bi = 1; bi <= o_num.iExec("GetNbinsX"); ++bi)
	{
		real c = o_num.rExec("GetBinCenter", bi);
		real w = o_num.rExec("GetBinWidth", bi);
		real l = c - w/2.;
		real r = c + w/2.;

		real v_num = o_num.rExec("GetBinContent", bi);
		real v_den = o_den.rExec("GetBinContent", bi);

		if (v_den == 0)
		{
			if (size(g) > 0)
				draw(g, p);

			guide g_new;
			g = g_new;

			continue;
		}

		real rat = v_num / v_den;

		g = g -- (l, rat)--(r, rat);
	}

	if (size(g) > 0)
		draw(g, p);
}

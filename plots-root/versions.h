#ifndef _versions_h_
#define _versions_h_

#include <vector>

using namespace std;

struct Version
{
	string dir;
	string label;
	int color;
	int style;
};

vector<Version> versions = {
    { "version_0", "base (at TODO)", 4, 1 },
    { "version_1", "this PR (at TODO)", 2, 2 },
};

#endif

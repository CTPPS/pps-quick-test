 0) Recommended installation place: in your CMSSW working directory, i.e. in
    * `cd .../CMSSW_X_Y_Z`
    * `git clone git@github.com:CTPPS/pps-quick-test.git -b <branch>`, if you use `CMSSW_12_1_X`, then use branch `12_1` etc.
    * `cd pps-quick-test`

 1) Before editting CMSSW, build plots:
    * `./run_multiple -o version_0`

 2) After making changes to CMSSW, rebuild plots:
    * `./run_multiple -o version_1`

 3) Step 2) can be repeated as many times as desirable. The output/version names can be whatever.

 4) Detailed numerical test of two versions (A and B):
	* run `./compare_multiple <version A> <version B>`

 5) Graphical comparison of standard plots:
	* `cd plots-root`
    * edit file `versions.h`: define the versions (and their line colour/style) you wish to plot
    * run `root -l -q make_plots.cc`: this produces separate PNG files for "reco" and "dirsim" workflow comparisons

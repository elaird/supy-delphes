This project is a satellite of <supy> for Delphes TTrees.
See <github.com/elaird/supy>.

-----------
| License |
-----------
GPLv3 (http://www.gnu.org/licenses/gpl.html)
Note: libDelphes.so is from
http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/spadhi/ECFA/Delphes/Delphes-3.0.10_ECFA_v1.tar.gz

---------------
| Quick Start |
---------------
<set up pyROOT>                                      # eg. with a CMSSW area: cd /<somepath>/CMSSW_5_3_7/src && cmsenv
git clone https://github.com/elaird/supy-delphes.git # clone repo
cd supy-delphes
git submodule update --init                          # checkout supy dependence
source env.sh                                        # add supy directory to your python path; add supy to your path
supy example.py --loop 1                             # run the example

----------------
| Dependencies |
----------------
ROOT (>=5.27.06) and python (2.x, x>=6) are required.

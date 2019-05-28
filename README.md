# matura-stats
Script using API from dane.gov.pl
## How to run it?
1. `pip install requests`
2. Download the file `app_beta.py`
3. Run it: `python3 app_beta.py [commands]`
## What options do I have?
There are three functions:
* `mean` - mean of people entering the matura exam until given year
  * `python3 app_beta.py mean voivodeship year`
  * e.g. `python3 app_beta.py mean dolnośląskie 2015`
* `pass_percent` - pass rate over the years for a given voivodeship
  * `python3 app_beta.py pass_percent voivodeship`
  * e.g. `python3 app_beta.py pass_percent zachodniopomorskie`
* `pass_max` - voivodeship with the best pass rate in a given year
  * `python3 app_beta.py pass_max year`
  * e.g. `python3 app_beta.py pass_max  2012`
## What can be improved?
- [ ] There is some redundant code that can be put into additional function/functions
- [ ] There is no exception handling 
- [ ] Two more features should be implemented

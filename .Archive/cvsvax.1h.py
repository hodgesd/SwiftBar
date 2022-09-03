#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

# <bitbar.title>CVS Vax</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>MajorDouble</bitbar.author>
# <bitbar.author.github>your-github-username</bitbar.author.github>
# <bitbar.desc>Checks CVS for COVID vaccine availability in Belleville IL.</bitbar.desc>
# <bitbar.image>http://www.hosted-somewhere/pluginimage</bitbar.image>
# <bitbar.dependencies>requests, beautiful soup</bitbar.dependencies>
# <bitbar.abouturl>http://url-to-about.com/</bitbar.abouturl>
# <bitbar.droptypes>Supported UTI's for dropping things on menu bar</droptypes.abouturl>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>false</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>false</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>

import requests
from bs4 import BeautifulSoup as BS
import re
import datetime

# CVS source data website to scrape
url = 'https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.IL.json?vaccineinfo'

# GET headers
header ={
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:85.0) Gecko/20100101 Firefox/85.0',
'Accept': '*/*',
'Accept-Language': 'en-US,en;q=0.5',
'Referer': 'https://www.cvs.com/immunizations/covid-19-vaccine',
'Connection': 'keep-alive'
}

# Request results
results = requests.get(url, headers = header)

# Results parsed by BS
soup = BS(results.content, "html.parser" )

# Regex query to find local status
belleville = re.search('BELLEVILLE.+?status":"(.+?)"', soup.text)
asof = re.search('currentTime":"(.+?)"', soup.text)

date_time_str = asof.group(1)
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f')

v = requests.get("https://idph.illinois.gov/DPHPublicInformation/api/COVIDExport/GetVaccineAdministration?countyName=Illinois")

wdata = requests.get("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json")


data = v.json()
t = data[-1]
tVacPct = "{:.1%}".format(t['PctVaccinatedPopulation'])
tRawSome = t['AdministeredCount']
tRawAll = t['PersonsFullyVaccinated']
tRawOne = tRawSome - (tRawAll * 2)
ILpop = 12741080.0
tOnePct = "{:.1%}".format(tRawOne / ILpop)

w = wdata.json()
def function(json_object, name):
    return [obj for obj in json_object if obj['country']==name][0]['data']

us = function(w, 'United States')
usVacPct = us[-1]['people_fully_vaccinated_per_hundred']
usRawAll = us[-1]['people_fully_vaccinated']
usRawSome = us[-1]['total_vaccinations']
usRawOne = usRawSome - (usRawAll * 2)
usPop = 336008333.0
usOnePct = "{:.1%}".format(usRawOne / usPop)

# print('Date:', date_time_obj.date())
# print('Date-time:', date_time_obj)


vaxout = ":worried:"
vaxin = ":smile:"
lastvax = ""
vaxintime = ""

if belleville.group(1) == "Fully Booked":
  status = vaxout
else:
  status = vaxin
  vaxintime = asof
  lastvax = ":exclamation:"



print (":syringe:" + status + lastvax +"| symbolize = false")
# print (":bandage.fill:" + "| symbolize = true"+status)
print ("---")
print (status+" Belleville CVS: "+belleville.group(1) + "| href=https://www.cvs.com/immunizations/covid-19-vaccine#acc_link_content_section_box_251541438_boxpar_accordion_910919113_2")

# print (" | symbolize = false")
print (":exclamation:Last in: " + vaxintime)
print ("---")
print ("IL Vax - Full: %s One: %s | href=https://www.dph.illinois.gov/covid19/vaccinedata?county=Illinois"  % (tVacPct, tOnePct))
print ("US Vax - Full: %s One: %s | href=https://covid.cdc.gov/covid-data-tracker/#datatracker-home"  % (usVacPct, usOnePct))
print ("---")
print('As Of:', date_time_obj.time())

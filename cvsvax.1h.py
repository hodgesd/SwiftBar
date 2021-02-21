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
print (status+" Belleville CVS: "+belleville.group(1))

# print (" | symbolize = false")
print (asof.group(1))
print (":exclamation:Last in: " + vaxintime)

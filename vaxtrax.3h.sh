#!/bin/bash

# <bitbar.title>Vax Trax</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>MajorDouble</bitbar.author>
# <bitbar.author.github>your-github-username</bitbar.author.github>
# <bitbar.desc>Short description of what your plugin does.</bitbar.desc>
# <bitbar.image>http://www.hosted-somewhere/pluginimage</bitbar.image>
# <bitbar.dependencies>none</bitbar.dependencies>
# <bitbar.abouturl>http://url-to-about.com/</bitbar.abouturl>
# <bitbar.droptypes>Supported UTI's for dropping things on menu bar</droptypes.abouturl>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

# Pull current vaccine data from JHU and extract Illinois numbers
ILupdate=$(curl -s https://jhucoronavirus.azureedge.net/jhucoronavirus/state_vaccination_rates.json | sed -E 's/.*"Illinois","data":{"doses_admin":([0-9.]+),"raw_full_vac":([0-9.]+),"percent_full_vac":([0-9.]+),"per100k_full_val":([0-9.]+),"date":([0-9]+).0.*/\1\n\2\n\3\n\4\n\5\n/')

# set the Internal Field Separator to \n
IFS=$'\n'

# Parse Illinois numbers and assign to variables
{ read doses; read vaxed; read vaxedpc; read vaxedp100k; read date; } <<< "${ILupdate}"

# Date calculations
newdate=$(date -r $date)          # Unix epoch date to human readable date
currenttime=$(date +'%s')         # Get current unix epoch date
let datediff="currenttime-date"   # Determent age of data date
message=$(printf '%02dh:%02dm:%02ds\n' $(($datediff/3600)) $(($datediff%3600/60)) $(($datediff%60)))
 

# Header
printf ":cross.case.fill: %.2f%% | dropdown=true" $vaxedpc
echo "---"

# Body

printf "Total Doses Administered: %.0f\n" $doses
echo "As of: $newdate | tooltip=$message ago"
echo "---"
echo "Source: JHU Vaccine Tracker | href=https://coronavirus.jhu.edu/region/us/illinois#vaccine-tracker"

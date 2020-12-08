"""
Used to corroborate collection of county/parish/etc...
FIPS codes from collected data to FIPS codes located
in the "id" attribute of each path on the SVG map
onto which results are to be displayed.

"""

# Relevant library imports
from bs4 import BeautifulSoup
import json, re


# Open results file and load into dictionary
with open('mergedResultsCorrected.json') as results_file:
    results_dict = json.load(results_file)

# Open svg file and load into BeautifulSoup object
with open('usa_counties_large.svg') as usa_svg_file:
    usa_svg_soup = BeautifulSoup(usa_svg_file, 'html.parser')

# Use regular expression to extract path elements that correspond to counties
matches = usa_svg_soup('path', id=re.compile('^(c\d{5})$'))

# Add county FIPS code to list for more convenient checking against map FIPS codes
county_list = []
for state in results_dict:
    for county in results_dict[state]:
        county_list.append(county)

# Keep list of discrepancies between two data sources
discreps_res = []

# Loop through matches from SVG map and record FIPS codes that are not in results set
for match in matches:
    if match['id'][1:] not in county_list:
        discreps.append(match['id'][1:])

## Reverse method checks if county in results is not outlined by a corresponding path in the SVG map ##

# Keep list of discrepancies between two data sources
discreps_map = []

# Loop to compare county FIPS codes in results to county FIPS codes on map
for state_FIPS in results_dict:
    for county_FIPS in results_dict[state_FIPS]:
        county_match_list = usa_svg_soup('path', {'id': f'c{county_FIPS}'})
        if len(county_match_list) != 1:
            discreps_map.append({county_FIPS: len(county_match_list)})
            print({county_FIPS: len(county_match_list)})
        else:
            matches.append(county_FIPS)



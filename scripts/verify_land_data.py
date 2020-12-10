"""
Checks the counties contained in the US Census
Bureau land data spreadsheet against the results
obtained from the election map.

"""

# Relevant library imports
import json, re
import pandas


# Open results file and load into dictionary
with open('mergedResultsCorrected.json') as results_file:
    results_dict = json.load(results_file)

# Add county FIPS code to list for more convenient checking against spreadsheet FIPS codes
county_list = []
for state in results_dict:
    for county in results_dict[state]:
        county_list.append(int(county))

# Import county land data
dfrm = pandas.read_excel('CountyLandData.xlsx')

## Method 1:  Check the US Census data against the election results data ##

# Keep track of discrepancies
discreps1 = []

# Check US Census land data against collected election data
for cell in dfrm['STCOU']:
    # Append discrepancy to list unless state or Alaskan county
    if int(cell) not in county_list and not str(cell).endswith('000') and not (str(cell).startswith('2') and len(str(cell)) == 4):
        discreps1.append(int(cell))

## Method 2:  Check the election results data against the US Census data ##

# Keep track of discrepancies
discreps2 = []

# Check collected election data against US Census land data
for county in county_list:
    # Append discrepancy to list unless Alaskan county
    if county not in list(dfrm['STCOU']) and not (str(county).startswith('2') and len(str(county)) == 4):
        discreps2.append(county)


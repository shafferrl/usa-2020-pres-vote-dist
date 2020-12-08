"""
Uses US Census data to add land area data to each county
included in results set of collected election data and
also adds computed values for county voter density and
county voter density normalized as a fraction of the most
dense county's population.

Since land area data is from 2010, counties that have either
had their FIPS codes reassigned or been dissolved into other
counties are also dealt with accordingly herein.

"""

# Relevant library imports
import json, re
import pandas
from operator import itemgetter

# Open results file and load into dictionary
with open('mergedResultsCorrected.json') as results_file:
    results_dict = json.load(results_file)

# Open file for dealing with defunct counties and load into dictionary
with open('defunctCountyLandMgmt.json') as defnct_mgmt:
    defnct_mgmt_dict = json.load(defnct_mgmt)

# Load census land area data into pandas dataframe
co_lnd_df = pandas.read_excel('CountyLandData.xlsx')

# Keep list if any counties slipped through the cracks
census_slipthroughs = []
results_slipthroughs = []

# Keep list of counties to be sorted by density when all results obtained
counties_by_density = []

# Loop through all relevant FIPS counties, excluding states
for co_FIPS in list(co_lnd_df['STCOU']):
    # FIPS codes in dataframe evenly divisible by 1000 are states, also exlcude Alaskan counties for now
    if not co_FIPS % 1000 == 0 and not ( str(co_FIPS).startswith('2') and len(str(co_FIPS)) == 4 ):
        # All relevant county FIPS codes that don't start with zero
        if len(str(co_FIPS)) == 5:
            co_FIPS_str = str(co_FIPS)
        # FIPS codes in dataframe starting with a zero are numbers, so leading zero needs to be replaced
        else:
            co_FIPS_str = '0' + str(co_FIPS)

        # Get the land area of the county
        co_lnd_area = co_lnd_df.loc[co_lnd_df.STCOU == co_FIPS, 'LND110210D'].values[0]

        # County FIPS code is present in the vote results
        if results_dict[co_FIPS_str[:2]].get(co_FIPS_str, None):
            # Land area has not yet been logged
            if not results_dict[co_FIPS_str[:2]][co_FIPS_str].get('land_area', None):
                results_dict[co_FIPS_str[:2]][co_FIPS_str]['land_area'] = co_lnd_area
            # There is already an entry for land area in the county
            else:
                results_dict[co_FIPS_str[:2]][co_FIPS_str]['land_area'] += co_lnd_area
        # County FIPS code is not present in the vote results
        else:
            # If county FIPS code has changed to another one
            if defnct_mgmt_dict['changed_to'].get(co_FIPS_str, None):
                results_dict[co_FIPS_str[:2]][defnct_mgmt_dict['changed_to'][co_FIPS_str]]['land_area'] = co_lnd_area
            # If county FIPS code has been rolled into existing county
            elif defnct_mgmt_dict['merged_into'].get(co_FIPS_str, None):
                # List of counties that are absorbing the now-defunct county
                absrbng_cos_lst = defnct_mgmt_dict['merged_into'][co_FIPS_str]
                # Approximate added land area to absorbing counties by equally dividing now-defunct by number absorbing
                for absrbd_by_co in absrbng_cos_lst:
                    # There isn't yet an entry for the county's land area
                    if not results_dict[co_FIPS_str[:2]][absrbd_by_co].get('land_area', None):
                        results_dict[co_FIPS_str[:2]][absrbd_by_co]['land_area'] = co_lnd_area / len(absrbng_cos_lst)
                    # County already has an entry for land area
                    else:
                        results_dict[co_FIPS_str[:2]][absrbd_by_co]['land_area'] += co_lnd_area / len(absrbng_cos_lst)
            # If no inclusion method can be found for county
            else:
                slipthroughs.append({'co_FIPS': co_lnd_area})

# Loop through the results and calculate the voter density in the county
for state in results_dict:
    for county in results_dict[state]:
        # County does not have land area data
        if not results_dict[state][county].get('land_area', None):
            results_slipthroughs.append(county) # deal with later
        # There is a land area entry for the county
        else:
            # Initialize vote totals to zero
            co_voter_total = 0
            co_alt_total = 0; co_dem_total = 0; co_rep_total = 0
            # Parse results for each candidate's vote totals
            for cand_votes in results_dict[state][county]['results']:
                # Exclude the "scraped_name" key, which is used for verification of county's data
                if cand_votes != 'scraped_name':
                    # Look inside each sub-dictionary / object, name strings are consistent throughout dataset
                    no_cand_votes = int(''.join(results_dict[state][county]['results'][cand_votes]['vote_count'].split(',')))
                    co_voter_total += no_cand_votes
                    if 'Biden' in results_dict[state][county]['results'][cand_votes]['name']:
                        co_dem_total += no_cand_votes
                    elif 'Trump' in results_dict[state][county]['results'][cand_votes]['name']:
                        co_rep_total += no_cand_votes
                    # Roll all third-party votes into one total for each county
                    else:
                        co_alt_total += no_cand_votes

            # Add newly tallied and computed values to results dictionary
            results_dict[state][county]['voter_total'] = co_voter_total
            results_dict[state][county]['voter_density'] = round(co_voter_total / results_dict[state][county]['land_area'], 4)
            results_dict[state][county]['vote_ratios'] = {
                "Biden": round(co_dem_total / co_voter_total, 4),
                "Trump": round(co_rep_total / co_voter_total, 4),
                "other": round(co_alt_total / co_voter_total, 4)
            }
            # Add county to list so that its order of density can be sorted out once all results have been collected
            counties_by_density.append({'FIPS': county, 'voter_density': results_dict[state][county]['voter_density']})

# Sort counties by density with first in list being densest
counties_by_density = sorted(counties_by_density, key=itemgetter('voter_density'), reverse=True)

# Loop through the counties again and include parameter for density relative to densest district
for state in results_dict:
    for county in results_dict[state]:
        try:
            results_dict[state][county]['rel_density'] = round(results_dict[state][county]['voter_density'] / counties_by_density[0]['voter_density'], 6)
        except: continue

# Save results to JSON file
with open('resultsWithComputedData.json', 'w') as computed_res_file:
    computed_res_file.write(json.dumps(results_dict, indent=4))
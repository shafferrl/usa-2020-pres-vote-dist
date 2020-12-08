import json

with open('CountyFIPS.json') as county_json_file:
    county_dict = json.load(county_json_file)

#county_tally = 0
#for state_code in county_dict:
    #county_tally += len(county_dict[state_code])
    #print(len(county_dict[state_code]))

print(county_dict['56'])
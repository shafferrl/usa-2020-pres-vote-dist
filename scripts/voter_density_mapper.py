"""
Takes US election and census data from JSON file and SVG map of counties/parishes/municipalities
corresponding to 5-digit FIPS codes to create new maps visualizing information about political 
leanings and "voter density" (normalized to densest county) of each respective municipality.

"County" herein refers to any county, parish, city, etc... that is represented by a 5-digit
FIPS (Federal Information Processing Standard) code and for which data was collected.

"""

# Relevant library imports
from bs4 import BeautifulSoup
import json, re, math

# Open JSON results and load into dictionary
with open('../Results/Final/json/resultsWithComputedData.json') as computed_res_file:
    results_dict = json.load(computed_res_file)

# Put county FIPS codes into list for searching
results_list = []
for state in results_dict:
    for county in results_dict[state]:
        if not county.startswith('02'):
            results_list.append(county)

# Open and load various formats for presenting the data
with open('../Resources/json/mapFormats.json') as img_format_json:
    image_formats = json.load(img_format_json)

# Loop through each variation of data presentation
for img_format in image_formats:
    # Open original SVG image and convert to BeautifulSoup object for easy parsing
    usa_svg_soup = BeautifulSoup(open('../Sources/svg/usa_counties_large.svg'), 'html.parser')
    # Use regex to collect list of all SVG path elements that correspond to counties
    FIPS_matches = usa_svg_soup('path', id=re.compile('^(c\d{5})$'))

    # Loop through the list of counties found in the SVG image
    for match in FIPS_matches:
        # Don't include counties for which there are no results
        if match['id'][1:] in results_list:
            # No density representation
            if not img_format['opacity_adj']:
                fill_opacity = '1'
            # Linear representation
            elif img_format['opacity_adj'] == 1:
                fill_opacity = str(round(results_dict[match['id'][1:3]][match['id'][1:]]['rel_density'], 3))
            # Quadratic bezier adjustment
            elif img_format['opacity_adj'] == 2:
                var_ind = results_dict[match['id'][1:3]][match['id'][1:]]['rel_density']
                bezier_pt = var_ind + 2 * math.sqrt(var_ind)
                fill_opacity = str(round(bezier_pt, 2))
            # Cubic bezier adjustment
            elif img_format['opacity_adj'] == 3:
                var_ind = results_dict[match['id'][1:3]][match['id'][1:]]['rel_density']
                #bezier_pt = ( 1.5 * var_ind ** (1/3) - (1/162) * var_ind ** (3/2) - (40/81) * var_ind )
                bezier_pt = (91/81) * ( (3/2) * var_ind ** (1/3) - (1/3) * var_ind ** (2/3) - (5/18) * var_ind )
                fill_opacity = str(round(bezier_pt, 2))

            co_vote_ratios = results_dict[match['id'][1:3]][match['id'][1:]]['vote_ratios']

            # Image format displays political leanings and blue candidate gets more votes than or equal votes to red candidate
            if img_format['red'] is None and co_vote_ratios['Biden'] >= co_vote_ratios['Trump']:
                blue = '255'
                red = str(int(255 * (co_vote_ratios['Trump']/co_vote_ratios['Biden'])))
            # Image format displays political leanings and blue candidate less votes than red candidate
            elif img_format['red'] is None and co_vote_ratios['Biden'] < co_vote_ratios['Trump']:
                red = '255'
                blue = str(int(255 * (co_vote_ratios['Biden']/co_vote_ratios['Trump'])))
            # Image formats not displaying political leanings
            else:
                red = '0'
                blue = '0'

            # Modify attributes of relevant county path
            match['fill'] = 'rgba('+ red +',0,'+ blue +',' + fill_opacity + ')'  # rgba(255, 255, 255, 1)
            match['stroke-width'] = '.04'
            match['stroke'] = 'black'

    # Modify the path defining the state borders
    state_borders = usa_svg_soup('path', id="borders")
    state_borders[0]['style'] = 'fill:none;stroke-width:.2;'
    state_borders[0]['stroke'] = 'black'

    # Convert BeautifulSoup object to string for saving
    new_svg = str(usa_svg_soup)

    # Write SVG image to file
    file_path = '../Results/Final/svg/'
    with open(file_path + img_format['name'] + '.svg' ,'w') as svg_map_file:
        svg_map_file.write(new_svg)

    ### Embed SVG image into HTML template to include basic annotations ###

    # Open and load html to prepend to SVG image
    with open('../Resources/html/map_page_format.html') as map_format_html:
        map_pre_html = ''
        for line in map_format_html:
            map_pre_html += map_format_html.read()

    # Create html with SVG embedded
    html_start = map_pre_html + img_format['title'] +'</h2>'
    new_svg_html = html_start + img_format['spec_html'] + new_svg +'<p class="img-blurb">'+ img_format['blurb'] +'</p></div></body></html>'
    
    # Write HTML image to file
    file_path = '../Results/Final/html/'
    with open(file_path + img_format['name'] + '.html' ,'w') as html_map_file:
        html_map_file.write(new_svg_html)

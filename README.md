# usa-2020-pres-vote-dist
Maps visualizing US 2020 election results by county, accounting for major candidates' vote percentages and county voter density.
Scripts relating to data collection and raw JSON data have been omitted from this repository.


## Data Collection ##

The SVG image files in this repository display the results of the 2020 US presidential election as reported by the Associated Press 
on Nov. 29, 2020 and Dec. 1, 2020 when the data were collected.  Some of the data that were not able to be to obtained through the primary
collection method were obtained from various state elections websites.

AP Source:
https://interactives.ap.org/elections-2020/?date=2020-11-03&site=19bcbd7a-edff-4356-8f26-1aba549558b8&map=geo

In the interest of preventing abuse, the Python script that was used to collect the data has been omitted from this repository, but it
will be available upon request if the party making the request has a compelling reason to see it and can be expected not to use it for
abusive purposes.  At the time the vote tallies were collected, there was ostensibly no public API providing the data with granularity
to the county level and with all the states' counties collated in one location.

Land area data were collected from the US Census Bureau via an Excel spreadsheet at the following link:
https://www.census.gov/library/publications/2011/compendia/usa-counties-2011.html

The SVG image at the following Wikipedia page was saved and modified to display the results:
https://upload.wikimedia.org/wikipedia/commons/5/59/Usa_counties_large.svg

Due to the AP's reporting of Alaska as a state total rather than on a per-county basis, Alaska's election website reporting results in
a manner that does not align with the boundaries of the FIPS counties shown in the SVG image obtained from Wikipedia, the relatively 
massive land area of Alaska compared to other states, and the relatively low population of Alaska, its results have been omitted from
the generated maps for the time being.


## Presentation of Results ##

The data have been presented in the following formats:

1) Voter Distribution (voter_dist):  
    Political leanings by county without voter/population density included.  Red color component represents the fraction of 
    Republican votes, and blue color component represents the fraction of Democratic votes.
    
2) Voter Density, Linear (voter_dnsty_linear): 
    Linear visualization of voter density in each county normalized to most voter-dense county (NY County, FIPS 36061).
    Map does not display relative political leanings, density shown via grayscale. Alpha channel represents normalized density.

3) Voter Distribution & Density, Linear (voter_dist_dnsty_linear): 
    Linear visualization of voter density (normalized) with political leanings in each county using RGBA color definition and
    same representations (combined) as described in 1) and 2).

4) Voter Density, Quadratic-Bezier-Adjusted (voter_dnsty_bez_quadr):
    Visualization of voter density (normalized) without political leanings in grayscale.  Alpha channel has been adjusted 
    so that density maps to opacity via the following equation: opacity = -density + 2 * sqrt(density)

5) Voter Distribution & Density, Quadratic-Bezier-Adjusted (voter_dist_dnsty_bez_quadr):
    Visualization of voter density (normalized) with political leanings in each county using RGBA color definition and
    same representations (combined) as described in 1) and 2).  Alpha channel has been adjusted according to quadratic bezier
    curve defined in 4).

6) Voter Density, Cubic-Bezier-Adjusted (voter_dnsty_bez_cubic):
    Visualization of voter density (normalized) without political leanings in grayscale.  Alpha channel has been adjusted 
    so that density maps to opacity via the cubic quasi-bezier curve following equation: 
    opacity = (91/81) * ( (3/2) * density ^ (1/3) - (1/3) * density ^ (2/3) - (5/18) * density )
 
7) Voter Distribution & Density, Cubic-Bezier-Adjusted (voter_dist_dnsty_bez_cubic):
    Visualization of voter density (normalized) with political leanings in each county using RGBA color definition and
    same representations (combined) as described in 1) and 2).  Alpha channel has been adjusted according to cubic 
    quasi-bezier curve defined in 6).


Note: Votes for third-party candidates have been included in voter density calculations but excluded from calculating color
values.  Using RGBA color on a white background, with red and blue representing the Republican and Democratic candidates,
respectively, would leave only the green color channel for third-party candidates, whose inclusion would (slightly) bring
the resulting color closer to white, negating the effect of votes adding to opacity.  Third-party and write-in candidates
also comprised a very small percentage of the vote totals and have thusly been excluded.  Write-in candidates have not been
included in any results calculations.
    


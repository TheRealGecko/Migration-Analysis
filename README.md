# Migration-Analysis
## Analyzing North-East Canadian geese migration trends using pandas
Seeing the geese in Waterloo got me thinking, where do they go anyways? While I couldn't find a dataset on Waterloo geese to answer the question for myself, I was able to find a dataset on (North-East American Canadain geese)[https://www.movebank.org/cms/webapp?gwt_fragment=page%3Dstudies%2Cpath%3Dstudy2105214573] with 1680000+ data points to analyze.

## Questions I wanted answered
- What does their migration route look like?
- Where do majority of geese tend to reside/lay-over in?
- What months have the most geese movement?

### What does their migration route look like?
To answer this, I created a visualization of the dataset using pandas and plotly
- Data is blocked into intervals of 3 days to reduce data points, reducing strain on program
- Data is mapped starting from 2017-08-08 due to the lack of data points from 2015-2017
![map preview](results\map_preview.png)
View the mapping (here)[]

## Where do majority of geese tend to reside/lay-over in?
To answer this, I generalized each latidue/lognitude coordinate as a city/region, and found the most common occurances of the cities/regions. Here are the results:
1) Vaughan, ON
2) Baie-d'Hudson, Quebec (specifically around (59.9, -77.4)) 
3) Baie-d'Hudson, Quebec (specifically around (59.4, -77.7))
4) Syosset, New York, USA
5) Pineville, Pennsylvania, USA

Notes on the process:
- Originally I was going to find each city/region for each data point using geopy, but I ran into a blocker:
 - Would require me to send several hundered to thousand API requests to geopy- inefficient and unethical
 - Would require me to significantly reduce the amount of data points to reduce the API requests to a managable amount
- Instead, performed the following:
 - Rounded longitude/latitiude values to the nearest 0.1 to get ~11km resolution for city level precision
 - Counted top 5 repeating cities/regions
 - Plugged 5 repeating regions into Google Maps to retrive the names of the actual locations

## What months have the most geese movement?
Steps to determine this:
- Sum the distance travelled over several 3 day interval throughout each month per geese 
- Take the average of all the geese per each month
![map preview](results\movement_per_month.png)

Notes on the processs:
- Originally geopy's distance function was to be used to calculate distances between points, but due to the volume of data points to analyze, the process was taking too long
- Resolved this by implementing a cutom distance function 

# topcitywikiscraper

Wikipedia webscraper for information on the top cities in the US. Used to parse for city data on population, population density, and other geographic features. Can be modified to scrape for more data.

There appears to be a linear positive correlation between population density of a city and the amount of outgoing links that the respective city has on its Wikipedia page. It seams that the more densily populated an area, the more attractions there are in the city. Clear example is New York City who has a steap advantage in both population density and number of outgoing links. An overwhelming majority of the top cities in the US by population appear to allign with the democratic party. This further supports the claim that political rivalry between Democrats and Republicans sources differences from rural vs. urban demographics.

Python Packages Required: pandas, bs4, requests, os

To Run: 

1. Open Terminal
2. Navigate to Folder containing scrape.py
3. Run command: python scrape.py

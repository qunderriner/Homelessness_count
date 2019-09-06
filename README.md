# Homelessness_count
Overall Project Goal: We want to study which economic factors drive increasing homelessness rates to be able to better target homelessness policy. 

Why is what we are doing novel?: When this kind of analysis is typically done, it does not include the HIC PIT count. This is a measure of the permanently housed homeless population. Excluding this figure (which is often done due to the complexity of the data) means that analysis that just looks at the sheltered and unsheltered homeless population is incomplete. If city A has good homeless policy and puts 20k people into permanent housing in a year, and city B only puts in 2k, this would skew the overall homeless figures in a way that would make it harder to see at what rate people were becoming homeless in a given city. Further, this analysis is rarely done across so many (19, currently) cities (more specifically, combined statistical areas (CSAs)) due again to the complexity in how the data is reported.

Process: HUD releases homeless figures here (https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/), including the HIC PIT count. To get this data aggregated to the CSA level we need to do some data manipulation and geocoding, described here. 

The HIC PIT count data in the HUD report is aggregated to the Continuum of Care (CoCs) level. A CoC is a regional or local planning body that coordinates housing and services funding for homeless families and individuals. In some cities, notably those in California, these CoCs map to counties (which we can use to validate our approach). We are doing a nationwide study however, and in most cases these CoCs do not map cleanly to anything, so we need to dig deeper into the data to figure out which are in a given CSA. We are focusing on 19 of the largest CSAs. 

In the HUD data there are varying amounts of information about a given facility in a CoC. In a majority of cases we are given a physical address, but in some cases the address data needs to be cleaned to be able to used. I wrote a script that parses which of the addresses are good or able to be cleaned and writes those to a csv. It then takes the files that provide only a zip code (e.g., no actual address provided) and separates those into another CSV. Finally, there are a small fraction of locations for which there is no address information provided. These are put in a separate CSV and we look up the organization on the internet to hand code an address. From those we were able to hand code, we separate those for which we could find a valid address to be with the other valid addresses and those for which we could only find a zip code. We then geocode these two files separately in ArcGIS, in both cases matching each facility, and its associated HIC PIT count, to a CSA.

Once each HIC PIT count can be mapped to a CSA we rejoin the data and augment it with data from the ACS (reported at the CSA level) and Zillow data (reported at the metropolitan statistical area (MSA) level, which can be mapped to CSAs). We then start our analysis. 

HOW TO USE THESE FILES:

Unfortunetly, some elements of this work cannot be automated (geocoding with ArcGIS, manually filling in some missing data) so there is some input needed (as well as some changing of hardcoded dates as you process data from different years). This is generally how the files fit together:

Split_data.py - reads in PIT data from a CSV downloaded from this hud https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/ site. Main thing to change here is the hardcoded pit_data_csv filepath for data from the above link. 



Homeless Pit Count Exploratory Analysis .ipynb: as the name suggests, is some initial exploratory work with the data. 

the Final_Data folder contains the output of running through this process on 2017 data (eg, it contains mapping of CSAs to PIT Count data, some ACS and Zillow Data) 

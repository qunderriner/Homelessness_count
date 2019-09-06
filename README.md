# Homelessness_count
Overall Project Goal: We want to study which economic factors drive increasing homelessness rates to be able to better target homelessness policy. 

Why is what we are doing novel?: When this kind of analysis is typically done, it does not include the HIC PIT count. This is a measure of the permanently housed homeless population. Excluding this figure (which is often done due to the complexity of the data) means that analysis that just looks at the sheltered and unsheltered homeless population is incomplete. If city A has good homeless policy and puts 20k people into permanent housing in a year, and city B only puts in 2k, this would skew the overall homeless figures in a way that would make it harder to see at what rate people were becoming homeless in a given city. Further, this analysis is rarely done across so many (20, currently) cities (more specifically, combined statistical areas (CSAs)) due again to the complexity in how the data is reported.

Process: HUD releases homeless figures here (https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/), including the HIC PIT count. To get this data aggregated to the CSA level we need to do some data manipulation and geocoding, described here. 

The HIC PIT count data in the HUD report is aggregated to the Continuum of Care (CoCs) level. A CoC is a regional or local planning body that coordinates housing and services funding for homeless families and individuals. In some cities, notably those in California, these CoCs map to counties (which we can use to validate our approach). We are doing a nationwide study however, and in most cases these CoCs do not map cleanly to anything, so we need to dig deeper into the data to figure out which are in a given CSA. We are focusing on 20 of the largest CSAs. 

In the HUD data there are varying amounts of information about a given facility in a CoC. In a majority of cases we are given a physical address, but in some cases the address data needs to be cleaned to be able to used. I wrote a script that parses which of the addresses are good or able to be cleaned and writes those to a csv. It then takes the files that provide only a zip code (e.g., no actual address provided) and separates those into another CSV. Finally, there are a small fraction of locations for which there is no address information provided. These are put in a separate CSV and we look up the organization on the internet to hand code an address. From those we were able to hand code, we separate those for which we could find a valid address to be with the other valid addresses and those for which we could only find a zip code. We then geocode these two files separately in ArcGIS, in both cases matching each facility, and its associated HIC PIT count, to a CSA.

Once each HIC PIT count can be mapped to a CSA we rejoin the data and augment it with data from the ACS (reported at the CSA level) and Zillow data (reported at the metropolitan statistical area (MSA) level, which can be mapped to CSAs). We then start our analysis. 

HOW TO USE THESE FILES:
(numbers indicate order to call files if starting this process from scratch. some are not numbered as they are called only by other fuctions).

Unfortunetly, some elements of this work cannot be automated (geocoding with ArcGIS, manually filling in some missing data, zillow economic data) so there is some input needed (as well as some changing of hardcoded dates as you process data from different years). This is generally how the files fit together:

1. Split_data.py - reads in PIT data from a CSV downloaded from this hud https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/ site. Main thing to change here is the hardcoded pit_data_csv filepath for data from the above link. This file will produce 3 CSV files from the HUD data: good addresses (those that are ready for geocoding with ArcGIS or something similiar), addresses that only contain zip codes (and not street addresses) and those files that do not contain address information. Ideally, the latter is a small number, and based on the name of the organization, can be manually filled out.

2. read_and_aggregate_final.py - After manually filling in addresses as mentioned above, this file takes in the good address and zip files from Split_data.py, as well as the manually fixed csv, and outputs two CSVs, a new good addresses file and a zipcode only file. 

3. Post_geocoding.py: 
The good addresses file should be geocoded to CSAs using the intersect feature on ArcGIS. In the data file there is a file that has a mapping of all zip codes to CSAs (zip_code_csa_mapping_only_clean.csv - created using ArcGIS), which is used in this function to create a mapping between the zipcode only file and the CSAs. This file will do this mapping, and merge the data with the good address data from Zillow. This file then groups the data and outputs a csv with a mapping of HIC PIT counts to CSAs. 

4. Pull_it_together.py - this file will take the mapping of CSAs to HIC PIT counts output from Post_geocoding and augment it with CSA level data from ACS data and Zillow, outputing a csv with this completed data set. It calls the files Zillow.py and ACS_v2.py, described below. 

Zillow.py - currently pulling data on rental cost to income ratio, housing costs, rental cost, and median income. need to download csvs (https://www.zillow.com/research/data/) and follow instructions in file if you want to add more zillow data. 

ACS_v2 - change code (in B01003_001E form) in both codes dictionary (this just does collumn naming) and in the "url" API call if you want different figures. Change hardcoded year at the top to get data from a different year. 

Homeless Pit Count Exploratory Analysis .ipynb: as the name suggests, is some initial exploratory work with the data. 

the Final_Data folder contains the output of running through this process on 2017 data (eg, it contains mapping of CSAs to PIT Count data, some ACS and Zillow Data) 

email qunderriner@gmail.com with any questions. 

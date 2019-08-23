import requests 
import pandas as pd 
import re 

pit_data_csv = "2017-Housing-Inventory-Count-Raw-File (3).xlsx" #PIT data comes from here: https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/ no api sadly 
#Note: Only the odd numbered years are used in this anaysis as even numbered years are only estimates, not actual counts.
address_data = ("Intersect1_0.csv")#add location here of file with correct mapping of pit counts to CSAs after having been geocoded 
pro_type = ["PSH","RRH","OPH"]

#year = 2017 #turn this on 

matches = ("CA-600",
"WI-500","IN-502",
"IL-512","VA-514",
"VA-521","WV-508",
"VA-513","MD-511",
"NH-500","TX-607",
"TX-624","OK-507",
"DE-500","NJ-503",
"FL-517","GA-501",
"MI-500","WA-501",
"MN-505","MN-502",
"MN-511","CO-500",
"OH-507","FL-520", 
"OR-505", "WA-501")#note this is just for the problomatic subset, the actual list of HudNumbers is actually much higher 

csa_filter = ["NY-Newark, NY-NJ-CT-PA CSA",
			"Los Angeles-Long Beach, CA CSA",
			"Chicago-Naperville, IL-IN-WI CSA",
              "Washington-Baltimore-Arlington, DC-MD-VA-WV-PA CSA",
             "San Jose-San Francisco-Oakland, CA CSA",
              "Boston-Worcester-Providence, MA-RI-NH-CT CSA",
              "Dallas-Fort Worth, TX-OK CSA",
              "Philadelphia-Reading-Camden, PA-NJ-DE-MD CSA",
              "Houston-The Woodlands, TX CSA",
              "Miami-Fort Lauderdale-Port St. Lucie, FL CSA",
              "Atlanta--Athens-Clarke County--Sandy Springs, GA CSA",
              "Detroit-Warren-Ann Arbor, MI CSA",
              "Seattle-Tacoma, WA CSA",
              "Minneapolis-St. Paul, MN-WI CSA",
              "Denver-Aurora, CO CSA",
              "Cleveland-Akron-Canton, OH CSA",
              "Orlando-Deltona-Daytona Beach, FL CSA",
              "Portland-Vancouver-Salem, OR-WA CSA"]

codes = {
	"NAME":"CSA",
	'B01003_001E':'population',
	'B25064_001E':'median_rent',
	"B25065_001E":"aggregate_gross_rent",
	"B25004_002E":"estimate_total_for_rent",
	"B23025_001E":"total_employement_status",
	"B23025_002E":"total_in_labor_force",
	"B25001_001E":"total_number_units",
	"B25014_013E":"two_or_more_occupants_per_room",
	"B25058_001E":"median_contract_rent",
	"combined statistical area":"combined statistical area"
}
    #8_21 NEW renter divided by total number of houses to get numbrer of renters


    B07013_003E (Estimate!!Total!!Householder lived in renter-occupied housing units)/B07013_001E (total households)

cols_to_keep = ["CoC", "HudNum", "address1", "city", "zip", "Project ID", "Project Type", "PIT Count"]


url = "https://api.census.gov/data/2017/acs/acs5?get=NAME,B01003_001E,B25064_001E,B25065_001E,B25004_002E,B23025_001E,B25001_001E,B25014_013E,B25058_001E&for=combined%20statistical%20area:*"



def get_data(year):
	"""
	Load data from API
	inputs:
		url (str)
	"""
	#url = "https://api.census.gov/data/"+year+"/acs/acs5?get=NAME,B01003_001E,B25064_001E,B25065_001E,B25004_002E,B23025_001E&for=combined%20statistical%20area:*"
	response = requests.get(url)
	data_1 = pd.DataFrame(response.json())

	return data_1 

def make_header(df):
	new_header = df.iloc[0] #grab the first row for the header
	df = df[1:] #take the data less the header row
	df.columns = new_header
	df.columns = [codes[x] for x in df.columns]
	df = df.drop(columns=['combined statistical area'])	
	return df 

def pull_acs_data(url,year):
	"""
	add as string which one year ACS estimate you want. 
	"""
	df = get_data(year)
	df = make_header(df)
	df = df[df['CSA'].isin(csa_filter)]
	return df 

def merge_data(df,year):
	#pit_counts = pd.read_csv(address_data)
	pit_counts = df 
	pit_counts = pit_counts[["NAMELSAD","PIT Count"]]
	pit_counts = pit_counts[pit_counts['NAMELSAD'].isin(csa_filter)]
	pit_counts = pit_counts.groupby("NAMELSAD").sum().reset_index()
	pit_counts = pit_counts.rename(columns={"NAMELSAD": "CSA"})
	acs = pull_acs_data(url,year)
	merged = pit_counts.merge(acs, on='CSA')
	merged["two_or_more_occupants_per_room"] = merged["two_or_more_occupants_per_room"].astype(int)
	merged["total_number_units"] = merged["total_number_units"].astype(int)
	merged["estimate_total_for_rent"] = merged["estimate_total_for_rent"].astype(int)
	merged["overcrowded"] = merged["two_or_more_occupants_per_room"]/ merged["total_number_units"]
	merged["Percent_of_Market_for_Rent"] = merged["estimate_total_for_rent"] /merged["total_number_units"]
	#merged = merged.drop(columns=['Unnamed: 0'])
	return merged 






def go():

"""
#B25064	MEDIAN GROSS RENT (DOLLARS)
B25065_001E	Estimate!!Aggregate gross rent	AGGREGATE GROSS RENT (DOLLARS)

B25014_001E TENURE BY OCCUPANTS PER ROOM

B19051	EARNINGS IN THE PAST 12 MONTHS FOR HOUSEHOLDS
B25014_002E	Estimate!!Total!!Owner occupied

B25004_002E	Estimate!!Total!!For rent	VACANCY STATUS


B25058_001E	Estimate!!Median contract rent

B23025_001E	Estimate!!Total	EMPLOYMENT STATUS FOR THE POPULATION 16 YEARS AND OVER


B20018_001E	Estimate!!Median earnings in the past 12 months (in 2017 inflation-adjusted dollars)	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2017 INFLATION-ADJUSTED DOLLARS) FOR THE POPULATION 16 YEARS AND OVER WHO WORKED FULL-TIME, YEAR-ROUND WITH EARNINGS IN THE PAST 12 MONTHS

B20004	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2017 INFLATION-ADJUSTED DOLLARS) BY SEX BY EDUCATIONAL ATTAINMENT FOR THE POPULATION 25 YEARS AND OVER

B20017	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2017 INFLATION-ADJUSTED DOLLARS) BY SEX BY WORK EXPERIENCE IN THE PAST 12 MONTHS FOR THE POPULATION 16 YEARS AND OVER WITH EARNINGS IN THE PAST 12 MONTHS


t_data(url):
	"""

	"""
	response = requests.get(url)
	data_1 = pd.DataFrame(response.json())
	return data_1 

def clean_data(df):
	new_header = df.iloc[0] #grab the first row for the header
	df = df[1:] #take the data less the header row
	df.columns = new_header
	df.columns = [codes[x] for x in df.columns]
	df = df.drop(columns=['combined statistical area'])
	df_df = df[df['CSA'].isin(csa_filter)]	
	return df 

def merge_with_pit(census_data, pit_data_csv):

	return df 


estimate_total_for_rent is number of vacant units, should normalize over population (already collected) or total number of units (B25001_001E)? could do both 

"name": "B23025_002E",
  "label": "Estimate!!Total!!In labor force",
  "concept": "EMPLOYMENT STATUS FOR THE POPULATION 16 YEARS AND OVER", could use this and then normalize by population 


B25014_013E	Estimate!!Total!!Renter occupied!!2.01 or more occupants per room - could divide by B25014_001E	Estimate!!Total	TENURE BY OCCUPANTS PER ROOM

B25056_001E	Estimate!!Total	CONTRACT RENT



  Total population
Below poverty level
Renters
Median earnings
Occupants per room
Owner occupied units
Rental vacancy rate
Mean rent asked
Median monthly housing costs
Median contract rent
Unemployment rate
"""




"""
estimate_total_for_rent is number of vacant units, should normalize over population (already collected) or total number of units (B25001_001E)? could do both 

"name": "B23025_002E",
  "label": "Estimate!!Total!!In labor force",
  "concept": "EMPLOYMENT STATUS FOR THE POPULATION 16 YEARS AND OVER", could use this and then normalize by population 


B25014_013E	Estimate!!Total!!Renter occupied!!2.01 or more occupants per room - could divide by B25014_001E	Estimate!!Total	TENURE BY OCCUPANTS PER ROOM

B25056_001E	Estimate!!Total	CONTRACT RENT


#B25064	MEDIAN GROSS RENT (DOLLARS)
B25065_001E	Estimate!!Aggregate gross rent	AGGREGATE GROSS RENT (DOLLARS)

B25014_001E TENURE BY OCCUPANTS PER ROOM

B19051	EARNINGS IN THE PAST 12 MONTHS FOR HOUSEHOLDS
B25014_002E	Estimate!!Total!!Owner occupied

B25004_002E	Estimate!!Total!!For rent	VACANCY STATUS


B25058_001E	Estimate!!Median contract rent

B23025_001E	Estimate!!Total	EMPLOYMENT STATUS FOR THE POPULATION 16 YEARS AND OVER


B20018_001E	Estimate!!Median earnings in the past 12 months (in 2017 inflation-adjusted dollars)	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2017 INFLATION-ADJUSTED DOLLARS) FOR THE POPULATION 16 YEARS AND OVER WHO WORKED FULL-TIME, YEAR-ROUND WITH EARNINGS IN THE PAST 12 MONTHS

B20004	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2017 INFLATION-ADJUSTED DOLLARS) BY SEX BY EDUCATIONAL ATTAINMENT FOR THE POPULATION 25 YEARS AND OVER

B20017	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2017 INFLATION-ADJUSTED DOLLARS) BY SEX BY WORK EXPERIENCE IN THE PAST 12 MONTHS FOR THE POPULATION 16 YEARS AND OVER WITH EARNINGS IN THE PAST 12 MONTHS
"""

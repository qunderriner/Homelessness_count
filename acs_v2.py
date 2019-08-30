import requests 
import pandas as pd 
import re 

pit_data_csv = "CSA_Zillow_Pit_Data_Merged.csv" #file with correct mapping of pit counts to CSAs
year = "2017" #year you want ACS data for - note that 

csa_filter = ['New York-Newark, NY-NJ-CT-PA CSA',
 'Los Angeles-Long Beach, CA CSA',
 'Chicago-Naperville, IL-IN-WI CSA',
 'Washington-Baltimore-Arlington, DC-MD-VA-WV-PA CSA',
 'San Jose-San Francisco-Oakland, CA CSA',
 'Boston-Worcester-Providence, MA-RI-NH-CT CSA',
 'Dallas-Fort Worth, TX-OK CSA',
 'Philadelphia-Reading-Camden, PA-NJ-DE-MD CSA',
 'Houston-The Woodlands, TX CSA',
 'Miami-Fort Lauderdale-Port St. Lucie, FL CSA',
 'Atlanta--Athens-Clarke County--Sandy Springs, GA CSA',
 'Detroit-Warren-Ann Arbor, MI CSA',
 'Seattle-Tacoma, WA CSA',
 'Minneapolis-St. Paul, MN-WI CSA',
 'Denver-Aurora, CO CSA',
 'Cleveland-Akron-Canton, OH CSA',
 'Orlando-Deltona-Daytona Beach, FL CSA',
 'Portland-Vancouver-Salem, OR-WA CSA',
 'Sacramento-Roseville, CA CSA',
 'Fresno-Madera, CA CSA']

codes = {
	"NAME":"CSA",
	'B01003_001E':'population',
	'B25064_001E':'median_rent',
	"B25014_008E":"total_renter_occupied",
	"B25014_012E":"1.5_2_occupants_per_room_renter",
	"B23025_001E":"total_employement_status",
	"B23025_002E":"total_in_labor_force",
	"B25001_001E":"total_number_units",
	"B25014_013E":"two_or_more_occupants_per_room_renter",
	"B25058_001E":"median_contract_rent",
	"combined statistical area":"combined statistical area"
}
    #8_21 NEW renter divided by total number of houses to get numbrer of renters


    #B07013_003E (Estimate!!Total!!Householder lived in renter-occupied housing units)/B07013_001E (total households)

#url = "https://api.census.gov/data/2017/acs/acs5?get=NAME,B01003_001E,B25064_001E,B25065_001E,B25004_002E,B23025_001E,B25001_001E,B25014_013E,B25058_001E&for=metropolitan%20statistical%20area:*"

def get_data(year):
	"""
	Load data from API
	inputs:
		url (str)
	"""
	url = "https://api.census.gov/data/"+year+"/acs/acs5?get=NAME,B01003_001E,B25064_001E,B25014_008E,B25014_012E,B23025_001E,B23025_002E,B25001_001E,B25014_013E,B25058_001E&for=combined%20statistical%20area:*"
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

def merge_data(pit_data_csv,year):
	pit_counts = pd.read_csv(pit_data_csv)

	url = "https://api.census.gov/data/"+year+"/acs/acs5?get=NAME,B01003_001E,B25064_001E,B25014_008E,B25014_012E,B23025_001E,B23025_002E,B25001_001E,B25014_013E,B25058_001E&for=combined%20statistical%20area:*"

	acs = pull_acs_data(url,year)
	pit_counts = pit_counts.replace({'Sacramento-Arden Arcade-Yuba City, CA-NV CSA': 'Sacramento-Roseville, CA CSA', 'NY-Newark, NY-NJ-CT-PA CSA': 'New York-Newark, NY-NJ-CT-PA CSA'})


	#acs.loc[pit_counts['CSA'] == 'Sacramento-Arden Arcade-Yuba City, CA-NV CSA'] = 'Sacramento-Roseville, CA CSA'
	#acs.loc[pit_counts['CSA'] == 'NY-Newark, NY-NJ-CT-PA CSA'] = 'New York-Newark, NY-NJ-CT-PA CSA'

	merged = pit_counts.merge(acs, on='CSA')

	merged["two_or_more_occupants_per_room_renter"] = merged["two_or_more_occupants_per_room_renter"].astype(int)
	merged["total_number_units"] = merged["total_number_units"].astype(int)
	merged["total_renter_occupied"] = merged["total_renter_occupied"].astype(int)
	merged["total_number_units"] = merged["total_number_units"].astype(int)
	merged["1.5_2_occupants_per_room_renter"] = merged["1.5_2_occupants_per_room_renter"].astype(int)
	merged["population"] = merged["population"].astype(int)
	merged["total_in_labor_force"] = merged["total_in_labor_force"].astype(int)

	merged["overcrowded"] = merged["two_or_more_occupants_per_room_renter"] + merged["1.5_2_occupants_per_room_renter"] / merged["total_renter_occupied"]
	merged["Percent_of_Market_for_Rent"] = merged["total_renter_occupied"] / merged["total_number_units"]
	merged["Workforce_Participation_Rate"] = merged["total_in_labor_force"] / merged["population"]

	merged.to_csv("ACS_agumented_CSA_data.csv")
	#merged = merged.drop(columns=['Unnamed: 0'])
	return merged 






def go():

	df = merge_data(df,year)


if __name__ == "__main__":
	go()

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

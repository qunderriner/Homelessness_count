import requests 
import pandas as pd 
import re 

pit_data_csv = "CSA_Zillow_Pit_Data_Merged.csv" #file with correct mapping of pit counts to CSAs
year = "2017" #year you want ACS data for 

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


#url = "https://api.census.gov/data/2017/acs/acs5?get=NAME,B01003_001E,B25064_001E,B25065_001E,B25004_002E,B23025_001E,B25001_001E,B25014_013E,B25058_001E&for=metropolitan%20statistical%20area:*"

def get_data(year):
	"""
	Load data from API. modify the url to change the items being requested. Also if adding new items to call, add them to the "codes" dictionary above
	so they they get proper column labels. 
	inputs:
		url (str)
	"""
	url = "https://api.census.gov/data/"+year+"/acs/acs5?get=NAME,B01003_001E,B25064_001E,B25014_008E,B25014_012E,B23025_001E,B23025_002E,B25001_001E,B25014_013E,B25058_001E&for=combined%20statistical%20area:*"
	response = requests.get(url)
	data_1 = pd.DataFrame(response.json())

	return data_1 

def make_header(df):
	"""
	do some basic cleanup of the header row 
	"""
	new_header = df.iloc[0] #grab the first row for the header
	df = df[1:] #take the data less the header row
	df.columns = new_header
	df.columns = [codes[x] for x in df.columns]
	df = df.drop(columns=['combined statistical area'])	
	return df 

def pull_acs_data(url,year):
	"""
	add as string which one year ACS estimate you want. 
	inputs:
	url: (str) API call for ACS
	year: (str) what year of ACS data you want 
	"""
	df = get_data(year)
	df = make_header(df)
	df = df[df['CSA'].isin(csa_filter)]
	return df 

def merge_data(pit_data_csv,year):
	"""
	this pulls in the ACS data from the API and merges it with the csa/pit count data in the filepath specified as pit_data_csv at the top of the page
	Further, it creates three new columns:
	Overcrowded- number of rental units with more than 1.5 occupants per room divided by the total number of renter occupied units 
	Percent_of_Market_for_Rent - total number of renter occupied units, over total number of units. 
	Workforce_Participation_Rate - total number of people in teh labor force, divided by the population 


	Inputs:
	pit_data_csv: (str) filepath to CSA-PIT count mapped data
	year: (str) year to call ACS API from 

	"""

	pit_counts = pd.read_csv(pit_data_csv)

	url = "https://api.census.gov/data/"+year+"/acs/acs5?get=NAME,B01003_001E,B25064_001E,B25014_008E,B25014_012E,B23025_001E,B23025_002E,B25001_001E,B25014_013E,B25058_001E&for=combined%20statistical%20area:*"

	acs = pull_acs_data(url,year)
	pit_counts = pit_counts.replace({'Sacramento-Arden Arcade-Yuba City, CA-NV CSA': 'Sacramento-Roseville, CA CSA', 'NY-Newark, NY-NJ-CT-PA CSA': 'New York-Newark, NY-NJ-CT-PA CSA'})
	#the above is done because of some slight naming differences between Sacremento CSAs... worth delving into more deeply if its a meaningful difference at a later date
	#currently assuming they are similar enough for evaluation purposes. In the NY case, the difference is just if NYC is spelled our or not. 
	merged = pit_counts.merge(acs, on='CSA')

	#need to make every column you want to manipulate from the ACS api into an int, ideally would do this cleaner with just a quick function 
	merged["two_or_more_occupants_per_room_renter"] = merged["two_or_more_occupants_per_room_renter"].astype(int)
	merged["total_number_units"] = merged["total_number_units"].astype(int)
	merged["total_renter_occupied"] = merged["total_renter_occupied"].astype(int)
	merged["total_number_units"] = merged["total_number_units"].astype(int)
	merged["1.5_2_occupants_per_room_renter"] = merged["1.5_2_occupants_per_room_renter"].astype(int)
	merged["population"] = merged["population"].astype(int)
	merged["total_in_labor_force"] = merged["total_in_labor_force"].astype(int)

	#creation of new collumns from ACS data 
	merged["overcrowded"] = merged["two_or_more_occupants_per_room_renter"] + merged["1.5_2_occupants_per_room_renter"] / merged["total_renter_occupied"]
	merged["Percent_of_Market_for_Rent"] = merged["total_renter_occupied"] / merged["total_number_units"]
	merged["Workforce_Participation_Rate"] = merged["total_in_labor_force"] / merged["population"]

	merged.to_csv("ACS_agumented_CSA_data.csv")

	return merged 






def go():

	merge_data(df,year)


if __name__ == "__main__":
	go()



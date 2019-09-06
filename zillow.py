import pandas as pd 

zillow_data = "Metro_Zhvi_AllHomes.csv" #the zillow data file to process 
city_csa_mapping = "Top Metros __ CoCs 2017 - CSA-MSA_augmented.csv" #mapping of CSA to MSA in the data folder of the github 
population = "cbsa-est2018-alldata.csv" #this is:
#"Metropolitan and Micropolitan Statistical Area Totals Dataset: Population and Estimated Components of Change: April 1, 2010 to July 1, 2018"	
#from https://www.census.gov/data/datasets/time-series/demo/popest/2010s-total-metro-and-micro-statistical-areas.html#par_textimage_546156642

#this fixes some naming descrepencies 
city_map = {
	'Los Angeles, CA': 'Los Angeles-Long Beach-Anaheim, CA',
	'Hagerstown, MD': 'Hagerstown, WV',
	'Minneapolis, MN': 'Minneapolis-St Paul, MN',
	'Miami, FL':  'Miami-Fort Lauderdale, FL',
	'Dallas, TX': 'Dallas-Fort Worth, TX'
}

def fix_city(region):
	"""
	cleans up city names to be usable 
	"""
	if '-' in region.split(',')[0]:
		city = region.split('-')[0]
		state = region.split(',')[1].split('-')[0]
		region = city + ',' + state
	elif '-' in region.split(',')[1]:
		city = region.split(',')[0]
		state = region.split(',')[1].split('-')[0]
		region = city + ',' + state
	if region in city_map:
		region = city_map[region]
	return region


def process_data(zillow_data, year,data_type,quarterly=False):
	"""
	will take zillow research data https://www.zillow.com/research/data/ and return data summarized by CSA for a given year.
	function takes the average for each month in a given year 
	zillow_data - filepath to zillow data download
	year - year you want data to sumarize for 
	data_type - what is this data about? this generates a column name 
	if the data, like those in the "More Metrics" section of zillow, is reportedly quarterly, then put quartly = True in the call, otherwise can ignore
	
	returns a mapping of the given metric to the CSA 
	"""


	zillow_home_values = pd.read_csv(zillow_data,encoding = "ISO-8859-1")
	
	if quarterly == False:
		begin_date = year+"-01"
		end_date = year+"-12"
	else:
		begin_date = year+"-03"
		end_date = year+"-12"

	if data_type == "rent_to_income_ratio":
		zillow_home_values = zillow_home_values[zillow_home_values["Index"].isin(["Rent Affordability"])]

	col = zillow_home_values.loc[: , begin_date:end_date]

	mean_data_type = data_type + " " + year 

	zillow_home_values[mean_data_type] = col.mean(axis=1)

	zillow_home_values = zillow_home_values[["RegionName",mean_data_type]]
	zillow_home_values = zillow_home_values.round({mean_data_type: 2})

	mapping = pd.read_csv(city_csa_mapping)

	mapping['RegionName'] = mapping['RegionName'].str.strip()

	zillow_home_values_augmented = zillow_home_values.merge(mapping, on="RegionName")

	zillow_home_values_augmented['RegionName'] = zillow_home_values_augmented['RegionName'].str.strip()


	weights = pd.read_csv(population,encoding = "ISO-8859-1")
	weights = weights[weights.LSAD=='Metropolitan Statistical Area']
	weights = weights.rename(columns={"NAME":"RegionName"})
	weights = weights[["RegionName","CENSUS2010POP"]]
	weights['RegionName'] = weights.RegionName.apply(lambda x: fix_city(x))
	weights["RegionName"] = weights["RegionName"].str.strip()
	
	zillow_home_values_augmented = zillow_home_values_augmented.dropna(subset=[mean_data_type])

	zillow_home_values_augmented = zillow_home_values_augmented.merge(weights,on="RegionName")

	zillow_home_values_augmented["big_weighted"] = zillow_home_values_augmented[mean_data_type] * zillow_home_values_augmented["CENSUS2010POP"]

	zillow_home_values_augmented = zillow_home_values_augmented.dropna()

	zillow_home_values_augmented.groupby("CSA").big_weighted.sum() / zillow_home_values_augmented.groupby("CSA").CENSUS2010POP.sum()

	zillow_home_values_augmented = (zillow_home_values_augmented.groupby("CSA").big_weighted.sum() / zillow_home_values_augmented.groupby("CSA").CENSUS2010POP.sum()).reset_index()

	zillow_home_values_augmented = zillow_home_values_augmented.rename(columns={0:mean_data_type})

	zillow_home_values_augmented = zillow_home_values_augmented.round({mean_data_type: 3})

	zillow_home_values_augmented = zillow_home_values_augmented[1:]
	
	
	return zillow_home_values_augmented



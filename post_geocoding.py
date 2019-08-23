import pandas as pd 

#Note: because of steps that arent coded, eg ArcGIS, need to ensure hardcoded filenames below are correct

zip_code = "augmented_zip_only.csv"#this is the zip code output from read_and_aggreage_final

zip_to_csa_mapping = "zip_code_csa_mapping_only_clean.csv"# this is the output from ArcGIS of running an intersection 
								#between zip codes and CSAs, which each row being a mapping of a zip code to a CSA

good_addresses = "GOOD_ADDRESSES_WITH_CSA_MAPPED.csv"

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

def add_zero(x):

	if len(x['zip']) == 4:
		return "0" + x['zip']
	elif len(x['zip']) == 3:
		return "00" + x['zip']
	elif len(x['zip']) == 2:
		return "000" + x['zip']
	else:
		return x['zip']

def fix_leading_zeros(df):    
	df["zip"] = df["zip"].astype(int)
	df["zip"] = df["zip"].astype(str)
	df["zip"] = df.apply(lambda x: add_zero(x), axis=1)
	return df

def map_zip_only_to_csa(zip_code, zip_to_csa_mapping):
	zip_to_csa_mapping = zip_to_csa_mapping.rename(columns={"ZIP_CODE":"zip"})
	zip_code = fix_leading_zeros(zip_code)
	zip_to_csa_mapping = fix_leading_zeros(zip_to_csa_mapping)
	zip_code_final = zip_code.merge(zip_to_csa_mapping, on="zip")
	zip_code_final = zip_code_final[["NAMELSAD","Pit Count"]]
	return zip_code_final 


def make_find_counts(good_addresses):
	zips = map_zip_only_to_csa(zip_code, zip_to_csa_mapping)
	if 'Sum PIT Count' in df.columns:
		good_addresses = good_addresses.rename(columns={"Sum PIT Count":"PIT Count"})
	good_addresses = good_addresses[["NAMELSAD","Pit Count"]]
	zips = zips[["NAMELSAD","PIT Count"]]
	good_addresses = good_addresses[["NAMELSAD","PIT Count"]]
	full_dataset = pd.concat([good_addresses, zips])
	full_dataset = full_dataset[full_dataset['NAMELSAD'].isin(csa_filter)]
	full_dataset_grouped=full_dataset.groupby('NAMELSAD').sum().reset_index()
	full_dataset_grouped = full_dataset_grouped.rename(columns={"NAMELSAD":"CSA"})
	full_dataset_grouped.to_csv("final_HICPIT_CSA_Mapping.csv")

def go():

	make_find_counts(good_addresses)


if __name__ == "__main__":
	go()

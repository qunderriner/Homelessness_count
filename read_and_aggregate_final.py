import pandas as pd 
import re

#Note: because of steps that arent coded, eg ArcGIS, need to ensure hardcoded filenames below are correct

#zip_to_csa_mapping = "zip_code_csa_mapping_only_clean"

#zip_mapped = pd.read_csv("zip_code_csa_mapping_only_clean")

missing = pd.read_csv("full_missing_list_augmented - full_missing_list_augmented.csv")#output from zipcode_less after its been
																	#manually fixed
good_addresses = "good_addresses.csv" #output of good addresses from split_data.py 
zip_code_only = "zip_code_only.csv" #output of zipcode only from split_data.py

cols_to_keep = ["CoC", "HudNum", "address1", "city", "zip", "PIT Count", "Project Type",'Organization ID','Project ID']


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


def good_addresses_(df):
	df = df[cols_to_keep]
	values = {'address1': "No Data"}
	df = df.fillna(value=values)
	df = df[~df.address1.str.contains("PO BOX",flags=re.IGNORECASE, na=False)]
	df = df[~df.address1.str.contains("P.O. BOX",flags=re.IGNORECASE, na=False)]
	df = df.dropna(subset=['zip',"address1"])
	good_address_filter = df.address1.str.contains("\d", regex=True,na=False)
	df = df[good_address_filter]
	df = fix_leading_zeros(df)
	df.to_csv("augmented_good_addresses.csv")
	return df

def zipcode_only_(df, dont_double_count):
	"""
	creates a csv of only the zipcode 
	"""
	df = df[cols_to_keep]
	po = df[df.address1.str.contains("PO BOX",flags=re.IGNORECASE, na=False)]
	popo = df[df.address1.str.contains("P.O. BOX",flags=re.IGNORECASE, na=False)]
	df = df[~df.address1.isin(dont_double_count)]
	values = {'address1': "No Data"}
	df = df.fillna(value=values)
	best_filter = df.address1.str.contains('\d', regex=True,na=False)
	df = df[~best_filter]
	df = pd.concat([df, po, popo])
	df = df.dropna(subset=['zip'])
	df = fix_leading_zeros(df)
	df.to_csv("augmented_zip_only.csv")
	return df 

def split_augmented_data(missing, good_addresses, zip_code_only):
	"""
	After taking the output from zipcode_less, which addresses need to be manually 
	checked, take the csv that results from this and use this function to break it into
	good addresses and the addresses for which you were only able to find zipcodes for. it then
	takes the good addresses files and the zip files and concatenates them with their respective 
	elements from the manually checked files

	inputs:
		missing: output from zipcode_less
		good_addresses: output of good addresses from split_data.py 
		zip_code_only: output of zipcode only from split_data.py
	outputs:
		final_good: good addresses ready to uploaded and geocoded
		final_zip: zip code only addresses ready to be uploaded and geocoded
	"""

	missing = missing[cols_to_keep]

	df_good_addresses_from_augmented = good_addresses_(missing)
	

	good_addy = pd.read_csv(good_addresses)

	final_good = pd.concat([good_addy, df_good_addresses_from_augmented])

	final_good.to_csv("big_final_merged_good_addresses_for_upload.csv")
	dont_double_count = final_good.address1
	
	good_zips = pd.read_csv(zip_code_only)
	df_zip_only_from_augmented = zipcode_only_(missing, dont_double_count)
	
	
	final_zip = pd.concat([good_zips, df_zip_only_from_augmented])
	#final_zip = final_zip.
	final_zip.to_csv("big_final_merged_zip_only.csv")


def go():

	split_augmented_data(missing, good_addresses, zip_code_only)


if __name__ == "__main__":
	go()







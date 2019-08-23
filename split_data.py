import pandas as pd 
import re 

pit_data_csv = "2015-Housing-Inventory-Count-Raw-File.xlsx" #PIT data comes from here: https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/ no api sadly 
#Note: Only the odd numbered years are used in this anaysis as even numbered years are only estimates, not actual counts.

pro_type = ["PSH","RRH","OPH"]

CoC_full = ['AZ-500',
 'AZ-502',
 'CA-500',
 'CA-501',
 'CA-502',
 'CA-503',
 'CA-504',
 'CA-505',
 'CA-506',
 'CA-507',
 'CA-508',
 'CA-511',
 'CA-512',
 'CA-514',
 'CA-515',
 'CA-515',
 'CA-517',
 'CA-518',
 'CA-521',
 'CA-524',
 'CA-524',
 'CA-525',
 'CA-600',
 'CA-601',
 'CA-602',
 'CA-606',
 'CA-607',
 'CA-608',
 'CA-609',
 'CA-611',
 'CA-612',
 'CO-500',
 'CO-500',
 'CO-500',
 'CO-500',
 'CO-500',
 'CO-503',
 'CO-503',
 'CO-503',
 'CO-503',
 'CO-503',
 'CO-503',
 'CO-503',
 'CT-503',
 'CT-505',
 'CT-505',
 'CT-505',
 'CT-505',
 'DC-500',
 'DE-500',
 'DE-500',
 'FL-504',
 'FL-507',
 'FL-509',
 'FL-517',
 'FL-520',
 'FL-600',
 'FL-601',
 'FL-605',
 'GA-500',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-501',
 'GA-502',
 'GA-503',
 'GA-506',
 'GA-508',
 'HI-501',
 'IL-500',
 'IL-502',
 'IL-506',
 'IL-509',
 'IL-510',
 'IL-511',
 'IL-512',
 'IL-514',
 'IL-517',
 'IL-518',
 'IL-518',
 'IL-518',
 'IN-502',
 'IN-502',
 'IN-502',
 'IN-502',
 'IN-502',
 'MA-500',
 'MA-502',
 'MA-503',
 'MA-505',
 'MA-506',
 'MA-508',
 'MA-509',
 'MA-510',
 'MA-511',
 'MA-515',
 'MA-516',
 'MA-517',
 'MA-519',
 'MD-501',
 'MD-502',
 'MD-503',
 'MD-504',
 'MD-505',
 'MD-506',
 'MD-507',
 'MD-508',
 'MD-509',
 'MD-511',
 'MD-511',
 'MD-512',
 'MD-600',
 'MD-601',
 'MI-500',
 'MI-500',
 'MI-501',
 'MI-502',
 'MI-503',
 'MI-504',
 'MI-505',
 'MI-509',
 'MI-511',
 'MI-515',
 'MI-518',
 'MN-500',
 'MN-501',
 'MN-502',
 'MN-502',
 'MN-502',
 'MN-502',
 'MN-503',
 'MN-503',
 'MN-503',
 'MN-503',
 'MN-503',
 'MN-505',
 'MN-505',
 'MN-505',
 'MN-505',
 'MN-505',
 'MN-505',
 'MN-505',
 'MN-511',
 'NH-500',
 'NH-500',
 'NH-500',
 'NH-500',
 'NH-501',
 'NH-502',
 'NJ-500',
 'NJ-501',
 'NJ-502',
 'NJ-503',
 'NJ-503',
 'NJ-503',
 'NJ-503',
 'NJ-504',
 'NJ-506',
 'NJ-507',
 'NJ-508',
 'NJ-509',
 'NJ-510',
 'NJ-511',
 'NJ-512',
 'NJ-513',
 'NJ-514',
 'NJ-515',
 'NJ-516',
 'NJ-516',
 'NJ-516',
 'NY-600',
 'NY-600',
 'NY-600',
 'NY-600',
 'NY-600',
 'NY-601',
 'NY-602',
 'NY-603',
 'NY-603',
 'NY-604',
 'NY-606',
 'NY-608',
 'OH-502',
 'OH-506',
 'OH-507',
 'OH-507',
 'OH-507',
 'OH-507',
 'OH-507',
 'OH-507',
 'OH-507',
 'OH-507',
 'OH-507',
 'OH-507',
 'OH-507',
 'OH-508',
 'OK-507',
 'OR-501',
 'OR-505',
 'OR-505',
 'OR-505',
 'OR-505',
 'OR-505',
 'OR-505',
 'OR-506',
 'OR-507',
 'PA-500',
 'PA-502',
 'PA-504',
 'PA-505',
 'PA-506',
 'PA-509',
 'PA-509',
 'PA-509',
 'PA-509',
 'PA-509',
 'PA-509',
 'PA-511',
 'RI-500',
 'RI-500',
 'RI-500',
 'RI-500',
 'RI-500',
 'TX-600',
 'TX-601',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-607',
 'TX-624',
 'TX-624',
 'TX-700',
 'TX-700',
 'TX-700',
 'VA-513',
 'VA-513',
 'VA-513',
 'VA-514',
 'VA-521',
 'VA-600',
 'VA-601',
 'VA-602',
 'VA-603',
 'VA-604',
 'WA-500',
 'WA-501',
 'WA-501',
 'WA-501',
 'WA-501',
 'WA-501',
 'WA-501',
 'WA-501',
 'WA-501',
 'WA-503',
 'WA-504',
 'WA-508',
 'WI-500',
 'WI-500',
 'WI-500',
 'WV-508',
 'WV-508',
 'WV-508',
 'WV-508']


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


cols_to_keep_2017 = ["CoC", "HudNum", "address1", "city", "zip", "PIT Count", "Project Type","Project Name","Organization Name"]


def read_pit_data(pit_data_csv,flag=True):
	"""
	read in hud data, keep columns that we want 
	inputs:
	pit_data_csv (str): path/filename for hud data https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/
	"""
	df = pd.read_excel(pit_data_csv)
	#if df.year.iloc[4] in (2015,2013):
	if df.year.iloc[4] in (2013,2014,2015,2016):
		df = df.rename(columns={"Address1":"address1","Zip":"zip","City":"city","Program Type":"Project Type"})
	df = filtered(df)
	if flag == False:
		return df
	else:
		df = df[cols_to_keep_2017]
	return df 

def add_zero(x):
	"""
	add back leading zeros dropped from zip codes 
	"""  

	if len(x['zip']) == 4:
		return "0" + x['zip']
	elif len(x['zip']) == 3:
		return "00" + x['zip']
	elif len(x['zip']) == 2:
		return "000" + x['zip']
	else:
		return x['zip']

def fix_leading_zeros(df):
	"""
	add back leading zeros dropped from zip codes 
	"""      
	df["zip"] = df["zip"].astype(int)
	df["zip"] = df["zip"].astype(str)
	df["zip"] = df.apply(lambda x: add_zero(x), axis=1)
	return df

def filtered(df):
	"""
	filter hud data by hud number and project type, both of which are hardcoded at the top of the file. 
	also fixes zipcode column 
	"""

	df = df[df["HudNum"].isin(CoC_full)]#updated to just do cali sub, can change back 
	df = df[df["Project Type"].isin(pro_type)]
	df = df[df["Project Type"].isin(pro_type)]
	return df 

def zipcode_less(df):
	"""
	these are the addresses that will have to be manually fixed 
	"""
	filter_no_zip = df["zip"].isna()
	no_address = df[filter_no_zip]
	no_address.to_csv("no_zip_code_manually_fix.csv")
	return no_address

def good_addresses(df):
	#df = df[cols_to_keep]
	values = {'address1': "No Data"}
	df = df.fillna(value=values)
	df = df[~df.address1.str.contains("PO BOX",flags=re.IGNORECASE, na=False)]
	df = df[~df.address1.str.contains("P.O. BOX",flags=re.IGNORECASE, na=False)]
	df = df.dropna(subset=['zip',"address1"])
	good_address_filter = df.address1.str.contains("\d", regex=True,na=False)
	df = df[good_address_filter]
	df = fix_leading_zeros(df)
	df.to_csv("good_addresses.csv")
	return df


def zipcode_only(df, dont_double_count):
	"""
	creates a csv of only the zipcode 
	"""
	#df = df[cols_to_keep]
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
	df.to_csv("zip_code_only.csv")
	return df 

def go():

	df = read_pit_data(pit_data_csv)
	df_good = df 
	good_addresses_1 = good_addresses(df_good)
	dont_double_count = good_addresses_1.address1
	df_zip = df
	zipcode_only(df_zip, dont_double_count)
	df_manual_fix = read_pit_data(pit_data_csv,flag=False)

	zipcode_less(df_manual_fix)

if __name__ == "__main__":
	go()


import pandas as pd 

import acs_v2 as acs 
import zillow 

#NOTE: occasionally calls to the ACS API just fail, run this a few times if that happens. 




def go():
	"""
	Main things to change below would year of zillow data (in the zillow.process_data call) or the filepaths, as designed below

	Can call this function once post_geocoding is complete to add ACS, Zillow, and other PIT Count data  
	"""


	HIC_PIT_CSA = "2017_PIT_CSA_v2.csv" #final mapping of hicpit counts to CSA, output of post_geocoding 
	other_PIT = pd.read_csv("2017_CSA_ALL_PIT_COUNTS.csv")#mapping of sheltered/unsheltered HIC/PIT count to CSA
	ACS_data = acs.merge_data(HIC_PIT_CSA,"2017")#change 2nd input for the year you want 


	zillow_rtoi = zillow.process_data("zillow_affordability_three_categories.csv", "2017","rent_to_income_ratio",quarterly=True)
	zillow_housing = zillow.process_data("zillow_data_housing_cost.csv", "2017","housing_cost",quarterly=False)
	zillow_rental = zillow.process_data("zillow_rental_cost.csv", "2017","rental_cost",quarterly=False)
	zillow_income = zillow.process_data("zillow_median_household_income.csv", "2017","median_household_income",quarterly=True)

	merged = ACS_data.merge(zillow_rtoi,on="CSA")
	merged = merged.merge(zillow_housing,on="CSA")
	merged = merged.merge(zillow_rental,on="CSA")
	merged = merged.merge(zillow_income,on="CSA")

	merged = merged.merge(other_PIT,on="CSA")



	try:
		merged = merged[merged.columns.drop(list(merged.filter(regex="Unnamed")))]
	except:
		print("Drop bad column names failed, can do manually")

	try:
		merged = merged.rename(columns={"PIT Count_y":"HIC_PIT"})
	except:
		print("renaming PIT Count_y to HIC_PIT failed, can do manually if needed")



	merged.to_csv("FINAL_SEPT.csv")




if __name__ == "__main__":
	go()
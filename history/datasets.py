import pandas as p
import numpy as np

CSV_PATH = "static/data/Historical_analysis.csv"
FULL_PATH = "./main/" + CSV_PATH
LANDCOVER = [
		{"value": "forest","name": "Forest"}
		,{"value": "hti","name": "HTI"}
		,{"value": "coffee","name": "Coffee"}
		,{"value": "rubber","name": "Rubber"}
		,{"value": "oilpalm","name": "Oil Palm"}
		,{"value": "rice","name": "Rice"}
	]

SUB_LANDCOVER = {
	"forest": [	"Undisturbed forest"
				,"Logged over forest-high density"
				,"Logged over forest-low density"
				,"Undisturbed swamp forest"
				,"Logged over swamp forest"
				,"Undisturbed mangrove"
				,"Logged over mangrove"
			],
	"hti": ["Acacia"],
	"coffee": ["Coffee agroforest"],
	"rubber": ["Rubber agroforest","Rubber monoculture"],
	"oilpalm": ["Oil palm"],
	"rice": ["Irrigated rice","Paddy field"]
}

LANDCOVER_GROUP = {
	"LC_T2": [	"Undisturbed forest","Logged over forest-high density","Logged over forest-low density"
				,"Undisturbed swamp forest","Logged over swamp forest"
				,"Undisturbed mangrove","Logged over mangrove"
				,"Acacia"
				,"Coffee agroforest"
				,"Rubber agroforest"
				,"Rubber monoculture"
				,"Oil palm"
				,"Irrigated rice"
				,"Paddy field"
			],
	"LC_T2_GROUP": [ "Dryland forest","Dryland forest","Dryland forest"
				,"Swamp forest","Swamp forest"
				,"Mangrove","Mangrove"
				,"Acacia"
				,"Coffee agroforest"
				,"Rubber agroforest"
				,"Rubber monoculture"
				,"Oil palm"
				,"Irrigated rice"
				,"Paddy field"
	]
}

PLAN_TOP = 5
NEW_INDE = "Other use"

AREA_PERIOD_BEGIN = 0
AREA_GROWTH = 0.00

def LoadRawData():
	global RAW_DATA
	RAW_DATA = p.read_csv(FULL_PATH)
	RAW_DATA["LC_T1"]=RAW_DATA["LC_T1"].str.strip()
	RAW_DATA["LC_T2"]=RAW_DATA["LC_T2"].str.strip()

	global LANDCOVER_GROUP_DATA
	LANDCOVER_GROUP_DATA = p.DataFrame(data=LANDCOVER_GROUP["LC_T2_GROUP"],index=LANDCOVER_GROUP["LC_T2"],columns=["LC_T2_GROUP"])
	LANDCOVER_GROUP_DATA.index.name = "LC_T2"
	
def LoadKabupaten():
	global KAB_LIST
	KAB_LIST = RAW_DATA.ADMIN.unique()
	KAB_LIST.sort()

def LoadPeriod():
	global PERIOD_LIST
	PERIOD_LIST = RAW_DATA.PERIOD.unique()
	PERIOD_LIST.sort()

def CalculateArea(selected_landcover,selected_period):
	global AREA_PERIOD_BEGIN
	global AREA_PERIOD_END
	global AREA_GROWTH
	global AREA_PERIOD_BEGIN_ADMIN
	global AREA_PERIOD_END_ADMIN
	global AREA_ADMIN_TOTAL
	global AREA_ADMIN_LARGEST
	#global AREA_ADMIN_FASTEST
	global AREA_PEAT
	global AREA_LANDCOVER
	global AREA_LANDCOVER_PLAN
	global AREA_PERIOD
	global AREA_CHANGES_PLAN
	# print("Calculate Area")

	if selected_landcover != "" and selected_period != "":
		dfper = RAW_DATA[RAW_DATA["PERIOD"].isin([selected_period])]

		dfp_t1 = dfper[dfper["LC_T1"].isin(SUB_LANDCOVER[selected_landcover])]
		dfp_t2 = dfper[dfper["LC_T2"].isin(SUB_LANDCOVER[selected_landcover])]

		### get total area for each period (MAP DESCRIPTION)
		AREA_PERIOD_BEGIN = dfp_t1["COUNT"].sum()
		AREA_PERIOD_END = dfp_t2["COUNT"].sum()

		### calculate the growth per year (MAP DESCRIPTION)
		AREA_GROWTH = (AREA_PERIOD_END - AREA_PERIOD_BEGIN) / (AREA_PERIOD_BEGIN * 1.00) * 100

		
		### Get total area group by Kabupaten for each period. Will be used in the map (MAP DATA)
		AREA_PERIOD_BEGIN_ADMIN = p.pivot_table(dfp_t1,index=["ADMIN"],values=["COUNT"],aggfunc=np.sum)
		AREA_PERIOD_END_ADMIN = p.pivot_table(dfp_t2,index=["ADMIN"],values=["COUNT"],aggfunc=np.sum)

		
		### Get total Kabupaten which has forest (Total Area > 0) (MAP DESCRIPTION)
		dfp_t2_kab_non_zero = AREA_PERIOD_END_ADMIN.query("COUNT > 0")
		AREA_ADMIN_TOTAL = len(dfp_t2_kab_non_zero)

		
		### Get Kabupaten Name which has the largest forest area (MAP DESCRIPTION)
		dfp_t2_kab_max_value = AREA_PERIOD_END_ADMIN["COUNT"].max()
		dfp_t2_kab_max_row = AREA_PERIOD_END_ADMIN[AREA_PERIOD_END_ADMIN["COUNT"].isin([dfp_t2_kab_max_value])].head()
		AREA_ADMIN_LARGEST = dfp_t2_kab_max_row.axes[0][0]

		
		### Get Kabupaten name which has the fastest growth (???)

		
		### Get total area group by Peat type (CHART 1)
		AREA_PEAT = p.pivot_table(dfp_t2,index=["PEAT"],values=["COUNT"],aggfunc=np.sum)

		
		### Get total area group by Landcover Group
		# Group data by Landcover type
		AREA_LANDCOVER = p.pivot_table(dfp_t2,index=["LC_T2"],values=["COUNT"],aggfunc=np.sum)
		# merge the data with Landcover group DataFrame to get the Landcover group data
		AREA_LANDCOVER = AREA_LANDCOVER.merge(LANDCOVER_GROUP_DATA,left_index=True,right_index=True,how="left")
		# Group data again by Landcover group
		AREA_LANDCOVER = p.pivot_table(AREA_LANDCOVER,index=["LC_T2_GROUP"],values=["COUNT"],aggfunc=np.sum)

		
		### Get top 5 + other total area by Landuse plan
		# Group total area by Landuse Plan
		dfp_t2_plan = p.pivot_table(dfp_t2,index=["PLAN"],values=["COUNT"],aggfunc=np.sum)

		plan_len = len(dfp_t2_plan)
		index_name = dfp_t2_plan.index.name
		column_name = dfp_t2_plan.columns[0]

		# Get top 5 
		AREA_LANDCOVER_PLAN = dfp_t2_plan.nlargest(PLAN_TOP,"COUNT")

		# Get the rest and group as one row data
		tmp = dfp_t2_plan.nsmallest((plan_len - PLAN_TOP),"COUNT")
		new_value = tmp.sum()
		# group the rest data as new dataFrame "Other use"
		tmp = p.DataFrame(data=[new_value],index=[NEW_INDE],columns=[column_name])
		tmp.index.name = index_name;

		#merge the top 5 and the merged rest of data
		AREA_LANDCOVER_PLAN = AREA_LANDCOVER_PLAN.append(tmp).sort_index()


		### Get Landcover area changes group by all period ###
		# filter raw data base on landcover type for each period
		dfc_t1 = RAW_DATA[RAW_DATA["LC_T1"].isin(SUB_LANDCOVER[selected_landcover])]
		dfc_t2 = RAW_DATA[RAW_DATA["LC_T2"].isin(SUB_LANDCOVER[selected_landcover])]

		# Get total area for the beggining period
		AREA_PERIOD = p.pivot_table(dfc_t1,index=["PERIOD"],values=["COUNT"],aggfunc=np.sum)
		# rename the index. Get only the beggining year
		AREA_PERIOD = AREA_PERIOD.rename(lambda x: x.split("-")[0])

		# Get total area for the ending period
		dfc_t2_period = p.pivot_table(dfc_t2,index=["PERIOD"],values=["COUNT"],aggfunc=np.sum)
		# rename the index. Get only the ending period
		dfc_t2_period = dfc_t2_period.rename(lambda x: x.split("-")[1])

		# Add the last row of ending period data to the beggining period data
		AREA_PERIOD = AREA_PERIOD.append(dfc_t2_period.tail(1))


		### Get total area of choosen landcover which changes into other landcover type
		dfc_t1_t2 = dfp_t1[~dfp_t1["LC_T2"].isin(SUB_LANDCOVER[selected_landcover])]
		# exclude No Data
		dfc_t1_t2 = dfc_t1_t2[~dfc_t1_t2["LC_T2"].isin(["No data"])]
		# group the data based on Landuse plan 
		dfc_t1_t2_plan = p.pivot_table(dfc_t1_t2,index=["PLAN"],values=["COUNT"],aggfunc=np.sum)

		plan_len = len(dfc_t1_t2_plan)
		index_name = dfc_t1_t2_plan.index.name
		column_name = dfc_t1_t2_plan.columns[0]

		# Get top 5
		AREA_CHANGES_PLAN = dfc_t1_t2_plan.nlargest(PLAN_TOP,"COUNT")

		# Get the rest data
		tmp = dfc_t1_t2_plan.nsmallest((plan_len - PLAN_TOP),"COUNT")
		new_value = tmp.sum()
		# group the rest data as new dataFrame "Other use"
		tmp = p.DataFrame(data=[new_value],index=[NEW_INDE],columns=[column_name])
		tmp.index.name = index_name;

		#append the grouped rest data into top DataFrame
		AREA_CHANGES_PLAN = AREA_CHANGES_PLAN.append(tmp).sort_index()

	else:
		AREA_PERIOD_BEGIN = 0
		AREA_PERIOD_END = 0
		AREA_GROWTH = 0
		AREA_PERIOD_BEGIN_ADMIN = p.DataFrame()
		AREA_PERIOD_END_ADMIN = p.DataFrame()
		AREA_ADMIN_TOTAL = 0
		AREA_ADMIN_LARGEST = ""
		#AREA_ADMIN_FASTEST = p.DataFrame()
		AREA_PEAT = p.DataFrame()
		AREA_LANDCOVER = p.DataFrame()
		AREA_LANDCOVER_PLAN = p.DataFrame()
		AREA_PERIOD = p.DataFrame()
		AREA_CHANGES_PLAN = p.DataFrame()

#def LoadDataLandUseChanges(selected_landcover,selected_period):

	# print("End process data")

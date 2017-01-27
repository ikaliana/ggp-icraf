import pandas as p
import numpy as np
import django.utils.translation as t
from django.conf import settings

# print(t.get_language())
CSV_PATH = "static/data/GGP_analysis_" + t.get_language() + ".csv"
# CSV_PATH = "static/data/BAU_analysis_en.csv"
FULL_PATH = settings.BASE_DIR + "/main/" + CSV_PATH
LANDCOVER = [
		{"value": "forest","name_en": "Forest","name_id":"Hutan"}
		,{"value": "hti","name_en": "HTI","name_id":"HTI"}
		,{"value": "coffee","name_en": "Coffee","name_id":"Kopi"}
		,{"value": "rubber","name_en": "Rubber","name_id":"Karet"}
		,{"value": "oilpalm","name_en": "Oil palm","name_id":"Kelapa sawit"}
		,{"value": "rice","name_en": "Rice","name_id":"Padi"}
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
	"hti": ["Acacia","Industrial timber"],
	"coffee": ["Coffee agroforest"],
	"rubber": ["Rubber agroforest","Rubber monoculture"],
	"oilpalm": ["Oil palm"],
	"rice": ["Irrigated rice","Paddy field"]
}

LANDCOVER_GROUP = {
	"LC_T2": [	"Undisturbed forest","Logged over forest-high density","Logged over forest-low density"
				,"Undisturbed swamp forest","Logged over swamp forest"
				,"Undisturbed mangrove","Logged over mangrove"
				,"Acacia","Industrial timber"
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
				#,"Acacia"
				,"Industrial timber","Industrial timber"
				,"Coffee agroforest"
				,"Rubber agroforest"
				,"Rubber monoculture"
				,"Oil palm"
				,"Irrigated rice"
				,"Paddy field"
	]
}

PLAN_TOP = 5
NEW_INDEX = "Other use"

AREA_PERIOD_BEGIN = 0
AREA_GROWTH = 0.00

PIVOT_PERIOD = {
	"": 0
	,"2014-2018" : 4
	,"2018-2022" : 4
	,"2022-2026" : 4
	,"2026-2030" : 4
}

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
	global AREA_ADMIN_FASTEST
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
		if AREA_PERIOD_BEGIN != 0:
			AREA_GROWTH = (AREA_PERIOD_END - AREA_PERIOD_BEGIN) / (AREA_PERIOD_BEGIN * 1.00) * 100
		else:
			AREA_GROWTH = 0
		
		### Get total area group by Kabupaten for each period. Will be used in the map (MAP DATA)
		AREA_PERIOD_BEGIN_ADMIN = p.pivot_table(dfp_t1,index=["ADMIN"],values=["COUNT"],aggfunc=np.sum)
		AREA_PERIOD_END_ADMIN = p.pivot_table(dfp_t2,index=["ADMIN"],values=["COUNT"],aggfunc=np.sum)

		
		### Get total Kabupaten which has forest (Total Area > 0) (MAP DESCRIPTION)
		dfp_t2_kab_non_zero = AREA_PERIOD_END_ADMIN.query("COUNT > 0")
		AREA_ADMIN_TOTAL = len(dfp_t2_kab_non_zero)

		
		### Get Kabupaten Name which has the largest forest area (MAP DESCRIPTION)
		#dfp_t2_kab_max_value = AREA_PERIOD_END_ADMIN["COUNT"].max()
		#dfp_t2_kab_max_row = AREA_PERIOD_END_ADMIN[AREA_PERIOD_END_ADMIN["COUNT"].isin([dfp_t2_kab_max_value])].head()
		#AREA_ADMIN_LARGEST = dfp_t2_kab_max_row.axes[0][0]
		AREA_ADMIN_LARGEST = AREA_PERIOD_END_ADMIN[AREA_PERIOD_END_ADMIN["COUNT"].isin([AREA_PERIOD_END_ADMIN["COUNT"].max()])].head().axes[0][0]
		
		### Get Kabupaten name which has the fastest growth (???)
		# dfp_kab = AREA_PERIOD_BEGIN_ADMIN.merge(AREA_PERIOD_END_ADMIN,how="inner",left_index="ADMIN",right_index="ADMIN")
		dfp_kab = AREA_PERIOD_BEGIN_ADMIN.merge(AREA_PERIOD_END_ADMIN,how="inner",left_index=True,right_index=True)
		dfp_kab["RATE"] = (dfp_kab["COUNT_y"]-dfp_kab["COUNT_x"])/dfp_kab["COUNT_x"] * 100.00
		AREA_ADMIN_FASTEST = dfp_kab[dfp_kab["RATE"].isin([dfp_kab["RATE"].max()])].head().axes[0][0]
		#AREA_ADMIN_FASTEST = dfp_kab_fast_row.axes[0][0]

		
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
		tmp = p.DataFrame(data=[new_value],index=[NEW_INDEX],columns=[column_name])
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
		tmp = p.DataFrame(data=[new_value],index=[NEW_INDEX],columns=[column_name])
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
		AREA_ADMIN_FASTEST = ""
		AREA_PEAT = p.DataFrame()
		AREA_LANDCOVER = p.DataFrame()
		AREA_LANDCOVER_PLAN = p.DataFrame()
		AREA_PERIOD = p.DataFrame()
		AREA_CHANGES_PLAN = p.DataFrame()

def CalculateData(t1_data,t2_data,count,multiplier,type):
	tmp = 0.0
	if type == "e":
		tmp = t1_data - t2_data
	elif type == "s":
		tmp = t2_data - t1_data
	else:
		tmp = (t1_data + t2_data) / 2.0

	return 0 if tmp < 0 else tmp * multiplier * count / 1000.0 #directly convert to TON

def CalculateDataEnv(selected_period,data_type):
	global PEAT_DATA_ZONE
	global PEAT_DATA_ADMIN
	global DATA_PERIOD_PEAT
	global DATA_PERIOD
	global TOTAL_DATA
	global TOTAL_RATE
	global DATA_DISTRICT
	global DATA_DISTRICT_MAX_RATE
	global DATA_DISTRICT_MAX_DATA
	global DATA_DISTRICT_MIN_DATA
	global DATA_DISTRICT_TOP
	global DATA_ZONE_TOP

	multiplier = PIVOT_PERIOD[selected_period] if data_type == "p" else 3.67
	fieldname1 = "P_T1" if data_type == "p" else "C_T1"
	fieldname2 = "P_T2" if data_type == "p" else "C_T2"
	totalyear = PIVOT_PERIOD[selected_period]

	df = RAW_DATA[~RAW_DATA["LC_T1"].isin(["No data"])]
	df = df[~df["LC_T2"].isin(["No data"])]

	df["M"] = multiplier
	df["D"] = data_type
	df["DATA"] = map(CalculateData,df[fieldname1],df[fieldname2],df["COUNT"],df["M"],df["D"])

	if selected_period != "":
		if data_type == "p":
			df = df[df["PERIOD"].isin([selected_period])]
			df = df[df["PEAT"].isin(["Gambut"])]

			PEAT_DATA_ZONE = p.pivot_table(df,index=["PLAN"],values=["DATA"],aggfunc=np.sum)
			PEAT_DATA_ADMIN = p.pivot_table(df,index=["ADMIN"],values=["DATA"],aggfunc=np.sum)
		else:
			#DATA carbon group by period and peat type
			DATA_PERIOD_PEAT = p.pivot_table(df,index=["PERIOD","PEAT"],values=["DATA","COUNT"],aggfunc=np.sum)
			
			#DATA carbon selected period, group by peat type
			DATA_PERIOD = DATA_PERIOD_PEAT.loc[selected_period]
			
			#TOTAL_DATA, TOTAL_RATE ==> Total Carbon Emission and Rate Emission
			TOTAL_DATA = DATA_PERIOD["DATA"].sum()
			TOTAL_AREA = DATA_PERIOD["COUNT"].sum()
			TOTAL_RATE = (TOTAL_DATA) / (TOTAL_AREA * multiplier)

			DATA_PERIOD_RAW = df[df["PERIOD"].isin([selected_period])]

			#DATA_DISTRICT ==> for MAP: use RATE Column
			DATA_DISTRICT = p.pivot_table(DATA_PERIOD_RAW,index=["ADMIN"],values=["DATA","COUNT"],aggfunc=np.sum)
			DATA_DISTRICT["RATE"] = DATA_DISTRICT["DATA"] / (DATA_DISTRICT["COUNT"] * multiplier)

			#DATA_DISTRICT_MAX_RATE ==> Fastest rate
			DATA_DISTRICT = DATA_DISTRICT.sort_values("RATE",ascending=False)
			DATA_DISTRICT_MAX_RATE = DATA_DISTRICT.head(1).axes[0][0]

			#Highest & Lowest district
			DATA_DISTRICT = DATA_DISTRICT.sort_values("DATA",ascending=False)
			DATA_DISTRICT_MAX_DATA = DATA_DISTRICT.head(1).axes[0][0]
			DATA_DISTRICT_MIN_DATA = DATA_DISTRICT.tail(1).axes[0][0]

			NEW_INDEX = "Others"

			#TOP 5 DISTRICT
			DATA_DISTRICT_TOP = DATA_DISTRICT.head(PLAN_TOP)
			tmp = DATA_DISTRICT.tail(len(DATA_DISTRICT)-PLAN_TOP)
			new_data = tmp["DATA"].sum()
			new_area = tmp["COUNT"].sum()
			new_rate = new_data / (new_area * multiplier)
			tmp = p.DataFrame(data=[[new_area,new_data,new_rate]],index=[NEW_INDEX],columns=["COUNT","DATA","RATE"])
			tmp.index.name = NEW_INDEX;

			DATA_DISTRICT_TOP = DATA_DISTRICT_TOP.append(tmp).sort_index()

			#TOP 5 LANDUSE PLAN carbon
			DATA_ZONE = p.pivot_table(DATA_PERIOD_RAW,index=["PLAN"],values=["DATA","COUNT"],aggfunc=np.sum)
			DATA_ZONE = DATA_ZONE.sort_values("DATA",ascending=False)

			DATA_ZONE_TOP = DATA_ZONE.head(PLAN_TOP)

			tmp = DATA_ZONE.tail(len(DATA_ZONE)-PLAN_TOP)
			new_data = tmp["DATA"].sum()
			new_area = tmp["COUNT"].sum()
			new_rate = new_data / (new_area * multiplier)
			tmp = p.DataFrame(data=[[new_area,new_data,new_rate]],index=[NEW_INDEX],columns=["COUNT","DATA","RATE"])
			tmp.index.name = NEW_INDEX;

			DATA_ZONE_TOP = DATA_ZONE_TOP.append(tmp).sort_index()

	else:
		if data_type == "p":
			PEAT_DATA_ZONE = p.DataFrame()
			PEAT_DATA_ADMIN = p.DataFrame()
		else:
			DATA_PERIOD_PEAT = p.DataFrame()
			DATA_PERIOD = p.DataFrame()
			TOTAL_DATA = 0.0
			TOTAL_RATE = 0.0
			DATA_DISTRICT = p.DataFrame()
			DATA_DISTRICT_MAX_RATE = ""
			DATA_DISTRICT_MAX_DATA = ""
			DATA_DISTRICT_MIN_DATA = ""
			DATA_DISTRICT_TOP = p.DataFrame()
			DATA_ZONE_TOP = p.DataFrame()

def CalculateProfit(selected_period):
	global PROFIT_DISTRIC_PERIOD_BEGIN
	global PROFIT_DISTICT_PERIOD_END

	if selected_period != "":
		DATA_PERIOD_RAW = RAW_DATA[RAW_DATA["PERIOD"].isin([selected_period])]

		PROFIT_DISTRIC_PERIOD_BEGIN = p.pivot_table(DATA_PERIOD_RAW,index=["ADMIN"],values=["PROF_T1"],aggfunc=np.sum)
		PROFIT_DISTICT_PERIOD_END = p.pivot_table(DATA_PERIOD_RAW,index=["ADMIN"],values=["PROF_T2"],aggfunc=np.sum)
	else:
		PROFIT_DISTRIC_PERIOD_BEGIN = p.DataFrame()
		PROFIT_DISTICT_PERIOD_END = p.DataFrame()


#def LoadDataLandUseChanges(selected_landcover,selected_period):

	# print("End process data")

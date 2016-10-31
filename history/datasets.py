import pandas as p
import numpy as np

CSV_PATH = "static/data/Historical_analysis.csv"
FULL_PATH = "./main/" + CSV_PATH
COMMODITY = [
		{"value": "forest","name": "Forest"}
		,{"value": "hti","name": "HTI"}
		,{"value": "coffee","name": "Coffee"}
		,{"value": "rubber","name": "Rubber"}
		,{"value": "oilpalm","name": "Oil Palm"}
		,{"value": "rice","name": "Rice"}
	]
SUB_COMMODITY = {
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

def LoadRawData():
	global RAW_DATA
	RAW_DATA = p.read_csv(FULL_PATH)
	RAW_DATA["LC_T1"]=RAW_DATA["LC_T1"].str.strip()
	
def LoadKabupaten():
	global KAB_LIST
	KAB_LIST = RAW_DATA.ADMIN.unique()
	KAB_LIST.sort()

def LoadPeriod():
	global PERIOD_LIST
	PERIOD_LIST = RAW_DATA.PERIOD.unique()
	PERIOD_LIST.sort()

def AreaPerCommodityAndPeriod(selected_commodity,selected_period):
	global COMMODITY_AREA_GROUP_PERIOD
	global COMMODITY_PER_PERIOD_KAB
	global COMMODITY_PER_PERIOD_PEAT

	if selected_commodity != "":
		DF1 = RAW_DATA[RAW_DATA["LC_T1"].isin(SUB_COMMODITY[selected_commodity])]
		COMMODITY_AREA_GROUP_PERIOD = p.pivot_table(DF1,index=["PERIOD"],values=["COUNT"],aggfunc=np.sum)
		DF1 = DF1[DF1["PERIOD"].isin([selected_period])]
		COMMODITY_PER_PERIOD_KAB = p.pivot_table(DF1,index=["ADMIN"],values=["COUNT"],aggfunc=np.sum)
		COMMODITY_PER_PERIOD_PEAT = p.pivot_table(DF1,index=["PEAT"],values=["COUNT"],aggfunc=np.sum)
	else:
		COMMODITY_AREA_GROUP_PERIOD = p.DataFrame()
		COMMODITY_PER_PERIOD_KAB = p.DataFrame()
		COMMODITY_PER_PERIOD_PEAT = p.DataFrame()

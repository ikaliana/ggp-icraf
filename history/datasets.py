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
	
def LoadKabupaten():
	global KAB_LIST
	KAB_LIST = RAW_DATA.ADMIN.unique()
	KAB_LIST.sort()

def LoadPeriod():
	global PERIOD_LIST
	PERIOD_LIST = RAW_DATA.PERIOD.unique()
	PERIOD_LIST.sort()

def LoadAreaPerCommodityGroupPeriod(selected_commodity):
	global COMMODITY_AREA_GROUP_PERIOD
	if selected_commodity != "":
		COMMODITY_AREA_GROUP_PERIOD = RAW_DATA[RAW_DATA["LC_T1"].isin(SUB_COMMODITY[selected_commodity])]
		COMMODITY_AREA_GROUP_PERIOD = p.pivot_table(COMMODITY_AREA_GROUP_PERIOD,index=["PERIOD"],values=["COUNT"],aggfunc=np.sum)
	else:
		COMMODITY_AREA_GROUP_PERIOD = p.DataFrame()
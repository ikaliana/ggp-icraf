import pandas as p

CSV_PATH = "data/Historical_analysis.csv"
FULL_PATH = "D:\Indra\GGP\WebApp\main\static\data\Historical_analysis.csv"

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
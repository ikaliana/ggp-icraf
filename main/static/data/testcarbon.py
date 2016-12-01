import pandas as p
import numpy as np

file = "Historical_analysis.csv"
selected_period = "2010-2014"
data_type = "e"
# datatype: emission (e), sequestration (s), peat (p)

PIVOT_PERIOD = {
	"1990-2000" :  10
	,"2000-2005" : 5
	,"2005-2010" : 5
	,"2010-2014" : 4
}

PLAN_TOP = 5
NEW_INDEX = "Other use"

multiplier = PIVOT_PERIOD[selected_period] if data_type == "p" else 3.67
fieldname1 = "P_T1" if data_type == "p" else "C_T1"
fieldname2 = "P_T2" if data_type == "p" else "C_T2"
columnlist = ["ID_LC_T1","ID_LC_T2","ID_Z","COUNT",fieldname1,fieldname2,"MULTIPLIER","DATA"]
#totalyear = PIVOT_PERIOD[selected_period]

def CalculateData(t1_data,t2_data,count,multiplier,type):
	tmp = 0.0
	if type == "e":
		tmp = t1_data - t2_data
	elif type == "s":
		tmp = t2_data - t1_data
	else:
		tmp = (t1_data + t2_data) / 2.00

	return 0 if tmp < 0 else tmp * multiplier * count / 1000 #directly convert to TON


# load all data from CSV
df = p.read_csv(file)
df["LC_T1"]=df["LC_T1"].str.strip()
df["LC_T2"]=df["LC_T2"].str.strip()
df = df[~df["LC_T1"].isin(["No data"])]
df = df[~df["LC_T2"].isin(["No data"])]

df["M"] = multiplier
df["D"] = data_type
df["DATA"] = map(CalculateData,df[fieldname1],df[fieldname2],df["COUNT"],df["M"],df["D"])

DATA_PERIOD_PEAT = p.pivot_table(df,index=["PERIOD","PEAT"],values=["DATA","COUNT"],aggfunc=np.sum)
DATA_PERIOD = DATA_PERIOD_PEAT.loc[selected_period]

converter = 1 #000.00  #convert to TON
TOTAL_DATA = DATA_PERIOD["DATA"].sum()
TOTAL_AREA = DATA_PERIOD["COUNT"].sum()
TOTAL_RATE = (TOTAL_DATA) / (TOTAL_AREA * multiplier)

DATA_PERIOD_RAW = df[df["PERIOD"].isin([selected_period])]
DATA_DISTRICT = p.pivot_table(DATA_PERIOD_RAW,index=["ADMIN"],values=["DATA","COUNT"],aggfunc=np.sum)
DATA_DISTRICT["RATE"] = DATA_DISTRICT["DATA"] / (DATA_DISTRICT["COUNT"] * multiplier)

DATA_DISTRICT = DATA_DISTRICT.sort_values("RATE",ascending=False)
DATA_DISTRICT_MAX_RATE = DATA_DISTRICT.head(1).axes[0][0]

DATA_DISTRICT = DATA_DISTRICT.sort_values("DATA",ascending=False)
DATA_DISTRICT_MAX_DATA = DATA_DISTRICT.head(1).axes[0][0]
DATA_DISTRICT_MIN_DATA = DATA_DISTRICT.tail(1).axes[0][0]

DATA_DISTRICT_TOP = DATA_DISTRICT.head(PLAN_TOP)
tmp = DATA_DISTRICT.tail(len(DATA_DISTRICT)-PLAN_TOP)
new_data = tmp["DATA"].sum()
new_area = tmp["COUNT"].sum()
new_rate = new_data / (new_area * multiplier)
tmp = p.DataFrame(data=[[new_area,new_data,new_rate]],index=[NEW_INDEX],columns=["COUNT","DATA","RATE"])
tmp.index.name = NEW_INDEX;

#append the grouped rest data into top DataFrame
DATA_DISTRICT_TOP = DATA_DISTRICT_TOP.append(tmp).sort_index()

DATA_ZONE = p.pivot_table(DATA_PERIOD_RAW,index=["PLAN"],values=["DATA","COUNT"],aggfunc=np.sum)
DATA_ZONE = DATA_ZONE.sort_values("DATA",ascending=False)

DATA_ZONE_TOP = DATA_ZONE.head(PLAN_TOP)

tmp = DATA_ZONE.tail(len(DATA_ZONE)-PLAN_TOP)
new_data = tmp["DATA"].sum()
new_area = tmp["COUNT"].sum()
new_rate = new_data / (new_area * multiplier)
tmp = p.DataFrame(data=[[new_area,new_data,new_rate]],index=[NEW_INDEX],columns=["COUNT","DATA","RATE"])
tmp.index.name = NEW_INDEX;

#append the grouped rest data into top DataFrame
DATA_ZONE_TOP = DATA_ZONE_TOP.append(tmp).sort_index()

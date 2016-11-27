import pandas as p
import numpy as np

file = "Historical_analysis.csv"
selected_period = "2010-2014"
data_type = "p"
# datatype: emission (e), sequestration (s), peat (p)

PIVOT_PERIOD = {
	"1990-2000" :  10
	,"2000-2005" : 5
	,"2005-2010" : 5
	,"2010-2014" : 4
}

multiplier = PIVOT_PERIOD[selected_period] if data_type == "p" else 3.67
fieldname1 = "P_T1" if data_type == "p" else "C_T1"
fieldname2 = "P_T2" if data_type == "p" else "C_T2"
columnlist = ["ID_LC_T1","ID_LC_T2","ID_Z","COUNT",fieldname1,fieldname2,"MULTIPLIER","DATA"]

def CalculateData(t1_data,t2_data,count,multiplier,type):
	tmp = 0.0
	if type == "e":
		tmp = t1_data - t2_data
	elif type == "s":
		tmp = t2_data - t1_data
	else:
		tmp = (t1_data + t2_data) / 2.0

	return 0 if tmp < 0 else tmp * multiplier * count / 1000 #directly convert to TON


# load all data from CSV
df = p.read_csv(file)
df["LC_T1"]=df["LC_T1"].str.strip()
df["LC_T2"]=df["LC_T2"].str.strip()
df = df[~df["LC_T1"].isin(["No data"])]
df = df[~df["LC_T2"].isin(["No data"])]
df = df[df["PERIOD"].isin([selected_period])]
df = df[df["PEAT"].isin(["Gambut"])]

df["M"] = multiplier
df["D"] = data_type
df["DATA"] = map(CalculateData,df[fieldname1],df[fieldname2],df["COUNT"],df["M"],df["D"])

PEAT_DATA_ZONE = p.pivot_table(df,index=["PLAN"],values=["DATA"],aggfunc=np.sum)
PEAT_DATA_ADMIN = p.pivot_table(df,index=["ADMIN"],values=["DATA"],aggfunc=np.sum)

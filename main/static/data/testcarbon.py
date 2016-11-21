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

multiplier = PIVOT_PERIOD[selected_period] if data_type == "p" else 3.67
fieldname1 = "P_T1" if data_type == "p" else "C_T1"
fieldname2 = "P_T2" if data_type == "p" else "C_T2"

# load all data from CSV
df = p.read_csv(file)

# filter data by specific period. Save to new dataframe
dfper = df[df["PERIOD"].isin([selected_period])]

PERIOD1_TOTAL = dfper[fieldname1].sum()
PERIOD2_TOTAL = dfper[fieldname2].sum()


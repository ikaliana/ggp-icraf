import pandas as p
import numpy as np

file = "Historical_analysis.csv"
selected_commodity = "hti"
selected_period = "1990-2000"

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

COMMODITY_GROUP = {
	"LC_T2": [	"Undisturbed forest"
				,"Logged over forest-high density"
				,"Logged over forest-low density"
				,"Undisturbed swamp forest"
				,"Logged over swamp forest"
				,"Undisturbed mangrove"
				,"Logged over mangrove"
				,"Acacia"
				,"Coffee agroforest"
				,"Rubber agroforest"
				,"Rubber monoculture"
				,"Oil palm"
				,"Irrigated rice"
				,"Paddy field"
			],
	"LC_T2_GROUP": [ "Dryland forest"
				,"Dryland forest"
				,"Dryland forest"
				,"Swamp forest"
				,"Swamp forest"
				,"Mangrove"
				,"Mangrove"
				,"Acacia"
				,"Coffee agroforest"
				,"Rubber agroforest"
				,"Rubber monoculture"
				,"Oil palm"
				,"Irrigated rice"
				,"Paddy field"
	]
}

# convert array COMMODITY_GROUP into DataFrame object. 
COMMODITY_GROUP_DATA = p.DataFrame(data=COMMODITY_GROUP["LC_T2_GROUP"],index=COMMODITY_GROUP["LC_T2"],columns=["LC_T2_GROUP"])
# set the COMMODITY_GROUP DataFrame as "LC_T2"
COMMODITY_GROUP_DATA.index.name = "LC_T2"

# load all data from CSV
df = p.read_csv(file)

# trim the whitespace
df["LC_T1"]=df["LC_T1"].str.strip()
df["LC_T2"]=df["LC_T2"].str.strip()

# filter data by specific period. Save to new dataframe
dfper = df[df["PERIOD"].isin([selected_period])]

# filter by Landcover type for period T1 and period T2
dfp_t1 = dfper[dfper["LC_T1"].isin(SUB_COMMODITY[selected_commodity])]
dfp_t2 = dfper[dfper["LC_T2"].isin(SUB_COMMODITY[selected_commodity])]

# get total area for each period
dfp_t1_sum = dfp_t1["COUNT"].sum()
dfp_t2_sum = dfp_t2["COUNT"].sum()

# calculate the growth per year
if dfp_t1_sum != 0:
	dfp_growth = (dfp_t2_sum - dfp_t1_sum) / (dfp_t1_sum * 1.00) * 100
else:
	dfp_growth = 0

# Get total area group by Kabupaten for each period. Will be used in the map
dfp_t1_kab = p.pivot_table(dfp_t1,index=["ADMIN"],values=["COUNT"],aggfunc=np.sum)
dfp_t2_kab = p.pivot_table(dfp_t2,index=["ADMIN"],values=["COUNT"],aggfunc=np.sum)
dfp_kab = dfp_t1_kab.merge(dfp_t2_kab,how="inner",left_index="ADMIN",right_index="ADMIN")
dfp_kab["RATE"] = (dfp_kab["COUNT_y"]-dfp_kab["COUNT_x"])/dfp_kab["COUNT_x"] * 100.00
#dfp_kab_fast_name = dfp_kab[dfp_kab["RATE"].isin([dfp_kab["RATE"].max()])].head().axes[0][0]
#dfp_kab_fast_name = dfp_kab_fast_row.axes[0][0]

# Get total Kabupaten which has forest (Total Area > 0)
dfp_t2_kab_non_zero = dfp_t2_kab.query("COUNT > 0")
dfp_t2_kab_count = len(dfp_t2_kab_non_zero)
dfp_t2_kab_max_value = dfp_t2_kab["COUNT"].max()
dfp_t2_kab_max_row = dfp_t2_kab[dfp_t2_kab["COUNT"].isin([dfp_t2_kab_max_value])].head()
#dfp_t2_kab_max_name = dfp_t2_kab_max_row.axes[0][0]

# Group data by PEAT type 
dfp_t2_peat = p.pivot_table(dfp_t2,index=["PEAT"],values=["COUNT"],aggfunc=np.sum)

# Group data by Landcover type
dfp_t2_group = p.pivot_table(dfp_t2,index=["LC_T2"],values=["COUNT"],aggfunc=np.sum)
# merge the data with COMMODITY_GROUP DataFrame to get the Group of Landvalue type
dfp_t2_group = dfp_t2_group.merge(COMMODITY_GROUP_DATA,left_index=True,right_index=True,how="left")
# Group data again by Group of Landcover type
dfp_t2_group = p.pivot_table(dfp_t2_group,index=["LC_T2_GROUP"],values=["COUNT"],aggfunc=np.sum)

# Group data by landuse PLAN
dfp_t2_plan = p.pivot_table(dfp_t2,index=["PLAN"],values=["COUNT"],aggfunc=np.sum)

plan_top = 5
plan_len = len(dfp_t2_plan)
index_name = dfp_t2_plan.index.name
column_name = dfp_t2_plan.columns[0]

# Get top 5 from PLAN DataFrame
dfp_t2_plan_top = dfp_t2_plan.nlargest(plan_top,"COUNT")

# Get the rest from PLAN DataFrame and group as one row data
tmp = dfp_t2_plan.nsmallest((plan_len - plan_top),"COUNT")
new_value = tmp.sum()
new_index = "Other use"
# group the rest data as new dataFrame "Other use"
tmp = p.DataFrame(data=[new_value],index=[new_index],columns=[column_name])
tmp.index.name = index_name;

#append the grouped rest data into top DataFrame
dfp_t2_plan_top = dfp_t2_plan_top.append(tmp).sort_index()


#### GET DATA LANDUSE CHANGES ####
# filter raw data base on landcover type for each period
dfc_t1 = df[df["LC_T1"].isin(SUB_COMMODITY[selected_commodity])]
dfc_t2 = df[df["LC_T2"].isin(SUB_COMMODITY[selected_commodity])]

# for t1: rename the period, get the first year
dfc_t1_period = p.pivot_table(dfc_t1,index=["PERIOD"],values=["COUNT"],aggfunc=np.sum)
dfc_t1_period = dfc_t1_period.rename(lambda x: x.split("-")[0])

# for t2: rename the period, get the second year
dfc_t2_period = p.pivot_table(dfc_t2,index=["PERIOD"],values=["COUNT"],aggfunc=np.sum)
dfc_t2_period = dfc_t2_period.rename(lambda x: x.split("-")[1])

# Merge those two period DataFrame. Get only the last row of T2
dfc_period = dfc_t1_period.append(dfc_t2_period.tail(1))

# Landuse replacing forest data
dfc_t1_t2 = dfp_t1[~dfp_t1["LC_T2"].isin(SUB_COMMODITY[selected_commodity])]
dfc_t1_t2 = dfc_t1_t2[~dfc_t1_t2["LC_T2"].isin(["No data"])]
dfc_t1_t2_plan = p.pivot_table(dfc_t1_t2,index=["PLAN"],values=["COUNT"],aggfunc=np.sum)

plan_len = len(dfc_t1_t2_plan)
index_name = dfc_t1_t2_plan.index.name
column_name = dfc_t1_t2_plan.columns[0]

dfc_t1_t2_plan_top = dfc_t1_t2_plan.nlargest(plan_top,"COUNT")

tmp = dfc_t1_t2_plan.nsmallest((plan_len - plan_top),"COUNT")
new_value = tmp.sum()
new_index = "Other use"
# group the rest data as new dataFrame "Other use"
tmp = p.DataFrame(data=[new_value],index=[new_index],columns=[column_name])
tmp.index.name = index_name;

#append the grouped rest data into top DataFrame
dfc_t1_t2_plan_top = dfc_t1_t2_plan_top.append(tmp).sort_index()
total = dfc_t1_t2_plan_top["COUNT"].sum()
dfc_t1_t2_plan_top["COUNT_MIL"] = dfc_t1_t2_plan_top["COUNT"] /  1000000.00
dfc_t1_t2_plan_top["COUNT_PERCENT"] = (dfc_t1_t2_plan_top["COUNT"] / total) * 100.00


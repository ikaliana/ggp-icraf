import pandas as p
import numpy as np

file = "Historical_analysis.csv"
selected_period = "2010-2014"

df = p.read_csv(file)
df = df[df["PERIOD"].isin([selected_period])]

PROF_ADMIN_T1 = p.pivot_table(df,index=["ADMIN"],values=["PROF_T1"],aggfunc=np.sum)
PROF_ADMIN_T2 = p.pivot_table(df,index=["ADMIN"],values=["PROF_T2"],aggfunc=np.sum)
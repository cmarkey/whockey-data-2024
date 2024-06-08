
import streamlit as st 
import pandas as pd
import numpy as np

st.set_page_config(page_title="Visualizations")

df_raw = pd.read_csv("Data/NCAA Stats 2023-2024 - Skaters.csv")
df_raw=df_raw.fillna(0)
df_raw["GF"] = df_raw["Minus"]
df_raw["GA"] = df_raw["Plus"]
df_names = df_raw.loc[df_raw["GP"] >= df_raw["GP"].max()/2].sort_values(by="Player")
df = df_raw.loc[df_raw["GP"] >= df_raw["GP"].max()/2,['Goals', 'Assists', 'Points', 'Shots', 'SHG', 'ENG','PPG','FO pct','Pen. Min.','GF', 'GA']]
median = df.median(numeric_only=True)
labels = pd.DataFrame(columns=df.columns)


label_list = ["Extremely Below Average","Below Average","Average","Above Average","Extremely Above Average"]
alt_label_list = ["Off board/Consider in free agency","Depth contributor","Average profile","Immediate impact","Game Changer"]

df_log = np.log(df[['Goals', 'Assists',
       'Points', 'Shots', 'SHG', 'ENG','PPG','Pen. Min.','GF',
       'GA']]+1)

pos_select = st.selectbox("Position", options = ["All Skaters","Forwards","Defenders","Goalies"])
player_select = st.selectbox("Player", options = df_names.Player.unique())
#forwards
df_forwards = df_log.loc[(df_names['Pos'] == 'F') | (df_names['Pos'] == 'D')]
means = df_forwards.mean(numeric_only=True)
std_devs = pd.DataFrame(columns=df.columns)

for column in df_log.columns:
    if not column in ['#', 'Player', 'Yr', 'Pos', 'Ht']:
        std_devs[column] = (df_log[column]-means[column])/df_log[column].std()
        placeholder = std_devs[column].copy(deep=True)
        
        placeholder.loc[std_devs[column] <= -2] = label_list[0]
        placeholder.loc[(std_devs[column] > -2) & (std_devs[column] <= -1)] = label_list[1]
        placeholder.loc[(std_devs[column] > -1) & (std_devs[column] < 1)] = label_list[2]
        placeholder.loc[(std_devs[column] >= 1) & (std_devs[column] < 2)] = label_list[3]
        placeholder.loc[std_devs[column] >= 2] = label_list[4]
        labels[column] = placeholder
        
column = 'FO pct'
df_fos = df_raw[df_raw['Pos'] == 'C']
std_devs[column] = (df_fos[column]-df_fos[column].mean(numeric_only=True))/df_fos[column].std()
placeholder = std_devs[column].copy(deep=True)

placeholder.loc[std_devs[column] <= -2] = label_list[0]
placeholder.loc[(std_devs[column] > -2) & (std_devs[column] <= -1)] = label_list[1]
placeholder.loc[(std_devs[column] > -1) & (std_devs[column] < 1)] = label_list[2]
placeholder.loc[(std_devs[column] >= 1) & (std_devs[column] < 2)] = label_list[3]
placeholder.loc[std_devs[column] >= 2] = label_list[4]
labels[column] = placeholder    



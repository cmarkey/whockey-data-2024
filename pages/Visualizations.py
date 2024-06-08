
import streamlit as st 
import pandas as pd

#st.set_page_config(page_title="NCAA")

df_raw = pd.read_csv("C:/Users/carle/Downloads/NCAA Stats 2023-2024 - Skaters.csv")
df_raw=df_raw.fillna(0)
df_raw["GF"] = df_raw["Minus"]
df_raw["GA"] = df_raw["Plus"]
df_names = df_raw.loc[df_raw["GP"] >= df_raw["GP"].max()/2]
df = df_raw.loc[df_raw["GP"] >= df_raw["GP"].max()/2,['Goals', 'Assists', 'Points', 'Shots', 'SHG', 'ENG','PPG','FO pct','Pen. Min.','GF', 'GA']]
median = df.median(numeric_only=True)
labels = pd.DataFrame(columns=df.columns)
print(df_names.Player.unique())
player_select = st.selectbox("Player", options = ["a","b"])

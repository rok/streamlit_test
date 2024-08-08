import pandas as pd
import pyarrow as pa
from pyarrow.parquet import read_table
import streamlit as st

st.set_page_config(layout="wide")

@st.cache_resource
def load_data():
    path = "deli_stavb_izkaznice.parquet"

    data = pd.read_parquet(path)
    return data

# st.title("Pregled stavb")
df = load_data()
col1, col2, col3 = st.columns(3)

with col1:
    ko_search = st.text_input("KO", value="")
    st_stavbe_search = st.text_input("ST_STAVBE", value="")

with col2:
    st_dela_stavbe_search = st.text_input("ST_DELA_STAVBE", value="")
    ulica_search = st.text_input("Ulica", value="")

with col3:
    obcina_search = st.text_input("Obcina", value="")
    energijski_razred_search = st.text_input("Energijski razred", value="")

column_config = {
    "url": st.column_config.LinkColumn("JV", display_text="link"),
    "url_izkaznice": st.column_config.LinkColumn("EI", display_text="EI"),
    "POPLAVNA_OGROZENOST": st.column_config.TextColumn(width="small"),
    "LETO_IZGRA": st.column_config.NumberColumn(format="%d", step="1", width="small"),
    "LETO_OBNOV": st.column_config.NumberColumn(format="%d", step="1", width="small"),
    "LETO_OBNO0": st.column_config.NumberColumn(format="%d", step="1", width="small"),
    "LETO_OBNOVE_INSTALACIJ": st.column_config.NumberColumn(format="%d", step="1", width="small"),
    "LETO_OBNOVE_OKEN": st.column_config.NumberColumn(format="%d", step="1", width="small"),
    "[p] Potrebna_toplota_za_ogrevanje":  st.column_config.NumberColumn(format="%d", step="1", width="small"),
    "[p] Dovedena_energija_za_delovanje_stavbe":  st.column_config.NumberColumn(format="%d", step="1", width="small"),
    "[p] Primarna_energija":  st.column_config.NumberColumn(format="%d", step="1", width="small"),
    "[p] Emisije_CO2":  st.column_config.NumberColumn(format="%d", step="1", width="small"),
    "[p] Energijski_razred":  st.column_config.TextColumn(width="small"),
}

columns = st.multiselect("Stolpci", options=df.columns.tolist(), default=df.columns.tolist(), label_visibility="hidden")


if ulica_search or st_stavbe_search or ko_search or st_dela_stavbe_search or obcina_search or energijski_razred_search:
    
    select = (
        ((df["ULICA_NAZIV"].str.contains(ulica_search) | df["OBCINA_NAZIV"].str.contains(ulica_search) | df["NASELJE_NAZIV"].str.contains(ulica_search)) if ulica_search else True) &
        (df["ST_DELA_STAVBE"].str.contains(st_dela_stavbe_search) if st_dela_stavbe_search else True) &
        (df["KO_ID"].str.contains(ko_search) if ko_search else True) &
        (df["ST_STAVBE"].str.contains(st_stavbe_search) if st_stavbe_search else True)  &
        (df["OBCINA_NAZIV"].str.contains(obcina_search) if obcina_search else True)  &
        (df["Energijski_razred"].str.contains(energijski_razred_search) if energijski_razred_search else True)
    )

    df_search = df[select]

    # st.write(df_search)
    st.dataframe(
        df_search[columns], 
        column_config=column_config,
        hide_index=True
        )
    st.map(df_search, size=10)

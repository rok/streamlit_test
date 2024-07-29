import pandas as pd
import pyarrow as pa
from pyarrow.parquet import read_table
import streamlit as st

@st.cache_resource
def load_data():
    path = "poplavna_ogrozenost.parquet"

    data = pd.read_parquet(path)
    return data

st.title("Poplavni ogrozenost")
st.write(
    """Ta aplikacija prikaze poplavno ogrozenost stavbe. Stavbe lahko iscemo po ulici, stevilki, katasterski obcini ali stevilki stavbe.
    """
)

df = load_data()

ulica_search = st.text_input("Ulica", value="")
stevilka_search = st.text_input("Stevilka", value="")
ko_search = st.text_input("KO", value="")
st_stavbe_search = st.text_input("ST_STAVBE", value="")
obcina_search = st.text_input("OBCINA_NAZIV", value="")

m1 = df["ULICA_NAZIV"].str.contains(ulica_search)
m2 = df["HS_STEVILKA"].str.contains(stevilka_search)
m3 = df["KO_ID"].str.contains(ko_search)
m4 = df["ST_STAVBE"].str.contains(st_stavbe_search)
m5 = df["OBCINA_NAZIV"].str.contains(obcina_search)
m6 = df["NASELJE_NAZIV"].str.contains(ulica_search)

df_search = df[(m1 | m6) & m2 & m3 & m4 & m5]

if ulica_search or stevilka_search or ko_search or st_stavbe_search or obcina_search:
    st.write(df_search)
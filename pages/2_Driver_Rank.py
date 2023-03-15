import streamlit as st
from main import read_database


st.title("Förar Placeringar")

st.caption("Placeringar över alla förare")
st.dataframe(read_database("drivers").sort_values(by=['points'], ascending=False),use_container_width=True,height=750)
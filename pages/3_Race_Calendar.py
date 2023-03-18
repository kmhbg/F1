import streamlit as st
from main import read_database

st.caption("Årets race")

st.table(read_database("races"))    
import streamlit as st
from main import create_next_race_table, insert_next_race, update_next_race_in_db


if st.button('Create Table'):
    create_next_race_table()
    insert_next_race(1,2)
    update_next_race_in_db()
else:
    pass
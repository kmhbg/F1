import streamlit as st
import streamlit_authenticator as stauthmel
import pandas as pd
from main import read_database, sum_bet_points


st.title('F1 Bet dashboard')


st.caption("Ledning i bett")
st.dataframe(sum_bet_points().sort_values(by=['points'], ascending=False))
st.caption("Alla bet under säsongen")
st.dataframe(read_database("bets").sort_values(by=['points'], ascending=False))

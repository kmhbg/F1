import streamlit as st
from main import create_next_race_table, insert_next_race, update_next_race_in_db, check_bet, next_race, get_race_results, remove_bet_from_db

next_race = next_race()
if st.button('Create Table'):
    create_next_race_table()
    insert_next_race(1,2)
    update_next_race_in_db()
else:
    pass

if st.button('Rätta bet'):
    check_bet(next_race)
    get_race_results(next_race)

else:
    pass

st.subheader("Ta bort specifikt bet ur databas")
round = st.number_input("Vilket race ska bettet bort från?", min_value=1, max_value=23)
better = st.selectbox(
    'Vems bet ska bort?',
    ('Seb', 'Jonte', 'Filip','Marcus','Oskar'))
if st.button('Ta bort bet'):
    remove = remove_bet_from_db(round,better)
    st.write(remove)
else:
    pass
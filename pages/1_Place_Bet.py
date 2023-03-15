import streamlit as st
from main import read_database,get_driver_list, get_race_list, create_bet
from PIL import Image
driver_list = get_driver_list()
race_list = get_race_list()




st.title("Placera nytt bett")
col1, col2, col3,col4,col5 = st.columns(5)

with col1:
    better = st.selectbox(
        'Vem lägger bettet',
        ('Seb', 'Jonte', 'Filip','Marcus','Oskar'))


with col2:
    first = st.selectbox(
        '1:a',
        driver_list)

with col3:
    second = st.selectbox(
        '2:a',
       driver_list)
with col4:
    third = st.selectbox(
        '3:a',
       driver_list)
with col5:
    race = st.selectbox(
        'Race',
       race_list)
#st.write('You selected:', better)
image = Image.open('./assets/qr.png')


if st.button('Placera bet'):
    bet = st.write(create_bet(race, better, first, second, third))

    st.caption("Använd qr koden för att swisha in ditt bett!")
    st.image(image)

else:
    pass
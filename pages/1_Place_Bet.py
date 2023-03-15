import streamlit as st
from main import read_database,get_driver_list, get_race_list, create_bet,next_race, get_race_name, create_next_race_table,get_next_race, insert_next_race
from PIL import Image
driver_list = get_driver_list()
race_list = get_race_list()
next_race = next_race()
next_race_name = get_race_name()
create_next_race_table()
insert_next_race(1,2)
get_next_race()


st.title("Placera nytt bett")
st.subheader(next_race_name)
col1, col2, col3,col4 = st.columns(4)




with col1:
    first = st.selectbox(
        '1:a',
        driver_list)

with col2:
    second = st.selectbox(
        '2:a',
       driver_list)
with col3:
    third = st.selectbox(
        '3:a',
       driver_list)
with col4:
    better = st.selectbox(
    'Vem lägger bettet',
    ('Seb', 'Jonte', 'Filip','Marcus','Oskar'))
    
    



#st.write('You selected:', better)
image = Image.open('./assets/qr.png')


if st.button('Placera bet'):
    bet = st.write(create_bet(next_race, better, first, second, third))

    st.caption("Använd qr koden för att swisha in ditt bett!")
    st.image(image)

else:
    pass
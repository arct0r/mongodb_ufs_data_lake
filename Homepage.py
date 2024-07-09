import streamlit as st
from functions import mongoConnect
import pymongo

st.set_page_config(
    page_title="Homepage",
    page_icon="👋",
    layout='wide'
)

st.title('Quack quack motherfuckers 🐥')
'In this page you will be able to see the upcoming events and buy tickets for them. '

# Mi collego al client
client = mongoConnect()
# Carico il database
db = client['ufs_data_lake']
# Carico le 4 collections su streamlit
st.session_state['db'] = client['ufs_data_lake']
st.session_state['artists'] = db['artists']
st.session_state['events'] = db['events']
st.session_state['locations'] = db['locations']
st.session_state['tickets'] = db['tickets']

events = db['events'].find({})
events = [event for event in events]

with st.expander('Event json'):
    events

c1, c2 = st.columns(2)
columns = [c1,c2]

def print_event(event:dict):
            f'*Evento:* {event['event_name']}'
            f'*Artisti:* {event['artist']}'
            f'*Data:* {event['date']}'
            f'*Posti disponibili:* {event['slots']}'
            f'*Prezzo:* {event['price']} 🍌'
            f'*Descrizione:* {event['description']}'
            confirm_event = st.form_submit_button("Add to cart")


for i in range(0,len(events),2):
    with c1:
        with st.form(f'{i}'):
            print_event(events[i])
    with c2:
        try:
            with st.form(f'{i+1}'):
                print_event(events[i])
        except:
            pass



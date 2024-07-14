import streamlit as st
from functions import mongoConnect
from pymongo import MongoClient, GEOSPHERE
from functions import get_coordinates, reverseCoord
import datetime
from functions import filter_events
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderInsufficientPrivileges
import time
import random
import uuid

st.set_page_config(
    page_title="Homepage",
    page_icon="👋",
    layout='wide'
)

st.title('🐥 TicketDuck')
'In this page you will be able to see the upcoming events and buy tickets for them. '
past_events = st.toggle('Show Past Events')


# Mi collego al client
client = mongoConnect()
# Carico il database
db = client['ufs_data_lake']
# Carico le 4 collections su streamlit
st.session_state['db'] = client['ufs_data_lake']
st.session_state['artists'] = db['artists']
st.session_state['events'] = db['events']
st.session_state['locations'] = db['locations']
db['locations'].create_index([("location", "2dsphere")])
db['events'].create_index([("location_coordinates", "2dsphere")])
st.session_state['tickets'] = db['tickets']

artisti = db['artists'].find({})
if past_events:
    events = db['events'].find({})
elif not past_events:
    current_datetime = datetime.datetime.now()
    events = db['events'].find({
    'date': {'$gte': current_datetime}
    })
luoghi = db['locations'].find({})
events = [event for event in events]
luoghi = [luogo for luogo in luoghi]



with st.expander('Event json'):
    events

filters = {}

with st.expander('Search Filters'):
    filtered_events = {}
    col1,col2,col3= st.columns(3)
    with col1:
        artista_filtro = st.selectbox("Nome artista", options=[a['artist'] for a in artisti], index = None)
        nome_evento_filtro = st.text_input("Nome evento")         
    with col2:
        data_start = st.date_input("Da")
        data_end = st.date_input("A", value=None)
    with col3:
        luogo_filtro = st.text_input("Luogo")
        distanza_filtro = st.slider(label='Distanza dal luogo in km', min_value = 1, max_value = 7, step=1, value=None)
    add = st.button('Conferma')
    reset = st.button('Resetta i filtri')

    if add:
        if artista_filtro:
            filters['artisti'] = artista_filtro
        if nome_evento_filtro:
            filters['nome_evento'] = nome_evento_filtro
        if data_start and data_end:
            filters['date'] = {'start' : data_start, 'end' : data_end}
        if luogo_filtro and distanza_filtro:
            coordinates = get_coordinates(luogo_filtro)
            if coordinates != 'Non ho trovato il luogo':
                filters['luogo_filtro'] = luogo_filtro
                filters['coordinate'] = (coordinates[1], coordinates[0])  # [longitude, latitude]
                filters['distanza'] = distanza_filtro
        filtered_events = filter_events(db['events'], filters)
        events = [event for event in filtered_events]


    # Mostro i filtri
    filters






c1, c2 = st.columns(2)
columns = [c1,c2]

def print_event(event:dict):
            
            st.subheader(f':violet[**{event['event_name']}**]')
            f'👨‍🎨 :blue[*Artisti:*] {', '.join(event['artist'])}'
            f'📅 :blue[*Data:*] {event['date'].strftime("**%d/%m**, %H:%M")}'
            f'🗺️ :blue[*Location:*] {event['location']}, {event['location_city']}'
            f'🎟️ :blue[*Posti disponibili:*] {event['freeSlots']}'
            f'🤑 :blue[*Prezzo:*] {event['price']} 🍌'
            f'{event['description']}'
            confirm_event = st.form_submit_button("Add to cart")
            if confirm_event:
                if int(event['freeSlots']) != 0:
                    try:
                        st.session_state['cart'].append({'evento':event['event_name'], 'price':event['price']})
                    except: 
                        st.session_state['cart'] = [{'evento':event['event_name'], 'price':event['price']}]



for i in range(0,len(events),2):
    with c1:
        with st.form(f'{i}'):
            print_event(events[i])

    with c2:
        try:
            with st.form(f'{i+1}'):
                print_event(events[i+1])
        except:
            pass



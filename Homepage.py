import streamlit as st
from functions import mongoConnect
from pymongo import MongoClient, GEOSPHERE, ASCENDING
from functions import get_coordinates, reverseCoord
import datetime
from functions import filter_events
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderInsufficientPrivileges
import time
import random
import uuid
from pages.Load import tags_opt
from functions import filter_query

st.set_page_config(
    page_title="Homepage",
    page_icon="🐥",
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
st.session_state['tickets'] = db['tickets']

db['locations'].create_index([("location", "2dsphere")])
db['events'].create_index([("location_coordinates", "2dsphere")])
st.session_state['tickets'] = db['tickets']

current_datetime = datetime.datetime.now()

artisti = db['artists'].find({})
if past_events:
    events = db['events'].find({}).sort('date', ASCENDING)
elif not past_events:
    current_datetime = datetime.datetime.now()
    events = db['events'].find({
    'date': {'$gte': current_datetime}
    }).sort('date', ASCENDING)
luoghi = db['locations'].find({})
events = [event for event in events]
luoghi = [luogo for luogo in luoghi]


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
        distanza_filtro = st.text_input(label='Distanza dal luogo in km', value=None)
    with col1: 
        add = st.button('Conferma')
        reset = st.button('Resetta i filtri')
    with col3:
        tags = st.selectbox(label='Tags', options=tags_opt, index=None)

    if add:
        if artista_filtro:
            filters['artisti'] = artista_filtro
        if nome_evento_filtro:
            filters['nome_evento'] = nome_evento_filtro
        if data_start and data_end:
            filters['date'] = {'start' : data_start, 'end' : data_end}
        if luogo_filtro and distanza_filtro:
            try:
                distanza_filtro_km = int(distanza_filtro.strip())
                coordinates = get_coordinates(luogo_filtro)
                if coordinates != 'Non ho trovato il luogo':
                    filters['coordinate'] = (coordinates[1], coordinates[0])  # [longitude, latitude]
                    filters['distanza'] = distanza_filtro_km
            except:
                st.error('Distanza non valida') 
        if tags:
            filters['tags'] = tags
        query = str(filter_query(filters))

        filtered_events = filter_events(db['events'], filters)
        events = [event for event in filtered_events]
        st.code('db.events.find('+query+')')



    # Mostro i filtri
    with col2:
        filters








c1, c2 = st.columns(2)
columns = [c1,c2]

def print_event(event:dict):
            
            st.subheader(f":violet[**{event['event_name']}**]")
            f"📅 :blue[*Data:*] {event['date'].strftime('**%d/%m**, %H:%M')}, :orange[***| {', '.join(event['tags'])}***]"
            f"👨‍🎨 :blue[*Artisti:*] {', '.join(event['artist'])}"
            f"🗺️ :blue[*Location:*] {event['location']}, {event['location_city']}"
            f"🎟️ :blue[*Posti disponibili:*] {event['freeSlots']}"
            f"🤑 :blue[*Prezzo:*] {event['price']} 🍌"
            f"{event['description']}"
            confirm_event = st.form_submit_button("Add to cart")
            if confirm_event:
                if int(event['freeSlots']) != 0:
                    if int(event['freeSlots'])>0 and event['date'] > current_datetime:
                        try:
                            st.session_state['cart'].append({'evento':event['event_name'], 'price':event['price'], 'artist':event['artist'], '_id':event['_id']})
                            st.toast(f"Ho aggiunto {event['event_name']} al carrello")
                        except: 
                            st.session_state['cart'] = []
                    else:
                        st.error("Il concerto non è piu' disponibile")



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



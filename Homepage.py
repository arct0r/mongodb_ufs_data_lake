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
from functions import filter_query, get_and_resize_artist_image

st.set_page_config(
    page_title="Homepage",
    page_icon="🐥",
    layout='wide'
)

st.title('🐥 TicketQuack')
'In this page you will be able to see the upcoming events and buy tickets for them. '
past_events = st.toggle('Show Past Events')


# Mi collego al client
client = mongoConnect()
# Carico il database
db = client['ufs_data_lake']
# Inizializzo le 4 collections e le carico su streamlit
st.session_state['db'] = client['ufs_data_lake']
st.session_state['artists'] = db['artists']
st.session_state['events'] = db['events']
st.session_state['locations'] = db['locations']
st.session_state['tickets'] = db['tickets']
st.session_state['tickets'] = db['tickets']

# Questi index mi servono per usare le geoqueries
db['locations'].create_index([("location", "2dsphere")])
db['events'].create_index([("location_coordinates", "2dsphere")])

# La current date mi serve per qualcosa dopo
current_datetime = datetime.datetime.now()

# Mi serve la lista degli artisti per poterla usare nei filtri 
artisti = db['artists'].find({})
if 'artisti_pictures' not in st.session_state:
    try:
        st.session_state.artisti_pictures = {a['artist']:get_and_resize_artist_image(a['artist']) for a in artisti}
    except:
        print("Non sono riuscito a caricare le immagini degli artisti")

# Carico gli eventi da mostrare nella homepage in base al toggle past_events
if past_events:
    events = db['events'].find({}).sort('date', ASCENDING)
elif not past_events:
    current_datetime = datetime.datetime.now()
    events = db['events'].find({
    'date': {'$gte': current_datetime} # gte current datetime = da oggi in poi. Non mostro la roba vecchia
    }).sort('date', ASCENDING) # Il sort è per ordinare dal piu' recente 

# luoghi = db['locations'].find({})
# luoghi = [luogo for luogo in luoghi]
events = [event for event in events]


filters = {}
# Inizializzo il dizionario per i filtri

with st.expander('Search Filters'):
    filtered_events = {}
    # E quello per gli eventi filtrati
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
        # Per mostrare la query che sto eseguendo

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
            if ('Concerto' or 'Spettacolo' or 'Musica' or 'Classica' or 'Jazz' or 'Rock' or 'Arte' or 'Musica') in event['tags']:
                try:
                    st.image(image=st.session_state.artisti_pictures[event['artist'][0]])
                except:
                    print(f"Non ho trovato l'immagine per {event['artist']}")
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
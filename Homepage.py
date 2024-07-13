import streamlit as st
from functions import mongoConnect
import pymongo

st.set_page_config(
    page_title="Homepage",
    page_icon="👋",
    layout='wide'
)

st.title('🐥 TicketDuck')
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
st.session_state['cart'] = []


artisti = db['artists'].find({})
events = db['events'].find({})
luoghi = db['locations'].find({})
events = [event for event in events]
luoghi = [luogo for luogo in luoghi]



with st.expander('Event json'):
    events

filters = {}

with st.expander('Search Filters'):
    col1,col2,col3= st.columns(3)
    with col1:
        artista_filtro = st.selectbox("Nome artista", options=[a['artist'] for a in artisti])
        nome_evento_filtro = st.text_input("Nome evento")         
    with col2:
        data_start = st.date_input("Da")
        data_end = st.date_input("A")
    with col3:
        luogo_filtro = st.text_input("Luogo")
        distanza_filtro = st.slider(label='Distanza dal luogo in km', min_value = 1, max_value = 7, step=1)
    add = st.button('Conferma')
    if add:
        if artista_filtro:
            filters['artisti'] = artista_filtro
    reset = st.button('Resetta i filtri')
    if reset:
        filters.clear()


filters



c1, c2 = st.columns(2)
columns = [c1,c2]

def print_event(event:dict):
            f':blue[*Evento:*] {event['event_name']}'
            f':blue[*Artisti:*] {', '.join(event['artist'])}'
            f':blue[*Data:*] {event['date']}'
            f':blue[*Posti disponibili:*] {event['freeSlots']}'
            f':blue[*Prezzo:*] {event['price']} 🍌'
            f':blue[*Descrizione:*] {event['description']}'
            f':blue[*Location:*] {event['location']}'
            confirm_event = st.form_submit_button("Add to cart")
            if confirm_event:
                 st.session_state['cart'].append({'evento':event['event_name'], 'price':event['price']})


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



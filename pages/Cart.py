import streamlit as st
import time 
from functions import load_ticket, mongoConnect 

st.set_page_config(
    page_title="Cart",
    page_icon="👋",
)


st.title('Cart')
# Bugfixing
if ('db' or 'artists' or 'events' or 'locations' or 'tickets') not in st.session_state:
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
if not 'cart' in st.session_state:
    st.session_state['cart'] = []

'In this page you will be able to buy selected events.'
for event in st.session_state['cart']:
    st.code(f'''{event['evento']}, {event['artist'][0]}, {event['price']} $''')

st.subheader(f"Totale: {sum(int(event['price']) for event in st.session_state['cart'])} $")

col1,col2, col3 = st.columns([2,2,6])

with col1:
    clear_cart = st.button('Clear Cart')
with col2:
    checkout = st.button('Checkout')
nominativo = st.text_input('Inserisci un nominativo per i biglietti')

if clear_cart:
    st.session_state['cart'] = []


if checkout and len(st.session_state['cart'])!=0 and nominativo.strip():

    with st.spinner("Buying..."):
                for event in st.session_state['cart']:
                    SN = load_ticket(event, nominativo)
                    st.success(f"Ecco il tuo ticket per {event['evento']}: | ***{SN}*** |" )
                    st.session_state['cart'] = []
                    st.balloons()

with st.expander('Biglietti emessi'):
     tickets = st.session_state['tickets'].find({})
     'Comando per ottenere tutti i ticket:'
     st.code("st.session_state['tickets'].find({})")
     [ticket for ticket in tickets]
with st.expander('Biglietti emessi, GROUP BY PER IL NOMINATIVO'):
     st.code('''pipeline_tickets_nominativo = [
    # Unwind the tickets array
    {"$unwind": "$tickets"},

    # Group by nominativo
    {"$group": {
        "_id": "$tickets.nominativo",
        "tickets": {"$push": {
            "event_name": "$event_name",
            "event_id": "$event_id",
            "ticket_id": "$tickets.ticket_id"
        }}
    }},
    
    # Sort by nominativo (optional)
    {"$sort": {"_id": 1}}
    ]
     pipeline_tickets_result = st.session_state['tickets'].aggregate(pipeline_tickets_nominativo)''')
     pipeline_tickets_nominativo = [
    # Unwind the tickets array
    {"$unwind": "$tickets"},

    # Group by nominativo
    {"$group": {
        "_id": "$tickets.nominativo",
        "tickets": {"$push": {
            "event_name": "$event_name",
            "event_id": "$event_id",
            "ticket_id": "$tickets.ticket_id"
        }}
    }},
    
    # Sort by nominativo (optional)
    {"$sort": {"_id": 1}}
    ]
     pipeline_tickets_result = st.session_state['tickets'].aggregate(pipeline_tickets_nominativo)
     [ticket for ticket in pipeline_tickets_result]


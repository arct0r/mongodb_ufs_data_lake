import streamlit as st
import time 
from functions import load_ticket

st.set_page_config(
    page_title="Cart",
    page_icon="👋",
)

st.title('Cart')

'In this page you will be able to buy selected events.'
for event in st.session_state['cart']:
    st.code(f'''{event['evento']}, {event['artist'][0]}, {event['price']} 🍌, ID: {event['_id']}''')

st.subheader(f"Totale: {sum(int(event['price']) for event in st.session_state['cart'])} 🍌")

col1,col2, col3 = st.columns([2,2,6])

with col1:
    clear_cart = st.button('Clear Cart')
with col2:
    checkout = st.button('Checkout')

if clear_cart:
    st.session_state['cart'] = []


if checkout and len(st.session_state['cart'])!=0:

    with st.spinner("Buying..."):
                for event in st.session_state['cart']:
                    SN = load_ticket(event)
                    st.success(f"Ecco il tuo ticket per {event['evento']}: | ***{SN}*** |" )
                    st.session_state['cart'] = []

with st.expander('Biglietti emessi'):
     tickets = st.session_state['tickets'].find({})
     [ticket for ticket in tickets]


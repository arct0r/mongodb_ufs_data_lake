import streamlit as st
import time 
from functions import check_for_availabily, remove_slot_from_event, load_ticket

st.set_page_config(
    page_title="Cart",
    page_icon="👋",
)

st.title('Cart')

'In this page you will be able to buy selected events.'

clear_cart = st.button('Clear Cart')
if clear_cart:
    st.session_state['cart'] = []
st.session_state['cart']

st.subheader(f'Totale: {None}')
checkout = st.button('Checkout')
if checkout and len(st.session_state['cart'])!=0:

    with st.spinner("Buying..."):
        for event in st.session_state['cart']:
            if check_for_availabily(event)==True:
                remove_slot_from_event(event)
                SN = load_ticket(event)
                st.sucess(f'Acquisto effettuato correttamente. Ecco il tuo ticket per {event['evento']}: ***{SN}')


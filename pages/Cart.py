import streamlit as st
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

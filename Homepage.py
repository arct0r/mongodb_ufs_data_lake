import streamlit as st
from functions import mongoConnect
import pymongo

st.set_page_config(
    page_title="Homepage",
    page_icon="👋",
)

st.title('Quack quack motherfuckers 🐥')
'In this page you will be able to see the upcoming events and buy tickets for them. '

# Mi collego al client
client = mongoConnect()
# Carico il database
db = client['ufs_data_lake']
# Carico le 4 collections su streamlit
st.session_state['artists'] = db['artists']
st.session_state['events'] = db['events']
st.session_state['locations'] = db['locations']
st.session_state['tickets'] = db['tickets']

# Test
print(db.list_collection_names())
[i for i in db.list_collection_names()]
'a'


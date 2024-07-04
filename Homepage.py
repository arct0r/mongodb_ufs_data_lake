import streamlit as st
from functions import mongoConnect
import pymongo

st.set_page_config(
    page_title="Homepage",
    page_icon="👋",
)

st.title('Quack quack motherfuckers 🐥')
'In this page you will be able to see the upcoming events and buy tickets for them. '

# Testing cnnection
client = mongoConnect()
db = client['ufs_data_lake']
print(db.list_collection_names())
[i for i in db.list_collection_names()]

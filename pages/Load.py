import streamlit as st
import json
st.set_page_config(
    page_title="Homepage",
    page_icon="👋",
)

st.title('Add new stuff to the database')
tab1, tab2, tab3 = st.tabs(["Event", "Artist", "Location"])

with tab1:
    st.subheader('Add Event')
    with st.form("Add Event"):
        col1,col2 = st.columns(2)
        with col1:
            event_name = st.text_input("Event name")
            artist = st.multiselect("Artist name", options=[])
            location = st.multiselect(label="Location", options=[])
        with col2:
            price = st.text_input("Price in 🍌")
            slots = st.text_input("Slots")
            date = st.date_input("Event date")   
        description = st.text_area("Event description")
        confirm_event = st.form_submit_button("Submit")

with tab2:
    st.subheader('Add Artist')
    with st.form("Add Artist"):
        name = st.text_input("Artist name")
        confirm_artist = st.form_submit_button("Submit")

with tab3:
    st.subheader('Add Location')
    with st.form("Add Location"):
        col1,col2 = st.columns(2)
        with col1:
            location_name = st.text_input("Location Name")
            location_city = st.text_input("Location City")
        with col2:
            location_country = st.text_input("Location Country")
            coordinates = st.text_input("Coordinates")
        confirm_location = st.form_submit_button("Submit")






import streamlit as st
import json
import datetime
from datetime import date
from datetime import datetime
from functions import get_coordinates  

st.set_page_config(
    page_title="Homepage",
    page_icon="👋",
)

artists = st.session_state['artists'].distinct('artist')
locations = st.session_state['locations'].distinct('location_name')

with st.expander('Locations, Artists'):
    artists
    locations


def add_event (event_name, artist, location, price, slots, date, description):
    try:
        st.session_state['events'].insert_one({'event_name':event_name,
                                                'artist':artist,
                                                'location':location,
                                                'price':price,
                                                'slots':slots,
                                                'date':date,
                                                'description':description})
        st.success(f'Added {event_name}')
    except:
        st.error('Could not add the event')


st.title('Add new stuff to the database')
tab1, tab2, tab3 = st.tabs(["Event", "Artist", "Location"])

with tab1:
    st.subheader('Add Event')
    with st.form("Add Event"):
        col1,col2 = st.columns(2)
        with col1:
            event_name = st.text_input("Event name")
            artist = st.multiselect("Artist name", options=artists)
            location = st.selectbox(label="Location", options=locations)
        with col2:
            price = st.text_input("Price in 🍌")
            slots = st.text_input("Slots")
            date = st.date_input("Event date")
            hour = st.time_input("Ora dell'evento")
        description = st.text_area("Event description")
        confirm_event = st.form_submit_button("Submit")
        if confirm_event and event_name and artist and location and price and slots and date and hour and description:
            date_combined = datetime.combine(date, hour)
            add_event(event_name, artist, location, price, slots, date_combined, description)
            


with tab2:
    st.subheader('Add Artist')
    with st.form("Add Artist"):
        name = st.text_input("Artist name")
        confirm_artist = st.form_submit_button("Submit")
        if name and name not in ['', ' '] and confirm_artist:
            try:
                st.session_state['artists'].insert_one({'artist': name})
                st.success(f'Added {name}')
            except: 
                st.error(f'Could not add {name}')

with tab3:
    st.subheader('Add Location')
    with st.form("Add Location"):
        col1,col2 = st.columns(2)
        with col1:
            location_street = st.text_input("Location Street")
            location_city = st.text_input("Location City")
        with col2:
            location_country = st.text_input("Location Country")
            location_name = st.text_input('Nome della location')
        confirm_location = st.form_submit_button("Submit")
        if (location_street and location_city and location_country and location_name) not in ['', ' '] and confirm_location:
                #st.session_state['locations'].insert_one({'location_name': location_name})
                location = f"{location_street.strip()}, {location_city.strip()}, {location_country.strip()}"
                coordinates = get_coordinates(location)
                coordinates
                st.success(f'Added {location}')







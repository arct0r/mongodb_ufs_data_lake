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
st.session_state['cart'] = []

artists = st.session_state['artists'].distinct('artist')
locations = st.session_state['locations'].distinct('name')
full_locations = [location for location in st.session_state['locations'].find({})]
full_locations_processed = {}
for loc in full_locations:
    full_locations_processed[loc['name']] = loc
full_locations_processed
with st.expander('Locations, Artists'):
        artists
        full_locations


#full_locations_processed['Kebab Anatolia ']['location']
def add_event (event_name, artist, location, price, slots, date, description):
    try:
        st.session_state['events'].insert_one({'event_name':event_name,
                                                'artist':artist,
                                                'location':location,
                                                'location_coordinates':full_locations_processed[location]['location'],
                                                'location_city':full_locations_processed[location]['city'],
                                                'location_street':full_locations_processed[location]['street'],
                                                'location_country':full_locations_processed[location]['country'],
                                                'price':price,
                                                'slots':slots,
                                                'freeSlots':slots,
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
            try:
                date_combined = datetime.combine(date, hour)
                add_event(event_name, artist, location, price, slots, date_combined, description)
            except:
                st.error("Coudln't add the event")
            


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
                location = f"{location_street.strip()}, {location_city.strip()}, {location_country.strip()}"
                try:
                    coordinates = get_coordinates(location)
                    st.session_state['locations'].insert_one({
                        'location': {
                            'type': 'Point',
                            'coordinates': [coordinates[1], coordinates[0]]  # [longitude, latitude] 
                            # Devo invertirli perchè il GeoJSON format li vuole invertiti
                            # GeoJSON https://geojson.org/
                        },
                        'street': location_street,
                        'country': location_country,
                        'city': location_city,
                        'name': location_name
                    })
                    st.success(f'Added {location}')
                except:
                    st.error(f"Coudln't add {location}")






import streamlit as st
from geopy.geocoders import Nominatim
# Inizializza il geocodificatore
geolocator = Nominatim(user_agent="geoapiExercises")

# Funzione per ottenere le coordinate geografiche
def get_geocode(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        print("Impossibile ottenere le coordinate.")
        return None, None
# Input dall'utente
address = input("Inserisci un indirizzo: ")

# Ottieni le coordinate geografiche
lat, lon = get_geocode(address)
if lat and lon:
    print(f'Le coordinate di "{address}" sono: latitudine {lat}, longitudine {lon}')
    
    # Converte le coordinate
    x, y = convert_coordinates(lat, lon)
    print(f'Le coordinate UTM sono: {x}, {y}')
else:
    print('Impossibile ottenere le coordinate.')
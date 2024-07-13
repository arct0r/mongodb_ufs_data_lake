from pymongo import MongoClient
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderInsufficientPrivileges
import time
import random
import uuid

def mongoConnect ():
    connection_url = "mongodb+srv://scimmiotto:ciao123@cluster0.tjaswsm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(connection_url)  
    return client


def get_coordinates(address):
    # Creo uno user per fare le richieste su Nomatim. Senno` mi da` errore. Uso uuid per generare il codice
    user_agent = f"MongoConcertApp/{uuid.uuid4()}"
    
    # Oggetto Nomatim per ottenere le coordinate
    geolocator = Nominatim(user_agent=user_agent)
    
    try:        
        location = geolocator.geocode(address)
        
        if location:
            return (location.latitude, location.longitude)
        else:
            return "Non ho trovato il luogo"
    except (GeocoderTimedOut, GeocoderUnavailable, GeocoderInsufficientPrivileges) as e:
        return f"Error: {str(e)}"
    # Per gestire le eccezioni

from pymongo import MongoClient
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderInsufficientPrivileges
import time
import random
import uuid

import datetime
from bson import ObjectId

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

def reverseCoord(latitude, longitude):
    user_agent = f"MongoConcertApp/{uuid.uuid4()}"
    # Oggetto Nomatim per ottenere le coordinate
    geolocator = Nominatim(user_agent=user_agent)

    # Perform reverse geocoding
    location = geolocator.reverse((latitude, longitude))

    # Print the address
    print(location.address)



def filter_query(filters):
    query = {}
    print("Filtri in entrata:", filters)
    if 'artisti' in filters:
        query['artist'] = filters['artisti']
    if 'nome_evento' in filters:
        query['event_name'] = {'$regex': filters['nome_evento'], '$options': 'i'}
    if 'date' in filters:
        start_date = datetime.datetime.combine(filters['date']['start'], datetime.time.min)
        end_date = datetime.datetime.combine(filters['date']['end'], datetime.time.max)
        query['date'] = {
            '$gte': start_date,
            '$lte': end_date
        }
    if 'luogo_filtro' in filters:
        query['location'] = {'$regex': filters['luogo_filtro'], '$options': 'i'}
    if 'coordinate' in filters and 'distanza' in filters:
        lon, lat = filters['coordinate']
        query['location_coordinates'] = {
            '$nearSphere': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': [lon, lat]
                },
                '$maxDistance': filters['distanza'] * 1000
                # Questo serve per convertire i km in metri
            }
        }
    if 'tags' in filters:
        query['tags'] = filters['tags']
    print("Query finale:", query)
    return query

def filter_events(collection, filters):
    query = filter_query(filters)
    events = list(collection.find(query))
    return events

def check_for_availabily(event):
    pass
def remove_slot_from_event(event):
    pass
def load_ticket(event):
    pass
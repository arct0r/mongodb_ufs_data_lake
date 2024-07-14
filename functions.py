from pymongo import MongoClient, ReturnDocument
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderInsufficientPrivileges
import time
import random
import uuid
import streamlit as st

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
        # $options : i era "Case insensitivity to match upper and lower cases. "
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


def load_ticket(event):
    events_collection = st.session_state['events']
    tickets_collection = st.session_state['tickets']

    # Cerco di ridurre 'freeSlots' nella collection degli eventi
    updated_event = events_collection.find_one_and_update(
        {
            '_id': event['_id'],
            'freeSlots': {'$gt': 0}  #$gt è 'greater than'. Si assicura che ci siano piu' di 0 tickets disponibili.
        },
        {'$inc': {'freeSlots': -1}},
        return_document=ReturnDocument.AFTER
    )

    if updated_event:
        print(f"Sono riuscito a ridurre gli slots per {event['evento']}: {updated_event['freeSlots']} posti rimasti")
        
        # Genero un uuid per il ticket
        ticket_id = str(uuid.uuid4())

        # Creo un nuovo dizionario per il ticket
        new_ticket = {
            'ticket_id': ticket_id,
        }

        result = tickets_collection.update_one(
            {'event_id': event['_id'], 'event_name':event['evento']},
            {'$push': {'tickets': new_ticket}},
            upsert=True
        ) # Questo mi 'spinge' il ticket dentro alla collections dei tickets.
        # Se è la prima volta che viene emesso un ticket per un determinato evento allora viene creato un nuovo oggetto per quel evento dentro la collection di tickets.

        if result.modified_count > 0 or result.upserted_id:
            print(f"Ticket {ticket_id} added to event {event['_id']}")
            return ticket_id
        else:
            print("Non sono riuscito ad aggiungere il ticket alla collections dei tickets")
            return None
    else:
        print("Non ci sono piu' biglietti disponibili!")
        return None

    

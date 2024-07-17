from pymongo import MongoClient, ReturnDocument
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderInsufficientPrivileges
import time
import random
import uuid
import streamlit as st
import datetime

import requests
import io
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def mongoConnect ():
    connection_url = st.secrets["DB_URL"]
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


def filter_query(filters):
    query = {}
    print("Filtri in entrata:", filters)
    if 'artisti' in filters:
        query['artist'] = filters['artisti']
        # Semplice semplice. Non serve il regex per gli artisti
    if 'nome_evento' in filters:
        query['event_name'] = {'$regex': filters['nome_evento'], '$options': 'i'}
        # Uso il regex per il nome_evento
    if 'date' in filters:
        start_date = datetime.datetime.combine(filters['date']['start'], datetime.time.min) # Devo fare un combine per il datetime da streamlit a mongo
        end_date = datetime.datetime.combine(filters['date']['end'], datetime.time.max)
        query['date'] = {
            '$gte': start_date, # greather than starting date
            '$lte': end_date # less than end date
        }
   # if 'luogo_filtro' in filters:
    #    query['location'] = {'$regex': filters['luogo_filtro'], '$options': 'i'}
        # $options : i era "Case insensitivity to match upper and lower cases. "
        # Non serve piu'. Cerco direttamente le coordinate
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


def load_ticket(event, nominativo):
    events_collection = st.session_state['events']
    tickets_collection = st.session_state['tickets']

    # Cerco di ridurre 'freeSlots' nella collection degli eventi
    print(f"Cerco di ridurre lo slot per {event['_id']}")
    updated_event = events_collection.find_one_and_update(
        {
            '_id': event['_id'],
            'freeSlots': {'$gt': 0}  #$gt è 'greater than'. Si assicura che ci siano piu' di 0 tickets disponibili.
        }, # Il primo dizionario è per "findare"
        {'$inc': {'freeSlots': -1}},
        return_document=ReturnDocument.AFTER
    ) # Il secondo è per fargli eseguire qualcosa su ciò che ha trovato

    if updated_event: # Se ha trovato un documento e ridotto gli slots liberi...
        print(f"Sono riuscito a ridurre gli slots per {event['evento']}: {updated_event['freeSlots']} posti rimasti")
        
        # Genero un uuid per il ticket
        ticket_id = str(uuid.uuid4())

        # Creo un nuovo dizionario per il ticket
        new_ticket = {
            'ticket_id': ticket_id,
            'nominativo': nominativo
        }

        result = tickets_collection.update_one(
            {'event_id': event['_id'], 'event_name':event['evento']},
            {'$push': {'tickets': new_ticket}},
            upsert=True
        ) # Questo mi 'spinge' il ticket dentro alla collections dei tickets.
        # Se è la prima volta che viene emesso un ticket per un determinato evento allora viene creato un nuovo oggetto per quell'evento dentro la collection di tickets.

        if result.modified_count > 0 or result.upserted_id: # Modified count se aggiunge, upserted_id se ha creato una nuova entry
            print(f"Ticket {ticket_id} aggiunto all'evento {event['_id']}")
            return ticket_id
        else:
            print("Non sono riuscito ad aggiungere il ticket alla collections dei tickets")
            return None
    else:
        print("Non ci sono piu' biglietti disponibili!")
        return None


def get_and_resize_artist_image(artist_name, size=(150, 150)):
    # Spotify client, credenziali
    client_credentials_manager = SpotifyClientCredentials(
        client_id=st.secrets['spoti_client'],
        client_secret=st.secrets['spoti_client_secret']
    ) # Spotify client, lo inizializzo
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Cerco l'artista
    print(f'Cerco {artist_name}')
    results = sp.search(q='artist:' + artist_name, type='artist')
    artists = results['artists']['items']
    #print(artists[0]['images'])
    if not artists:
        return None

    # Piglio il primo artista
    artist = artists[0]
    if not artist['images']: 
        return None

    image_url = artist['images'][0]['url']
    # Pheega che comodo 

    # Scarico l'immagine
    response = requests.get(image_url)
    if response.status_code != 200:
        return None 

    # Apro l'immagin e faccio un resize
    image = Image.open(io.BytesIO(response.content))
    resized_image = image.resize(size)

    return resized_image

# metodo semplicissimo per ottenere la location dell'user in base all'IP
def get_user_location():
    response = requests.get('https://ipapi.co/json/')
    if response.status_code == 200:
        data = response.json()
        return [data.get('latitude'), data.get('longitude')]
    return None


user_location = get_user_location()
print(user_location)

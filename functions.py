from pymongo import MongoClient

def mongoConnect ():
    connection_url = "mongodb+srv://scimmiotto:ciao123@cluster0.tjaswsm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(connection_url)  
    return client


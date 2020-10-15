from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from typing import Dict
from mongoengine import connect,disconnect
from mongoengine import errors
from schemas import *
import os

MONGODB_ADDR = "52.255.160.180" #os.environ.get("MONGODB_ADDR", "chaos.mongodb.openshift")
MONGODB_PORT = os.environ.get("MONGODB_PORT", 8080)
DB_NAME = os.environ.get("DB_NAME", "chaos")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", 5001))

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def create_db_client():
    try:
        ## Add authentication
        connect(db=DB_NAME, host=MONGODB_ADDR, port=MONGODB_PORT)
    except errors.ServerSelectionTimeoutError:
        print("error connecting to mongodb")

@app.on_event("shutdown")
async def shutdown_db_client():
    pass

@app.get("/{collection}")
def read_object(collection: Collections):
    # Get all documents from collection
    collection = get_collection_object(collection)
    output = [document.to_dict() for document in collection.objects]
    return output

@app.get("/{collection}/{doc_id}")
def read_one_object(collection: Collections,doc_id: str):
    try:
        # Get specific document from collection depending on route
        # try to get first document, considering there could not be more then 1
        collection_object = get_collection_object(collection)
        doc_identifier_to_doc_id = {collection_object.get_identifier() : doc_id}
        # Get all objects that have the doc_id and
        # return the first one as a dict
        output = collection_object.objects(**doc_identifier_to_doc_id)[0].to_dict()
    except (IndentationError, IndexError):
        output = f"No such document '{doc_id}' in '{collection}' collection"
    return output

@app.post("/{collection}/{doc_id}")
def write_object(collection: Collections, document: Dict = {}):
    try:
        collection = get_collection_object(collection)
        document = collection(**document)
        document.save()
        return document.to_dict()
    except TypeError as E:
        print(E)
        return 'missing parameters'
    except (errors.FieldDoesNotExist , errors.ValidationError):
        return 'unknown parameter '


@app.put("/{collection}/{doc_id}")
def update_object(collection: Collections, doc_id : str, document: Dict = {}):
    try:
        collection_object = get_collection_object(collection)
        doc_identifier_to_doc_id = {collection_object.get_identifier() : doc_id}
        document_object = collection_object.objects(**doc_identifier_to_doc_id)[0]
        document_object.update(**document)
        document_object.save()
        document_object = collection_object.objects(**doc_identifier_to_doc_id)[0]
        return document_object.to_dict()
    except TypeError:
        return 'missing parameters'
    except (errors.FieldDoesNotExist , errors.ValidationError):
        return 'unknown parameter '

def get_collection_object(collection):
    if collection == Collections.servers:
        document = Server
    elif collection == Collections.groups:
        document = Group
    elif collection == Collections.probes:
        document = Probe
    elif collection == Collections.methods:
        document = Method
    elif collection == Collections.rollbacks:
        document = Rollback
    elif collection == Collections.logs:
        document = Log
    return document
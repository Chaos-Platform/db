from fastapi import FastAPI
from typing import Dict
from mongoengine import connect,disconnect
from mongoengine import errors
from schemas import *
import os

mongodb_addr = "52.255.160.180" #os.environ.get("MONGODB_ADDR", "chaos.mongodb.openshift")
mongodb_port = os.environ.get("MONGODB_PORT", 8080)
db_name = os.environ.get("DB_NAME", "chaos")
listen_port = int(os.environ.get("LISTEN_PORT", 5001))


app = FastAPI()

@app.on_event("startup")
async def create_db_client():
    try:
        connect(db=db_name, host=mongodb_addr, port=mongodb_port)
    except errors.ServerSelectionTimeoutError:
        print("error connecting to mongodb")

@app.on_event("shutdown")
async def shutdown_db_client():
    pass

@app.get("/{collection}")
def read_object(collection: str):
    # Get all documents from collection
    if collection == "servers":
        output = [server.to_dict() for server in Server.objects]
    elif collection == "groups":
        output = [group.to_dict() for group in Group.objects]
    elif collection == "probes":
        output = [probe.to_dict() for probe in Probe.objects]
    elif collection == "methods":
        output = [method.to_dict() for method in Method.objects]
    elif collection == "rollbacks":
        output = [rollback.to_dict() for rollback in Rollback.objects]
    elif collection == "logs":
        output = [log.to_dict() for log in Log.objects]
    else:
        output = None
    return output

@app.get("/{collection}/{doc_id}")
def read_object(collection: str,doc_id:str):
    try:
        # Get specific document from collection depending on route
        # try to get first document, considering there could not be more then 1
        if collection == "servers":
            output = Server.objects(dns = doc_id)[0].to_dict()
        elif collection == "groups":
            output = Group.objects(name = doc_id)[0].to_dict()
        elif collection == "probes":
            output = Probe.objects(name = doc_id)[0].to_dict()
        elif collection == "methods":
            output = Method.objects(name = doc_id)[0].to_dict()
        elif collection == "rollbacks":
            output = Rollback.objects(name = doc_id)[0].to_dict()
        elif collection == "logs":
            output = Log.objects(name = doc_id)[0].to_dict()
        else:
            output = None
    except (IndentationError, IndexError):
        output = f"No such document '{doc_id}' in '{collection}' collection"


    return output

@app.post("/{collection}/{doc_id}")
def write_object(collection: str, doc_id : str, document: Dict = {}):
    try:
        # Create document object with type depending on route
        if collection == "servers":
            document = Server(dns = doc_id, **document)
        elif collection == "groups":
            document = Group(name = doc_id, **document)
        elif collection == "probes":
            document = Probe(name = doc_id, **document)
        elif collection == "methods":
            document = Method(name = doc_id, **document)
        elif collection == "rollbacks":
            document = Rollback(name = doc_id, **document)
        elif collection == "logs":
            document = Log(name = doc_id, **document)

        document.save()
        return document.to_dict()
    except TypeError:
        return 'missing parameters'
    except (errors.FieldDoesNotExist , errors.ValidationError):
        return 'unknown parameter parameters'

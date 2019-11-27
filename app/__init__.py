from flask import Flask
import os
from config import Config
from flask_pymongo import PyMongo, MongoClient
from bson.objectid import ObjectId

# initiates an instace of the flask and assigns it to app
app = Flask(__name__) 
app.config.from_object(Config) 

# Passes the MongoURI and assigns the correct collection to db to access it in routes.
client = MongoClient(Config.MONGO_URI)
db = client.hfc_stats

# has to be imported after the instace on the flask app has been created.
from app import routes
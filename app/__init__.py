from flask import Flask
import os
from config import Config
from flask_pymongo import PyMongo, MongoClient
from bson.objectid import ObjectId

app = Flask(__name__) # initiates an instace of the flask app
app.config.from_object(Config) 

client = MongoClient(Config.MONGO_URI)
db = client.hfc_stats

mongo = PyMongo(app)

from app import routes # has to be imported after the instace on the flask app has been created.
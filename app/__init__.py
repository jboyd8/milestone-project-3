from flask import Flask
import os
from config import Config
from flask_pymongo import PyMongo, MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(Config.MONGO_URI)
#add db here

from app import routes # has to be imported after the instace on the flask app has been created.
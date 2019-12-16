from flask import Flask
from config import Config
from flask_pymongo import PyMongo, MongoClient
from flask_bcrypt import Bcrypt

# initiates an instance of the flask and assigns it to app
app = Flask(__name__) 
app.config.from_object(Config)
bcrypt = Bcrypt(app)

# Passes the MongoURI and assigns the correct collection to db to access it in routes.
client = MongoClient(Config.MONGO_URI)
db = client.hfc_stats

# has to be imported after the instance on the flask app has been created.
from app import routes
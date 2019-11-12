from flask import Flask
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

from app import routes # has to be imported after the instace on the flask app has been created.
# app/__init__.py

from flask import Flask

# Initialize the app
app = Flask(__name__)

# Load the views
from app import views
# Define your view functions here
from flask import render_template

def home():
    return render_template('home.html')
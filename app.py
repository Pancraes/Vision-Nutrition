from flask import Flask, render_template, request, Response, flash, redirect, url_for
from cassiopeia import Summoner
import os

# AWS does not like the application named "app", mini workaround
application = Flask(__name__, static_folder="assets")
app = application

# Default to defaultkey if no env variable 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "defaultkey")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/presets")
def presets():
    return render_template("presets.html")

from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from passlib.hash import sha256_crypt
from app import app,db
#from .forms import RegistrationForm

import json
#from .models import User, Product, Category, Bill
#from .mongo_models import Post, Comment
import datetime

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    return render_template("index.html")

@app.route('/login/', methods=["GET", "POST"])
def login_page():
    return render_template("index.html")

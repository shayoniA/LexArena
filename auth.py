from flask import Blueprint, request, redirect, render_template, session, url_for
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from db import users_collection
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users_collection.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            session['username'] = username
            return redirect(url_for('quiz.home'))
        return "Invalid credentials."
    return render_template('login.html')

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form['password'])
        if users_collection.find_one({"username": username}):
            return "User already exists."
        users_collection.insert_one({
            "username": username,
            "password": password,
            "score": 0,
            "level": 1,
            "history": []
        })
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

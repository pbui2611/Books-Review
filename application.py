import os
import requests
import json

from flask import Flask, session, render_template, request, redirect, jsonify, abort, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
	# Bring users to "About Us" page if they do not sign up. Or Go to "Home" page otherwise
	if request.method == "POST":
		if 't_Name_User' in session:
			return render_template("search.html")
	else render_template("about-us.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
	errorMessage = ""
	if 't_Name_User' in session
		return redirect(url_for('index'))
	if request.method == "POST":
		t_Name_User = request.form.get("t_Name_User")
		t_Password = request.form.get("t_Password")
		if db.execute("SELECT * FROM users WHERE t_name_user = :t_Name_User AND t_password = :t_Password,"
			{"t_name_user": t_Name_User, "t_password": t_Password}).rowcount == 1:
			#if username and password are correct, store that username into session
			session["t_Name_User"] = t_Name_User
			return redirect(url_for('index'))
		else:
			errorMessage = "Incorrect username or password"
	return render_template("login-register.html", errorMessage = errorMessage)

@app.route("/register", methods = ["GET", "POST"])
def register():
	#Let user register for an account and store it into the database
	errorMessage = ""
	if request.method == "POST":
		t_Name_User = request.form.get("t_Name_User")
		t_Password = request.form.get("t_Password")
		t_Email = request.form.get("t_Email")
		if t_Name_User == "" or t_Password == "" or t_Email =="":
			errorMessage = "Please fill in all text fields"
		else:
			try:
				db.execute("INSERT INTO users(t_name_user, t_password, t_email) VALUES (:t_Name_User, :t_Password, :t_Email)",
					{"t_name_user": t_Name_User, "t_password": t_Password, "t_email": t_Email})
				db.commit()
				session_start()
				session["t_Name_User"] = t_Name_User
				return redirect(url_for('index'))
			except exc.IntegrityError:
				db.rollback()
				errorMessage = "Username is already taken"
	return render_template("login-register.html", errorMessage=errorMessage)


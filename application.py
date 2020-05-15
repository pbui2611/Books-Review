import os
import json
import requests

from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, session, render_template, request, redirect, jsonify, abort, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
#DATABASE_URL = "postgres://novtgbsngkfotl:fad0f06df0c477ce9ced03f184da766ad2b4b09798c4fe5a1852d7110fb59a4c@ec2-52-87-58-157.compute-1.amazonaws.com:5432/de6evg3luksu9s"
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
	if session.get("logged_in"):
		return render_template("search.html")
	else: 
		return render_template('about-us.html')

@app.route("/aboutus")
def aboutus():
	return render_template('about-us.html')

@app.route("/login", methods = ["GET", "POST"])
def login():
	if session.get("logged_in"):
		return redirect(url_for('index'))
	if request.method == "POST":
		t_Email = request.form.get("t_Email")
		t_Password = request.form.get("t_Password")
			#if username and password are correct, store that username into session
		user = db.execute("SELECT * FROM users WHERE t_email = :t_email", {"t_email": t_Email}).fetchone()
		if user == None or not check_password_hash(user[2], t_Password):
			flash("*Incorrect username or password*")
			return redirect(url_for('login'))
		else:	
			session["logged_in"] = True
			session["t_Name_User"] = user.t_name_user
			session["user_id"] = user.user_id
			return redirect(url_for('index'))
	return render_template("login-register.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
	#Let user register for an account and store it into the database
	if session.get("logged_in"):
		return redirect(url_for('index'))
	if request.method == "POST":
		t_Name_User = request.form.get("t_Name_User")
		t_Password = request.form.get("t_Password")
		t_Email = request.form.get("t_Email")
		if t_Name_User == "" or t_Password == "" or t_Email =="":
			flash("Please fill in all text fields")
			return redirect(url_for('register'), "303")
		if (db.execute("SELECT t_email FROM users WHERE t_email = :t_email",{"t_email": t_Email}).rowcount > 0):
			flash("*This email is already taken*")
			return redirect(url_for('register'))
		else:
			try:
				hashedPassword = generate_password_hash(t_Password, method="pbkdf2:sha256", salt_length=8)
				db.execute("INSERT INTO users(t_name_user, t_password, t_email) VALUES (:t_name_user, :t_password, :t_email)",
					{"t_name_user": t_Name_User, "t_password": hashedPassword, "t_email": t_Email})
				db.commit()
				user = db.execute("SELECT * FROM users WHERE t_name_user = :t_name_user AND t_password = :t_password", {"t_name_user": t_Name_User, "t_password": hashedPassword}).fetchone()
				session["logged_in"] = True
				session["t_Name_User"] = t_Name_User
				session["user_id"] = user.user_id
				return redirect(url_for('index'))
			except exc.IntegrityError:
				db.rollback()
				flash("This account is already existed")
				return redirect(url_for('register'), "303")
	return render_template("login-register.html")

@app.route('/logout')
def logout():
	session["logged_in"] = False
	session["t_Name_User"] = None
	session["user_id"] = None
	session.clear()
	flash("You've logged out successfully")
	return redirect("/")

@app.route('/search', methods = ["GET", "POST"])
def search():
	if request.method == "GET":
		if session.get("logged_in"):
			return render_template('search.html')
		else:
			return render_template("about-us.html")
	if request.method == "POST":
		isbn = request.form['t_search_isbn']
		title = request.form['t_search_title']
		author = request.form['t_search_author']
		if isbn == "" and title == "" and author =="":
			flash("Please fill at least one text fields")
			return redirect(url_for('search'), "303")
		else:
			if isbn == "" and title != "" and author != "":
				books = db.execute("SELECT * FROM books WHERE (t_title LIKE :title) AND (t_author LIKE :author)",{"title": "%" + title + "%", "author": "%" + author + "%"}).fetchall()
				return render_template('books.html', books = books)
			if isbn == "" and title == "" and author != "":
				books = db.execute("SELECT * FROM books WHERE (t_author LIKE :author)",{"author": "%" + author + "%"}).fetchall()
				return render_template('books.html', books = books)
			if isbn == "" and author == "" and title != "":
				books = db.execute("SELECT * FROM books WHERE (t_title LIKE :title)",{"title": "%" + title + "%"}).fetchall()
				return render_template('books.html', books = books)
			if title == "" and isbn != "" and author != "":
				books = db.execute("SELECT * FROM books WHERE (t_isbn LIKE :isbn) AND (t_author LIKE :author)",{"isbn": "%" + isbn + "%", "author": "%" + author + "%"}).fetchall()
				return render_template('books.html', books = books)
			if title == "" and author == "" and isbn != "":
				books = db.execute("SELECT * FROM books WHERE (t_isbn LIKE :isbn)",{"isbn": "%" + isbn + "%"}).fetchall()
				return render_template('books.html', books = books)
			if author == "" and title != "" and isbn != "":
				books = db.execute("SELECT * FROM books WHERE (t_isbn LIKE :isbn) AND (t_title LIKE :title)",{"isbn": "%" + isbn + "%", "title": "%" + title + "%"}).fetchall()
				return render_template('books.html', books = books)
			else:
				books = db.execute("SELECT * FROM books WHERE (t_isbn LIKE :isbn) AND (t_title LIKE :title) AND (t_author LIKE :author)",{"isbn": "%" + isbn + "%", "title": "%" + title + "%", "author": "%" + author + "%"}).fetchall()
				return render_template('books.html', books = books)

@app.route("/book/<int:book_id>")
def book(book_id):
	if not session.get("logged_in"):
		flash("You are not logged in")
		return render_template("about-us.html")
	else:
		user_id = session.get('user_id')
		book = db.execute("SELECT * FROM books WHERE book_id = :id", {"id": book_id}).fetchone()
		if book is None:
			return render_template("error.html")
		goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "pUEQGCOAskn1WDtta6liTQ", "isbns": book[1]})
		if goodreads.status_code != 200:
			return render_template("error.html")
		else:
			book_all = goodreads.json()
			book_rating = book_all['books'][0]['average_rating']
			reviews = db.execute("SELECT * FROM reviews LEFT JOIN users ON reviews.user_id = users.user_id WHERE book_id = :id",{"id": book_id}).fetchall()
			if (db.execute("SELECT * FROM reviews LEFT JOIN users ON (reviews.user_id = users.user_id) WHERE (book_id = :id) AND (reviews.user_id = :user_id)", {"id": book_id, "user_id": user_id},).rowcount > 0):
				allow_to_rate = False
			else:
					allow_to_rate = True
			return render_template("book.html", book = book, book_rating = book_rating, reviews = reviews, allow_to_rate = allow_to_rate)

@app.route("/review/<int:book_id>", methods = ["POST"])
def review(book_id):
	if not session.get("logged_in"):
		flash("You are not logged in")
		return render_template("about-us.html")
	else:
		username = session.get("t_Name_User")
		user_id = session.get("user_id")
		if (db.execute("SELECT * FROM reviews LEFT JOIN users ON (reviews.user_id = users.user_id) WHERE (book_id = :id) AND (reviews.user_id = :user_id)", {"id": book_id, "user_id": user_id},).rowcount > 0):
				allow_to_rate = False
				flash("You already gave a review for this book")
				return redirect(url_for('book', book_id = book_id), "303")
		else:
			allow_to_rate = True
			review = request.form.get("review")
			book_rating = request.form.get("book_rating")
			db.execute("INSERT INTO reviews (book_id, user_id, book_rating, review) VALUES (:book_id, :user_id, :book_rating, :review)",{"book_id": book_id,"user_id": user_id, "book_rating": book_rating, "review": review})
			db.commit()
			return redirect(url_for('book', book_id = book_id), "303")

@app.route("/api/<isbn_id>")
def api(isbn_id):
	book_api = db.execute("SELECT * FROM books WHERE t_isbn = :isbn",{"isbn": isbn_id}).fetchone()
	if book_api is None:
			return render_template("error.html")
	else:
		book_reviews = db.execute("SELECT COUNT(review_id), AVG(book_rating) FROM reviews WHERE book_id = :book_id",{"book_id": book_api.book_id}).fetchone()
	result = {
		"title":book_api.t_title,
		"author": book_api.t_author,
		"year": book_api.t_year,
		"isbn": book_api.t_isbn,}
	try:
		result["review_count"] = str(book_reviews[0])
		result["average_score"] = "% 1.1f" % book_reviews[1]
	except TypeError: 
		result["review_count"] = "No Reviews"
		result["average_score"] = "No Reviews"
	#json_result = json.dumps(result)
	return jsonify(result), 200

if __name__ == 'main':
	app.run()
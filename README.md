# Project 1: bookrates Website Project

Web Programming with Python and JavaScript

Description: This is a basic project in which I applied what I have learned in CS50's Web Programming with Python and JavaScript class offered by edX. This project's goal is to build a book review website. Users will be able to register for your website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. We will also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via your website’s API.

Requirements:
  Registration: Users should be able to register for your website, providing (at minimum) a username and password.
  Login: Users, once registered, should be able to log in to your website with their username and password.
  Logout: Logged in users should be able to log out of the site.
  Import: Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called import.py separate from your web application, write a program that will take the books and import them into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python3 import.py to import the books into your database, and submit this program with the rest of your project code.
  Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
  Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
  Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
  Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
  API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score.

How to run my Project on Windows:
    $env:FLASK_APP = "application"
    $env:FLASK_DEBUG = "1"
    $env:DATABASE_URL="postgres://novtgbsngkfotl:fad0f06df0c477ce9ced03f184da766ad2b4b09798c4fe5a1852d7110fb59a4c@ec2-52-87-58-157.compute-1.amazonaws.com:5432/de6evg3luksu9s"
    python -m flask run

Note: I also posted .sql files here for you to have better understanding about what table and its elements I use.
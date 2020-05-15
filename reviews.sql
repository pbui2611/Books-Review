CREATE TABLE reviews (
	review_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	book_id INTEGER REFERENCES books,
  book_rating INTEGER NOT NULL,
	review VARCHAR NOT NULL,
	t_name_user VARCHAR NOT NULL
);
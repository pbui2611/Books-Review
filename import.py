import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for t_isbn, t_title, t_author, t_year in reader:
        db.execute("INSERT INTO books (t_isbn, t_title, t_author, t_year) VALUES (:t_isbn, :t_title, :t_author, :t_year)",
            {"t_isbn": t_isbn, "t_title": t_title, "t_author": t_author, "t_year": t_year})
db.commit()

if __name__ == "__main__":
    main()
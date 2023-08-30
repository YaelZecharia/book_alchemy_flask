from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
import os

app = Flask(__name__)
app.secret_key = 'fjhsj84jsvk472nnks83'

# Get the absolute path of the directory where app.py is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Use this base directory to define an absolute path for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'data', 'library.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# This will connect the Flask app to the flask-sqlalchemy code
db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Endpoint to add an author. If accessed via GET, displays the form to add an author.
    If accessed via POST, saves the new author to the database.
    """
    if request.method == 'POST':
        # Extract data from the form
        name = request.form.get('name')
        birthdate = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')

        # Create a new author instance and add to the database
        new_author = Author(name=name, birth_date=birthdate, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        # Flash a success message
        flash("Author added successfully!", "success")
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Endpoint to add a book. If accessed via GET, displays the form to add a book.
    If accessed via POST, saves the new book to the database.
    """
    if request.method == 'POST':
        # Extract data from the form
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        # Create a new book instance and add to the database
        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()

        # Flash a success message
        flash("Book added successfully!", "success")
        return redirect(url_for('add_book'))

    # Get all authors from the database for the dropdown
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/')
def home():
    """
    Homepage route that displays all the books. Optionally, it can display the books 
    filtered based on a search query.
    """
    # Extract data from the form
    search_query = request.args.get('search_query')

    if search_query:
        books = Book.query.filter(Book.title.like(f"%{search_query}%")).all()
        if not books:
            flash(f"No books found for query '{search_query}'", "warning")
    else:
        books = Book.query.all()

    return render_template('home.html', books=books)


@app.route('/sort_books', methods=['POST'])
def sort_books():
    """
    Route to sort and display books based on the user's preference.
    The books can be sorted by their title or the author's name.
    """
    # Extract data from the form
    sort_by = request.form.get('sort_by')

    if sort_by == "title":
        books = Book.query.order_by(Book.title.asc()).all()
    elif sort_by == "author_name":
        books = Book.query.join(Author).order_by(Author.name.asc(), Book.title.asc()).all()
    else:
        books = Book.query.all()

    return render_template('home.html', books=books)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Endpoint to delete a specific book from the database based on its ID.
    """
    book = Book.query.get(book_id)
    if not book:
        # Handle a not found scenario. 
        flash('Book not found', 'error')
        return redirect(url_for('home'))

    db.session.delete(book)
    db.session.commit()
    flash(f"'{book.title}' has been deleted!", 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)

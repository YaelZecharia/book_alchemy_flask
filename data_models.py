from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(10), nullable=True)  # e.g., 'YYYY-MM-DD'
    date_of_death = db.Column(db.String(10), nullable=True)  # e.g., 'YYYY-MM-DD'

    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}', birth_date='{self.birth_date}', date_of_death='{self.date_of_death}')"

    def __str__(self):
        return f"Author {self.name} (Born: {self.birth_date}, Died: {self.date_of_death})"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f"Book(id={self.id}, isbn='{self.isbn}', title='{self.title}', publication_year={self.publication_year}, author_id={self.author_id})"

    def __str__(self):
        return f"Book '{self.title}' (ISBN: {self.isbn}, Published: {self.publication_year})"

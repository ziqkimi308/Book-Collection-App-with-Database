from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize sqlalchemy extension
db = SQLAlchemy(app)

# Define the table model
class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(250), unique=True, nullable=False)
	author = db.Column(db.String(250), nullable=False)
	rating = db.Column(db.Float, nullable=False)

# Create table
with app.app_context():
	db.create_all()

@app.route('/')
def home():
	all_books = db.session.query(Book).all()
	return render_template('index.html', books=all_books)

@app.route("/add", methods=["GET", "POST"])
def add():
	if request.method == "POST":
		# Update the table and changes in database
		new_book = Book(
			title = request.form["title"],
			author = request.form["author"],
			rating = request.form["rating"]
		)
		db.session.add(new_book)
		db.session.commit()
		
		# Return home after finish
		return redirect(url_for('home'))
    
	return render_template('add.html')

@app.route("/edit", methods=["GET", "POST"])
def edit():
	if request.method == "POST":
		# Update record
		book_to_update = Book.query.get(request.form["id"])
		book_to_update.rating = request.form["rating"]
		db.session.commit()
		return redirect(url_for('home'))
	
	book_selected = Book.query.get(request.args.get('id'))
	return render_template('edit_rating.html', book=book_selected)

@app.route("/delete")
def delete():
	# Delete a record
	book_to_delete = Book.query.get(request.args.get('id'))
	db.session.delete(book_to_delete)
	db.session.commit()
	return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)


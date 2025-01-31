from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Contact {self.name}>'

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')  # Your HTML file

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # Create a new contact instance
        new_contact = Contact(name=name, email=email, phone=phone, message=message)

        # Add to the database
        db.session.add(new_contact)
        db.session.commit()

        return redirect(url_for('index'))  # Redirect to the index page after submission

if __name__ == '__main__':
    app.run(debug=True)

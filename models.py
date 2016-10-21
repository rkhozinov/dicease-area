from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120), unique=True)
    coordinates = db.Column(db.String(120), unique=True, nullable=True)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    district = db.relationship('District',
            backref=db.backref('hospitals',lazy='dynamic'))

    def __init__(self, name, address, district, coordinates=None):
        self.name = name
        self.address = address
        self.district = district
        self.coordinates = coordinates

    def __repr__(self):
        return self.name

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    coordinates = db.Column(db.String(120), unique=True, nullable=True)

    def __init__(self, name, coordinates=None):
        self.name = name
        self.coordinates = coordinates

    def __repr__(self):
        return self.name

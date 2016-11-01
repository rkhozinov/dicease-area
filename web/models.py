# models.py
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

from app import db


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    coordinates = db.Column(db.String(120), nullable=True)

    def __init__(self, name, coordinates=None):
        self.name = name
        self.coordinates = coordinates

    def __repr__(self):
        return self.name


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    coordinates = db.Column(db.String(120), nullable=True)

    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    district = db.relationship('District',
                               backref=db.backref('hospitals', lazy='dynamic', uselist=True))

    def __init__(self, name, district, address=None, phone=None, coordinates=None):
        self.name = name
        self.district = district
        self.address = address
        self.phone = phone
        self.coordinates = coordinates

    def __repr__(self):
        return self.name


class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description


class DiseasePopulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    year = db.Column(db.Integer, nullable=True)
    children = db.Column(db.Integer, nullable=True)
    children_observed = db.Column(db.Integer, nullable=True)
    adults = db.Column(db.Integer, nullable=True)
    adults_observed = db.Column(db.Integer, nullable=True)

    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    hospital = db.relationship('Hospital',
                                backref=db.backref('population', lazy='dynamic',
                                                   uselist=True))

    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'))
    disease = db.relationship('Disease',
                              backref=db.backref('population', lazy='dynamic', uselist=True))



    def __init__(self, disease, hospital, year, adults=0, adults_observed=0,
                 children=0, children_observed=0):
        self.disease = disease
        self.hospital = hospital
        self.year = int(year) if year else 0
        self.children = int(children)
        self.children_observed = int(children_observed)
        self.adults = int(adults)
        self.adults_observed = int(adults_observed)
        self.all = self.children + self.adults
        self.all_observed = self.children_observed + self.adults_observed

    def __repr__(self):
        return '{0}{1}'.format(self.name, self.year)



class Population(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    all = db.Column(db.Integer)
    men = db.Column(db.Integer)
    women = db.Column(db.Integer)
    children = db.Column(db.Integer)
    adults = db.Column(db.Integer)
    employable = db.Column(db.Integer)
    employable_men = db.Column(db.Integer)
    employable_women = db.Column(db.Integer)

    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    district = db.relationship('District',
                               backref=db.backref('population', lazy='dynamic', uselist=True))

    def __init__(self, year, district,
                 men=0, women=0, children=0, employable_men=0, employable_women=0, district_id=0):
        self.district = district
        self.year = int(year)
        self.men = int(men)
        self.women = int(women)
        self.children = int(children)
        self.employable_men = int(employable_men)
        self.employable_women = int(employable_women)

        self.all = self.men + self.women
        self.adults = self.all - self.children
        self.employable = self.employable_men + self.employable_women

    def __repr__(self):
        return '{}:{}'.format(self.year, self.all)

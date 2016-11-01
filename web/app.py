from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))

import logging

from config import Config
from flask import Flask
from flask import request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from googlemaps import client

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
db.init_app(app)

from models import *

with app.test_request_context():
    db.create_all()

gmaps = client.Client(key=Config.GOOGLE_MAPS_KEY)

console = logging.StreamHandler()
log = logging.getLogger("app")
log.addHandler(console)
log.setLevel(logging.DEBUG)

navigation = ['district', 'population', 'hospital', 'disease',
              'disease population']


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', navigation=navigation)


@app.route('/district', methods=['GET', 'POST'])
def district():
    if request.method == 'POST':
        log.debug(request.form)
        name = request.form.get('name')

        # TODO: update coordinates for district
        district = District.query.filter_by(name=name).first()
        if name and not district:
            db.session.add(District(name=name, coordinates=_get_coordignates(name)))
            db.session.commit()
        return redirect(url_for('district'))

    return render_template('district.html', districts=_get_all_districts(),
                           navigation=navigation)


@app.route('/district/delete', methods=['POST'])
def district_delete():
    if request.method == 'POST':
        district_id = int(request.form.get('district_id'))
        log.debug(request.form)
        district = District.query.filter_by(id=district_id).first()

        log.debug(district)

        if district and not district.hospitals.count() \
                and not district.population.count():
            db.session.delete(district)
            db.session.commit()

    return redirect(url_for('district'))


@app.route('/disease', methods=['GET', 'POST'])
def disease():
    if request.method == 'POST':
        log.debug(request.form)
        name = request.form.get('name')
        if name:
            db.session.add(Disease(name=name))
            db.session.commit()
    return render_template('disease.html', diseases=_get_all_diseases(),
                           navigation=navigation)


@app.route('/disease/delete', methods=['POST'])
def disease_delete():
    if request.method == 'POST':
        disease_id = int(request.form.get('disease_id'))
        log.debug(request.form)
        disease = Disease.query.filter_by(id=disease_id).first()

        if disease and not disease.population.count():
            db.session.delete(disease)
            db.session.commit()

    return redirect(url_for('disease'))


@app.route('/hospital', methods=['GET', 'POST'])
def hospital():
    if request.method == 'POST':
        log.debug(request.form)
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        district_id = request.form.get('district_id')

        district = District.query.filter_by(id=district_id).first() \
            if district_id else None

        if name and district:
            db.session.add(Hospital(name=name, address=address, phone=phone,
                                    coordinates=_get_coordignates(name), district=district))
            db.session.commit()

    return render_template('hospital.html', hospitals=_get_all_hospitals(),
                           districts=_get_all_districts(),
                           navigation=navigation)


@app.route('/hospital/delete', methods=['POST'])
def hospital_delete():
    if request.method == 'POST':
        hospital_id = int(request.form.get('hospital_id'))
        log.debug(request.form)
        hospital = Hospital.query.filter_by(id=hospital_id).first()

        if hospital and not hospital.population.count():
            db.session.delete(hospital)
            db.session.commit()

    return redirect(url_for('hospital'))


@app.route('/population', methods=['GET', 'POST'])
def population():
    if request.method == 'POST':
        log.debug(request.form)
        year = request.form.get('year')
        men = request.form.get('men')
        women = request.form.get('women')
        children = request.form.get('children')
        employable_men = request.form.get('employable_men')
        employable_women = request.form.get('employable_women')
        district_id = request.form.get('district_id')
        district = _get_district_by_id(district_id)
        if year and district:
            db.session.add(Population(district=district,
                                      year=year,
                                      men=men,
                                      women=women,
                                      children=children,
                                      employable_men=employable_men,
                                      employable_women=employable_women
                                      )
                           )
            db.session.commit()

    return render_template('population.html', populations=_get_all_population(),
                           districts=_get_all_districts(),
                           navigation=navigation)


@app.route('/population/delete', methods=['POST'])
def population_delete():
    if request.method == 'POST':
        population_id = int(request.form.get('population_id'))
        log.debug(request.form)
        population = Population.query.filter_by(id=population_id).first()
        if population:
            db.session.delete(population)
            db.session.commit()

    return redirect(url_for('population'))


@app.route('/disease_population', methods=['GET', 'POST'])
def disease_population():
    if request.method == 'POST':
        log.debug(request.form)

        year = request.form.get('year')
        children = request.form.get('children')
        children_observed = request.form.get('children_observed')
        adults = request.form.get('adults')
        adults_observed = request.form.get('adults_observed')
        hospital_id = request.form.get('hospital_id')
        disease_id = request.form.get('disease_id')

        disease = _get_disease_by_id(disease_id)
        hospital = _get_hospital_by_id(hospital_id)

        if year and disease and hospital:
            db.session.add(DiseasePopulation(year=year,
                                             children=children,
                                             children_observed=children_observed,
                                             adults=adults,
                                             adults_observed=adults_observed,
                                             hospital=hospital,
                                             disease=disease,
                                             )
                           )
            db.session.commit()

    return render_template('disease_population.html',
                           disease_populations=_get_all_disease_population(),
                           diseases=_get_all_diseases(),
                           hospitals=_get_all_hospitals(),
                           navigation=navigation)


@app.route('/disease_population/delete', methods=['POST'])
def disease_population_delete():
    if request.method == 'POST':
        log.debug(request.form)
        disease_population_id = request.form.get('disease_population_id')
        disease_population = DiseasePopulation.query.filter_by(
            id=disease_population_id).first()
        if disease_population:
            db.session.delete(disease_population)
            db.session.commit()

    return redirect(url_for('disease_population'))


def _get_all_population():
    return Population.query.order_by(Population.year).all()


def _get_all_districts():
    return District.query.order_by(District.name).all()


def _get_all_hospitals():
    return Hospital.query.order_by(Hospital.name).all()


def _get_all_diseases():
    return Disease.query.order_by(Disease.name).all()


def _get_all_disease_population():
    return DiseasePopulation.query.order_by(DiseasePopulation.year).all()


def _get_district_by_id(district_id):
    return District.query.filter_by(
        id=district_id).first() if district_id else None


def _get_disease_by_id(disease_id):
    return Disease.query.filter_by(
        id=disease_id).first() if disease_id else None


def _get_hospital_by_id(hospital_id):
    return Hospital.query.filter_by(
        id=hospital_id).first() if hospital_id else None


def _get_coordignates(name):
    geodata = gmaps.geocode(address=name, language='RU')
    return str(geodata[0]) if len(geodata) > 0 else None


if __name__ == '__main__':
    app.run()

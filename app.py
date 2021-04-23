from config import password
from flask import jsonify, Flask, render_template
import sqlalchemy
from sqlalchemy import create_engine, inspect, func
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, query


engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/Meteorite_Landings')
conn = engine.connect()
 
 # reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Landings = Base.classes.landings


app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    session = Session(engine)
    results = pd.read_sql("Select * from landings",conn)
    session.close()
    print(results.head().to_json(orient="records"))
    
    return render_template("index.html")

@app.route("/map")
def map():
    session = Session(engine)
    meteoritedata = session.query(Landings.name,Landings.mass,Landings.latitude,Landings.longitude).all()
    session.close()
    print(meteoritedata)
    return render_template("map.html", meteoritedata=meteoritedata)


# @app.route("/name")
# def name():
    
#     """Retreive Meteorite Landings Data"""
#     session = Session(engine)

#     """Return a list of name"""
#     # Query for the dates and precipitation from last year
#     name = session.query(Landings.name).all()
#     session.close()
#     return jsonify(name)

@app.route("/meteoritedata")
def meteoritedata():
    
    """Retreive Meteorite Landings Data"""
    session = Session(engine)

    """Return a list of name"""
    # Query for the dates and precipitation from last year
    meteoritedata = session.query(Landings.name,Landings.mass,Landings.latitude,Landings.longitude).all()
    session.close()
    return jsonify(meteoritedata)


# @app.route("/latitude")
# def latitude():
    
#     """Retreive Meteorite Landings Data"""
#     session = Session(engine)

#     """Return a list of latitude"""
#     # Query for the dates and precipitation from last year
#     latitude = session.query(Landings.latitude).all()
#     session.close()
#     return jsonify(latitude)


# @app.route("/longitude")
# def longitude():
    
#     """Retreive Meteorite Landings Data"""
#     session = Session(engine)

#     """Return a list of longitude"""
#     # Query for the dates and precipitation from last year
#     longitude = session.query(Landings.longitude).all()
#     session.close()
#     return jsonify(longitude)


# @app.route("/mass")
# def mass():
    
#     """Retreive Meteorite Landings Data"""
#     session = Session(engine)

#     """Return a list of mass"""
#     # Query for the dates and precipitation from last year
#     mass = session.query(Landings.mass).all()
#     session.close()
#     return jsonify(mass)


    
if __name__ == '__main__':
        app.run()
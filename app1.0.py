import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Conect to the data base (conection)
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the data base (objects)
Base = automap_base()
Base.prepare(engine, reflect=True)

# Variables object from DB
Measurement = Base.classes.measurement
Station = Base.classes.station

# Session create (query)
session = Session(engine)

# This the new Flask app instance
app = Flask(__name__)

# Flask routes... 
@app.route("/")
def welcome():
    return(
    '''
    <h1>Welcome to the Climate Analysis API!</h1>
    </br>
    <h4>Available Routes:</h4>
    </br>
    <div>
        <li>
            <a href="http://127.0.0.1:5000/api/v1.0/precipitation">/api/v1.0/precipitation</a>
        </li>
        <li>
             <a href="http://127.0.0.1:5000/api/v1.0/stations">/api/v1.0/stations</a>
        </li>
        <li>
             <a href="http://127.0.0.1:5000/api/v1.0/tobs">/api/v1.0/tobs</a>
        </li>
        <li>
             <a href="http://127.0.0.1:5000/api/v1.0/temp/start/end">/api/v1.0/temp/start/end</a>
        </li>
    </div>
    ''')

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)        

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
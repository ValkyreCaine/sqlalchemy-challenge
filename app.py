# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base= automap_base()
# reflect the tables
Base.prepare(autoload_with= engine)


# Save references to each table
station= Base.classes.station
measurement=Base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app= Flask(__name__)



#################################################
# Flask Routes
#################################################
#Home Page
@app.route("/")

def Welcome():
    
    return(
        f"Congratulations for taking this step to treat yourself to this vacation!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Last 12 Months of Precipitation Data<br/>"
        f"/api/v1.0/stations - List of Stations<br/>"
        f"/api/v1.0/tobs - Temperature observations of the most-active station from the previous year.<br/>"
        f"/api/v1.0/<start> - Temperature observations from the start date<br/>"
        f"/api/v1.0/<start>/<end> - Temperature observations from the start date to the end date<br/>"
    )

#Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    the_latest= session.query(func.max(measurement.date)).scalar()
    one_year_ago= dt.datetime.strptime(the_latest, "%Y-%m-%d") - dt.timedelta(days=365)

    result=session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all()

    precipi___tation_dict={date: prcp for date, prcp in result}
    return jsonify(precipi___tation_dict)

#Crustation Station
@app.route("/api/v1.0/stations")
def stations():
    result = session.query(station.station).all()
    hook_and_ladder = [station[0] for station in result]
    return jsonify(hook_and_ladder)

#TOBiaS
@app.route("/api/v1.0/tobs")
def tobs():
    hook_and_ladder=session.query(measurement.station, func.count(measurement.station))\
        .group_by(measurement.station)\
        .order_by(func.count(measurement.station).desc())\
        .first()[0]

    the_latest= session.query(func.max(measurement.date)).scalar()
    the_latest= dt.datetime.strptime(the_latest, "%Y-%m-%d")
    one_year_ago= the_latest - dt.timedelta(days=365)

    result=session.query(measurement.date, measurement.tobs)\
        .filter(measurement.station == hook_and_ladder)\
        .filter(measurement.date >= one_year_ago.strftime("%Y-%m-%d"))\
        .all()
    
    temps=[]
    for date, tobs in result:
        temps.append({"date": date, "tobs": tobs})
    return jsonify(temps)

#It's /starting to/ gettin hot in here
@app.route("/api/v1.0/<start>")
def tobs_start_date(start):
    try:
        starter= dt.datetime.strptime(start, '%Y-%m-%d')

        result= session.query(
            func.min(measurement.tobs),
            func.max(measurement.tobs),
            func.avg(measurement.tobs)
        ).filter(measurement.date >= starter).all()

        result_dict={
            "TMIN": result[0][0],
            "TAVG": result[0][2],
            "TMAX": result[0][1]
        }
        return jsonify(result_dict)
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400


#The beginning of the end
@app.route("/api/v1.0/<start>/<end>")
def start_to_finish(start, end):
    starter=dt.datetime.strptime(start, '%Y-%m-%d')
    finisher=dt.datetime.strptime(end, '%Y-%m-%d')
    result= session.query(
    func.min(measurement.tobs),
    func.max(measurement.tobs),
    func.avg(measurement.tobs))\
    .filter(measurement.date >= starter)\
    .filter(measurement.date <= finisher).all()
    
    result_dict={
        "TMIN": result[0][0],
        "TAVG": result[0][2],
        "TMAX": result[0][1]
    }
    return jsonify(result_dict)
if __name__=="__main__":
    app.run(debug=True)
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import os
import sqlite3

# conn = sqlite3.connect("Resources/hawaii.sqlite")
# print("Connected successfully!")
# conn.close()
print("osPAth",os.path.exists("Resources/hawaii.sqlite"))
print("hi")

# Get the absolute path of the database file
db_path = os.path.abspath("Resources/hawaii.sqlite")
print("dbpath",db_path)

# Create the engine with the absolute path
engine = create_engine(f"sqlite:///{db_path}")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

@app.route("/")
def homepage():
    """List all available API routes."""
    return (
        f"<h1>Welcome to the Climate API</h1>"
        f"<h2>Available Routes:</h2>"
        f"<ul>"
        f"<li><a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a> - Precipitation data for the last year</li>"
        f"<li><a href='/api/v1.0/stations'>/api/v1.0/stations</a> - List of weather stations</li>"
        f"<li><a href='/api/v1.0/tobs'>/api/v1.0/tobs</a> - Temperature observations for the most active station in the last year</li>"
        f"<li>/api/v1.0/&lt;start&gt; - Min, Avg, and Max temperatures from a start date</li>"
        f"<li>/api/v1.0/&lt;start&gt;/&lt;end&gt; - Min, Avg, and Max temperatures for a date range</li>"
        f"</ul>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Start a session to query the database
    session = Session(engine)

    # Calculate the date 12 months ago from the most recent date in the dataset
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= one_year_ago
    ).all()

    # Close the session
    session.close()

    # Convert the query results into a dictionary with date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create a new session
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    # Close the session after querying
    session.close()

    # Convert list of tuples into a flat list
    station_list = [station[0] for station in results]

    # Return JSON response
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a session
    session = Session(engine)

    # Step 1: Identify the most-active station (the station with the highest number of observations)
    most_active_station = (
        session.query(Station.station)
        .join(Measurement, Station.station == Measurement.station)
        .group_by(Station.station)
        .order_by(func.count(Measurement.station).desc())
        .first()
    )[0]

    # Step 2: Find the last date in the dataset
    last_date = session.query(func.max(Measurement.date)).scalar()

    # Step 3: Calculate the date one year ago from the last date
    one_year_ago = (dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)).date()

    # Step 4: Query the dates and temperature observations for the most-active station in the last year
    results = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.station == most_active_station)
        .filter(Measurement.date >= one_year_ago)
        .all()
    )

    # Close the session
    session.close()

    # Convert results into a list of dictionaries
    tobs_data = [{"date": result[0], "temperature": result[1]} for result in results]

    # Return JSON response
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    """Return TMIN, TAVG, and TMAX for a specified start or start-end range."""

    # Create a session
    session = Session(engine)

    try:
        # Query for temperature stats
        if end:
            # If both start and end dates are provided
            results = (
                session.query(
                    func.min(Measurement.tobs),
                    func.avg(Measurement.tobs),
                    func.max(Measurement.tobs)
                )
                .filter(Measurement.date >= start)
                .filter(Measurement.date <= end)
                .all()
            )
        else:
            # If only the start date is provided
            results = (
                session.query(
                    func.min(Measurement.tobs),
                    func.avg(Measurement.tobs),
                    func.max(Measurement.tobs)
                )
                .filter(Measurement.date >= start)
                .all()
            )

        # Extract TMIN, TAVG, and TMAX from the query results
        temps = {
            "start_date": start,
            "end_date": end if end else "Present",
            "TMIN": results[0][0],
            "TAVG": results[0][1],
            "TMAX": results[0][2]
        }

        # Return JSON response using jsonify
        return jsonify(temps)

    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({"error": str(e)}), 500

    finally:
        # Close the session
        session.close()


if __name__ == "__main__":
    app.run(debug=True)
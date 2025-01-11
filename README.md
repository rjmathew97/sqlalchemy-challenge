# Module 10 Challenge: SQL Alchemy

## **Overview**
This project involves perfoming a climate analysis on Honolulu, Hawaii, using historical weather data stored in a SQLite database. The goal is to uncover meaningful weather patterns and trends to aid in vacation planning. The project includes building a Flask API to expose these insights for user-friendly data access.

# Part 1: Analyze and Explore Climate Data
1. Connect to a SQLite Database using SQLAlchmey and perform precipitation analysis to uncover yearly trends.  
2. Analyze station activity to identify the most-active weather stations and visualize data using Matplotlib and Pandas

# Part 2: Design a Flask API
1. Create a API with routes to provide climate data insights
2. Include static and dynamic routes for querying precipitation, station activity, and temperature statistics. 


## **Technologies Used**
- SQLAlchemy and SQLite
- Python 
- Flask 
- Pandas and Matplotlib

sqlalchemy-challenge/
    SurfsUp/
│       Resources/                  # CSV files for data import
            hawaii.sqlite           # SQLite database file
│       climate_starter.ipynb       # Jupyter Notebook for data analysis
│       README.md                   # Project documentation (this file)
│       app.py                      # Flask API Application


## **Setup Instructions**
# Part 1: Analyze and Explore the Climate Data
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/sqlalchemy-challenge.git
   cd sqlalchemy-challenge

2. **Launch Jupyter Notebook:**
Open the climate_starter.ipynb file in the notebook interface.

3. **Database Connection:**
Connect to the database using SQLAlchemy and reflect the database schema using automap_base().

3. **Run Analysis:**
Perform precipitation and station analyses and performing visualization using Motplotlib plots

# Part 2: Design the Flask

1. **Verify Database File:**
Ensure hawii.sqlite is located in the Resources/ directory 

2. **Run the Flask Application:** 
python app.py

3. **Acess API Endpoints:** 
Navigate to the root endpoint (/) to view all available routes.
Use the following routes to query climate data:
/api/v1.0/precipitation: Last 12 months of precipitation data.
/api/v1.0/stations: List of all weather stations.
/api/v1.0/tobs: Temperature observations for the most-active station for the last year.
/api/v1.0/<start>: Min, avg, and max temperatures from a specified start date.
/api/v1.0/<start>/<end>: Min, avg, and max temperatures for a specified date range.

4. **Test the API:**
Navigate to : http://127.0.0.1:5000/api/v1.0/precipitation














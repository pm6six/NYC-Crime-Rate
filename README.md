# NYC Crime Rate by Precinct

This Project analyzes New York City crime data and visualizes which precincts have the 

# Download CSV and GeoJson Files
Go to https://opendata.cityofnewyork.us
Search "nypd complaints" on the search bar
Click "NYPD Complaint Data Historic"
Click "Data" on the top left
If mouse get close to "CMPLNT_FR_DT", it will show three bars on the right side. Click that bars.
Click Filter symbol and change equal to in range, and change the range from 2013 to 2018.
Click Export and download the CSV file.

In the same manner download the CSV file, ranging from 2022 to 2024.

Go back to https://opendata.cityofnewyork.us
Search "nypd complaints" on the search bar
Click "NYPD Complaint Data Current (Year To Date)"
Click Export and download the CSV file.

Go to https://data.cityofnewyork.us/City-Government/Police-Precincts/y76i-bdw7/about_data
Click Export and download the GeoJson file.

Store All three files into the Data folder

# Requirements
Download required libraries, which were written in requirements.txt by using the following command.
pip install -r requirements.txt

# How to create forecasting png files?
python main_forecasting.py
png files are created under output folder

# How to run heat map?
python main_maps.py
open the created HTML files.

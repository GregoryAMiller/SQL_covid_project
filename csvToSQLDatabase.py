import pandas as pd
import sqlite3

# Read in the CSV files
deaths_df = pd.read_csv('CovidDeaths.csv')
vaccinations_df = pd.read_csv('CovidVaccinations.csv')

# Create a connection to a new SQLite database
conn = sqlite3.connect('covid_data.db')

# Write the data to the SQLite database
deaths_df.to_sql('deaths', conn, if_exists='replace', index=False)
vaccinations_df.to_sql('vaccinations', conn, if_exists='replace', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()
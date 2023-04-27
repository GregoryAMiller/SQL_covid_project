import requests
import sqlite3
import pandas as pd
import openpyxl
# Create a connection to a new SQLite database file
conn = sqlite3.connect('covid_data.db')

# Create a cursor object
cur = conn.cursor()

sql_query = """
    SELECT SUM(new_cases) as total_cases, SUM(new_deaths) as total_deaths, SUM(new_deaths)/SUM(new_cases)*100 as DeathPercentage
    FROM deaths
    where continent is not null
    order by 1,2
"""
sql_query = """
    SELECT location, SUM(new_deaths) as TotalDeathCount
    FROM deaths
    where continent is null and location not in ('World', 'European Union', 'International', 'High income', 'Upper middle income', 'Lower middle income', 'Low income')
    Group by location
    order by TotalDeathCount DESC
"""
sql_query = """
    SELECT Location, population, MAX(total_cases) as HighestInfectionCount, MAX((total_cases/population))*100 as InfectedPercentage
    FROM deaths
    Group by Location, population
    order by InfectedPercentage DESC
"""
sql_query = """
    SELECT Location, population, date, MAX(total_cases) as HighestInfectionCount, MAX((total_cases/population))*100 as InfectedPercentage
    FROM deaths
    Group by Location, population, date
    order by InfectedPercentage DESC
"""
# Execute the SQL query and read the results into a pandas dataframe
df = pd.read_sql_query(sql_query, conn)

# Replace any missing column values with zero
df = df.fillna(0)

# Export the dataframe to an Excel file
df.to_excel('TableauTable4.xlsx', index=False)

# # Execute the SQL query
# cur.execute(sql_query)

# # Fetch the results and print them
# results = cur.fetchall()
# for row in results:
#     print(row)

# Commit the changes and close the connection
conn.commit()
conn.close()
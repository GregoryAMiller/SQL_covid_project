import requests
import sqlite3

# Create a connection to a new SQLite database file
conn = sqlite3.connect('covid_data.db')

# Create a cursor object
cur = conn.cursor()

# Define the SQL query
sql_query = """
    SELECT *
    FROM deaths
    LIMIT 100
"""
sql_query = """
    SELECT Location, date, total_cases, new_cases, total_deaths, population
    FROM deaths
    order by 1,2
    LIMIT 100
"""
''' Looking at total cases vs total deaths'''
''' Shows the likelihood of dying of covid in a given country '''
sql_query = """
    SELECT Location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
    FROM deaths
    Where location like '%states%'
    order by 1,2
    LIMIT 100
"""
''' looking at total cases vs population '''
''' Shows what percentage of population got covid in the united states '''
sql_query = """
    SELECT Location, date, total_cases, population, (total_cases/population)*100 as InfectedPercentage
    FROM deaths
    Where location like '%states%'
    order by date DESC
    LIMIT 100
"""
''' looking at countries with the highest indection rate compared to population '''
sql_query = """
    SELECT Location, population, MAX(total_cases) as HighestInfectionCount, MAX((total_cases/population))*100 as InfectedPercentage
    FROM deaths
    Group by Location, population
    order by InfectedPercentage DESC
    LIMIT 100
"""
''' showing countries with highest death count per population '''
sql_query = """
    SELECT Location, MAX(total_deaths) as TotalDeathCount
    FROM deaths
    where continent is not null
    Group by Location
    order by TotalDeathCount DESC
    LIMIT 10
"""
''' showing continents with highest death count per population '''
sql_query = """
    SELECT continent, MAX(total_deaths) as TotalDeathCount
    FROM deaths
    where continent is not null
    Group by continent
    order by TotalDeathCount DESC
    LIMIT 10
"""
sql_query = """
    SELECT Location, MAX(total_deaths) as TotalDeathCount
    FROM deaths
    where continent is null
    Group by Location
    order by TotalDeathCount DESC
    LIMIT 10
"""
sql_query = """
    SELECT continent, MAX(total_deaths) as TotalDeathCount
    FROM deaths
    where continent is not null
    Group by continent
    order by TotalDeathCount DESC
    LIMIT 10
"""
''' GLOBAL NUMBERS '''
'''  '''
sql_query = """
    SELECT SUM(new_cases) as total_cases, SUM(new_deaths) as total_deaths, SUM(new_deaths)/SUM(new_cases)*100 as DeathPercentage
    FROM deaths
    where continent is not null
    order by 1,2
    LIMIT 10
"""
''' looking at total populations vs vaccinations '''
sql_query = """
    SELECT deaths.continent, deaths.Location, deaths.date, deaths.population, vaccinations.new_vaccinations, SUM(vaccinations.new_vaccinations) OVER (Partition by deaths.location Order by deaths.location, deaths.date) as RollingPeopleVaccinated
    FROM deaths
    JOIN vaccinations
        On deaths.Location = vaccinations.location 
        and deaths.date = vaccinations.date
    WHERE deaths.continent is not null
    order by 2,3
    LIMIT 100
"""
''' Using CTE '''
sql_query = """
    with PopvsVac (continent, location, date, population, new_vaccinations, RollingPeopleVaccinated)
    as
    (
    SELECT deaths.continent, deaths.Location, deaths.date, deaths.population, vaccinations.new_vaccinations, SUM(vaccinations.new_vaccinations) OVER (Partition by deaths.location Order by deaths.location, deaths.date) as RollingPeopleVaccinated
    FROM deaths
    JOIN vaccinations
        On deaths.Location = vaccinations.location 
        and deaths.date = vaccinations.date
    WHERE deaths.continent is not null
    LIMIT 100
    )
    SELECT *, (RollingPeopleVaccinated/Population)*100
    FROM PopvsVac
"""
sql_query = """
    Create view PercentPopulationVaccinated as
    SELECT deaths.continent, deaths.Location, deaths.date, deaths.population, vaccinations.new_vaccinations
    , SUM(vaccinations.new_vaccinations) OVER (Partition by deaths.location Order by deaths.location, deaths.date) as RollingPeopleVaccinated
    FROM deaths
    JOIN vaccinations
        On deaths.Location = vaccinations.location 
        and deaths.date = vaccinations.date
    WHERE deaths.continent is not null
    LIMIT 100
"""
sql_query = """
    SELECT * from PercentPopulationVaccinated
"""
# Execute the SQL query
cur.execute(sql_query)

# Fetch the results and print them
results = cur.fetchall()
for row in results:
    print(row)

# Commit the changes and close the connection
conn.commit()
conn.close()
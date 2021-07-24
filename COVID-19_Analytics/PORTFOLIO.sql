--UPDATE PortfolioDataBase..CovidDeaths SET continent = NULL WHERE continent = ''


select * 
from PortfolioDataBase..CovidDeaths
where continent is not null
order by 3,4

--select * 
--from PortfolioDataBase..CovidVaccinations
--order by 3,4

--select Location, date, total_cases, new_cases, total_deaths, population
--from PortfolioDataBase..CovidDeaths
--order by 1,2


-- Looking at all infection cases...

-- The probability of contracting coronavirus in USA

select Location, date, total_cases, total_deaths, (CAST(CovidDeaths.total_deaths AS FLOAT)/NULLIF(CAST(CovidDeaths.total_cases AS FLOAT),0))*100 as DeathPercentage
from PortfolioDataBase..CovidDeaths
where location like '%states%'
and continent is not null
order by 1,2




select Location, date, Population,total_cases, (CAST(CovidDeaths.total_cases AS FLOAT)/NULLIF(CAST(CovidDeaths.Population AS FLOAT),0))*100 as PercentageInfected
from PortfolioDataBase..CovidDeaths
--where location like '%states%'
order by 1,2


--Highest infection rates compared to population

select Location, Population,MAX(CAST(CovidDeaths.total_cases AS FLOAT)) as HighestInfectionCount, MAX((CAST(CovidDeaths.total_cases AS FLOAT)/NULLIF(CAST(CovidDeaths.Population AS FLOAT),0))*100) as PercentageInfectedMax
from PortfolioDataBase..CovidDeaths
 
Group by Location, Population
--where location like '%states%'
order by PercentageInfectedMax DESC

--Showing countries with highest deathcount per population

select Location, MAX(CAST(CovidDeaths.total_deaths AS FLOAT)) as TotalDeathCount
from PortfolioDataBase..CovidDeaths

where continent is not null

Group by Location
--where location like '%states%'
order by TotalDeathCount DESC

--Showing continents with highest deathcount per population

select Location, MAX(CAST(CovidDeaths.total_deaths AS FLOAT)) as TotalDeathCount
from PortfolioDataBase..CovidDeaths

where continent is null

Group by Location
--where location like '%states%'
order by TotalDeathCount DESC

--global num-s

select data, SUM(CAST(new_cases AS FLOAT)) as TotalCases, SUM(CAST(new_deaths AS FLOAT)) as TotalDeaths, (SUM(CAST(new_deaths AS FLOAT))/NULLIF(SUM(CAST(new_cases AS FLOAT)),0))*100 as DeathPercentage
from PortfolioDataBase..CovidDeaths
--where location like '%states%'
where continent is not null
group by date
order by 1,2

--all of the world

select   SUM(CAST(new_cases AS FLOAT)) as TotalCases, SUM(CAST(new_deaths AS FLOAT)) as TotalDeaths, (SUM(CAST(new_deaths AS FLOAT))/NULLIF(SUM(CAST(new_cases AS FLOAT)),0))*100 as DeathPercentage
from PortfolioDataBase..CovidDeaths
--where location like '%states%'
where continent is not null
--group by date
order by 1,2

--Second Table

--UPDATE PortfolioDataBase..CovidVaccinations SET new_vaccinations = NULL WHERE new_vaccinations = ''

--Total population vs the vaccinated

select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations as FLOAT)) OVER (Partition by dea.location Order by dea.location, dea.Date) as TotalVaccinationsCurrently
from PortfolioDataBase..CovidDeaths dea
JOIN PortfolioDataBase..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent is not null
order by 2,3


--Using CTE to see the last data concerning vaccinations

With PopvsVac (Continent, location, date, population, new_vaccinations, TotalVaccinationsCurrently)
AS
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations as FLOAT)) OVER (Partition by dea.location Order by dea.location, dea.Date) as TotalVaccinationsCurrently
from PortfolioDataBase..CovidDeaths dea
JOIN PortfolioDataBase..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent is not null
--order by 2,3

)

select *, (CAST(TotalVaccinationsCurrently AS FLOAT)/NULLIF(CAST(Population AS FLOAT),0))*100 as PercentVaccinatedCurrently
FROM PopvsVac

--The same but via TEMP TABLE

DROP TABLE if exists #PercentPopulationVaccinated3
Create Table #PercentPopulationVaccinated3
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population nvarchar(255),
new_vaccinations nvarchar(255),
TotalVaccinationsCurrently nvarchar(255)
)
Insert into #PercentPopulationVaccinated3
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
,SUM(CAST(vac.new_vaccinations as FLOAT)) OVER (Partition by dea.location Order by dea.location, dea.Date) as TotalVaccinationsCurrently
from PortfolioDataBase..CovidDeaths dea
JOIN PortfolioDataBase..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent is not null
--order by 2,3

select *, (CAST(TotalVaccinationsCurrently AS FLOAT)/NULLIF(CAST(Population AS FLOAT),0))*100 as PercentVaccinatedCurrently
FROM #PercentPopulationVaccinated3






--Views to store data for visuals

Create VIEW PercentPopulationVaccinated as
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations as FLOAT)) OVER (Partition by dea.location Order by dea.location, dea.Date) as TotalVaccinationsCurrently
from PortfolioDataBase..CovidDeaths dea
JOIN PortfolioDataBase..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent is not null 

select *
FROM PercentPopulationVaccinated

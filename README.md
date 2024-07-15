# Weather Data Pipeline from API


## Objective
Create a pipeline to fetch weather data from an API, process it, and store it in a database for further analysis and visualization.

You can check my presentation with this [LINK](https://docs.google.com/presentation/d/17DKl1tHmxJMJBuGKcAIIMvfL2jxO79IEYLgNr0L5N_s/edit?usp=sharing)

## Technologies Involved
- **Programming Language:** Python (for scripting and data manipulation)
- **API:** OpenWeatherMap API
- **Database:** PostgreSQL
- **Tools:** Docker (for containerization), Airflow (for scheduling and orchestrating the pipeline), Grafana (for visualization)

## How to run

### Step 1: docker-compose up -d
- Dockerize your environment to ensure consistency and portability.
- Set up containers for PostgreSQL (for data storage), Airflow (for orchestration), and Grafana (for visualization).
- {make sure the db is auto-build and the coordinates data is already in db}
- {how to append collected data in development}

### Step 2: add your API key
- You can Sign Up on [Weather API](https://www.weatherapi.com/) to get your API keys
- {How to set user-own API}

### Step 3: unpause the DAGs
- {installing airflow}
- {make sure the DAGs is already have}
- {make sure connected to postgres}

### Step 4: Grafana
- {How to grafana}
- {make sure db is configurated}
- {ensure dashboard template is exist}

## Code Explained

### DAGs

### Response

### Wrangling and Cleaning

### Inserting to Database

## Additional Considerations
- **Security:** Ensure API keys and sensitive data are securely managed within your Docker/local environment.

## Conclusion
By building this pipeline, I gained practical experience in fetching API, scheduling DAGs, Processing raw data, also evaluate and monitoring data by visualization in dashboard

## Recommendation
- Make improvement about Data Governance in the database
- Adding more API or use real hardware so it can be streamed with real-time data and much more source data

## Updates Notice

(16/07/24)
- Fixing README.md

TODO :
- Make sure docker and build makefile to initialize container
- Explaining how the code works
- Make sure the image, database, and API key to smoothly runs
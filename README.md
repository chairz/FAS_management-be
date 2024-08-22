# Financial Assistance Scheme Management System

This project is a backend service for managing financial assistance schemes, applicants, and their applications. It is built on macOS with FastAPI and MySQL, and is containerized using Docker for easy setup and deployment.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Clone the Repository](#clone-the-repository)
  - [Environment Variables](#environment-variables)
  - [Docker Setup](#docker-setup)
- [Running the Application](#running-the-application)
- [Sample Request Data](#sample-request-data)
- [API Documentation](#api-documentation)


### **Overview**

- **`app/`**: Contains the core logic of the application.
  - **`crud/`**: Houses all CRUD operations, which are divided by tables. This structure keeps operations related to different tables separated, making the codebase easier to maintain.
  - **`db/`**: Contains database configurations, connection management, and the SQLAlchemy models that define the database schema. For a detailed explanation of the database schema, please refer to the [Database Schema Documentation](app/db/db_schema.md)
  - **`router/`**: Contains all the route handlers, each categorized by the type of entity they manage (e.g., `auth`, `applicants`, `schemes`, `applications`).
  - **`schemas/`**: Contains Pydantic models that define the structure of request and response bodies for each API endpoint. This ensures data validation and serialization are handled cleanly.
  - **`dependencies.py`**: Contains shared dependencies that are injected into routes. This might include functions authenticating JWTs, database session, etc.
  - **`config/`**: Contains configuration files, including settings for logging and other application-wide configurations.

- **`main.py`**: The main entry point of the application, where the FastAPI app is instantiated and routers are included.

- **`sample_data/`**: Contains JSON files with sample request data for testing each endpoint. This allows for quick and easy testing of the API.

- **`Dockerfile`**: Defines the Docker image for the FastAPI application. It installs the necessary dependencies and sets up the environment.

- **`docker-compose.yml`**: Sets up the entire application stack, including the FastAPI app and the MySQL database, using Docker Compose.

- **`requirements.txt`**: Lists all the Python packages that the application depends on.

- **`config.env`**: Contains environment variables that configure the application, such as database connection details and secret keys.

- **`README.md`**: Provides documentation for the project, including setup instructions, API usage, and project structure.

## Prerequisites

Ensure you have the following installed on your machine:

- Docker
- Docker Compose

## Setup

### Clone the Repository

Clone this repository to your local machine.

```bash
git clone git@github.com:chairz/FAS_management-be.git
cd FAS_management-be
```

### Environment Variables

Create a `config.env` file in the root directory of the project, 
a sample of the required variables can be found under `config.env.example`.

To simplify the demo setup for this project. I have attached a working config.env file, however, take note that this should **NOT** be uploaded to the repository in production.

### Docker Setup

The project is fully containerized using Docker. The Docker Compose configuration sets up the FastAPI application and a MySQL database.


## Running the Application

To build and run the Docker containers, execute the following command:
```bash
docker-compose up --build
```

This command will:

- Build the Docker images for the application.
- Set up a MySQL database container.
- Run the FastAPI application, which will automatically create the necessary database tables.

Once the containers are running, the application will be available at http://localhost:8000.

## Sample Request Data

Sample JSON request data is provided in the `sample_request_data` folder. You can use these files to test the API endpoints.

### Example Usage with Curl

You can use the following command to create an applicant using the sample data:

```bash
curl -X POST "http://localhost:8000/api/applicants" -H "Content-Type: application/json" -d @sample_request_data/create_applicant.json
```

## API Documentation
Once the application is running, you can access the API documentation at:

- Redoc: http://localhost:8000/redoc
- Swagger UI: http://localhost:8000/docs

These provide interactive documentation for testing the API endpoints.
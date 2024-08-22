# Financial Assistance Scheme Management System

This project is a backend service for managing financial assistance schemes, applicants, and their applications. It is built with FastAPI and MySQL, and is containerized using Docker for easy setup and deployment.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Clone the Repository](#clone-the-repository)
  - [Environment Variables](#environment-variables)
  - [Docker Setup](#docker-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)



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


## API Documentation
Once the application is running, you can access the API documentation at:

- Redoc: http://localhost:8000/redoc
- Swagger UI: http://localhost:8000/docs

These provide interactive documentation for testing the API endpoints.
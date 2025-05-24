# Job Platform

## Overview

The **Job Platform** is a web application that allows users to create, update, delete, and view job postings. The platform includes API endpoints for managing job listings and incorporates features such as filtering, pagination, and search by multiple fields like job title, description, and company name.

## Assumptions & Design Decisions

- **Django Framework**: The application is built using Django to manage backend tasks and handle user requests.
- **Django Ninja**: Used for creating API endpoints for CRUD operations related to jobs. This is a lightweight framework built on top of FastAPI, optimized for speed and ease of use with Pydantic.
- **JWT Authentication**: JWT is used for securing API endpoints, ensuring that only authenticated users can access and perform certain operations (like creating or updating jobs).
- **Database**: The database is managed using SQLite during development for simplicity and portability, though it can easily be switched to PostgreSQL for production.
- **Django ORM**: The models for the jobs are defined using Django's ORM to handle database operations.
- **OpenAPI & Documentation**: The API documentation is automatically generated using Django Ninja's OpenAPI support.

## Setup & Running Locally

### Prerequisites

1. **Python 3.10+** is required.
2. Ensure that **Django** and **Django Ninja** are installed.
3. Ensure taht **pdm** is installed.

### 1. Clone the Repository

Clone the repository to your local machine using Git:

```bash
git clone <repository_url>
cd <project_folder>
```

### 2. Install Dependencies
This project uses PDM for dependency management. Install the required dependencies with:

```bash
pdm install
```

### 3. Apply migrations:
Make sure to run migrations to set up the database schema:

```bash
pdm run python manage.py migrate
```

### 4. Run the application:
Start the development server:

```bash
pdm run python manage.py runserver
```
The application will be available at http://127.0.0.1:8000.

### API Endpoints

- **GET /api/jobs/**: Retrieve a list of jobs with optional filters and pagination.
- **POST /api/jobs/**: Create a new job posting.
- **GET /api/jobs/{id}/**: Get a specific job by ID.
- **PUT /api/jobs/{id}/**: Update an existing job posting.
- **DELETE /api/jobs/{id}/**: Delete a job posting.

## Assumptions

- Only authenticated users can create, update, or delete job postings.
- The required fields for job postings are: `title`, `company_name`, `description`, `posting_date`, and `expiration_date`.
- SQLite is used as the default database for development. In production, you can switch to PostgreSQL or another relational database by updating the database settings in `settings.py`.

## Testing

To run the test suite, use:

```bash
pdm run pytest
```

This will execute the tests and ensure everything is functioning as expected.

## Deployment

### Database for Production
To deploy the project to production, we recommend switching the database to PostgreSQL or another relational database for better scalability and reliability.

Update your `settings.py` database configuration to use PostgreSQL.

### Environment Variables
For security reasons, ensure your sensitive environment variables (e.g., JWT secret keys, database credentials) are configured correctly. You can use `.env` files or services like [django-environ](https://django-environ.readthedocs.io/en/latest/) to manage these settings securely.

Fitness Center Management System

The Fitness Center Management System is a backend application developed using FastAPI, PostgreSQL, and SQLAlchemy. It provides a robust and scalable API for managing the operations of a fitness center, including member registration, trainer schedules, administrative tools, equipment tracking, class management, and more. The system follows a modular architecture to ensure maintainability, clarity, and extensibility.


Overview
The application is designed to handle the core operational needs of a fitness center. It provides distinct interfaces for members, trainers, and administrators, each with clearly defined responsibilities and permissions. SQLAlchemy ORM is used for database modeling and interaction, ensuring clean schema definitions and efficient query 
handling.

Video description: https://youtu.be/C0WzHhe5Iuw

Features
Member Features
Create and manage member profiles.
Register for group fitness classes.
Track health metrics such as weight, body fat, and heart rate.
Maintain personal fitness goals.

Trainer Features
Profile creation and management.
Define and update availability schedules.
Train members individually through personal training sessions.

Admin Features
Manage rooms and facility spaces.
Oversee gym equipment, including status tracking and repairs.
Create and schedule group fitness classes.
Record and resolve maintenance issues.

System Features
Full CRUD operations for all major resources.
Comprehensive validation using Pydantic schemas.
SQLAlchemy ORM database layer.
Centralized routing through FastAPI for clarity and testability.

Technology Stack
Programming Language: Python 3.10+
Framework: FastAPI
Database: PostgreSQL
ORM: SQLAlchemy
Validation: Pydantic
Server: Uvicorn (ASGI)
Tools: pgAdmin, pip, virtual environments



Setup and Installation
Clone the repository
git clone <repository-url>
cd <project-folder>

Create a virtual environment and install dependencies
pip install -r requirements.txt
Copy the environment template
cp env/template.env .env

Update .env with your PostgreSQL credentials.

Environment Configuration

Your .env file must contain valid database connection information. Example:

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=fitness_center_db_group
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/fitness_center_db_group

Ensure .env is never committed to version control.

Database Setup
You can create the database using pgAdmin or the PostgreSQL command line.

Option A: Using pgAdmin
Open pgAdmin and register your server.
Right-click "Databases" → "Create" → "Database".
Enter the database name shown in .env.

Option B: Using psql
CREATE DATABASE fitness_center_db_group;
Schema Creation
Tables are automatically created when FastAPI starts and SQLAlchemy loads the models (if Base.metadata.create_all(engine) is included in your startup logic).

Running the Application
Start the FastAPI server:
uvicorn main:app --reload

The API will be available at:
http://localhost:8000

To run our Frontend run the following commands one at a time:
npm install
cd frontend
npm run dev

Frontend will be available at:
http://localhost:3000/


API Documentation

FastAPI automatically generates Swagger documentation. Access it at:

http://localhost:8000/docs


The Swagger interface allows interactive testing of all API endpoints.

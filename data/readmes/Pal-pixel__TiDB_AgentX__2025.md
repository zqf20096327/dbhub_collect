# TiDB4 Application with B+ Tree Search

This application demonstrates the use of  B+ tree indexing capabilities for efficient question-answer data retrieval.

## Features

- B+ tree indexed search for fast data retrieval
- Question-answer database with keyword support
- REST API for managing QnA entries
- CSV data import capability
- React frontend with search interface

## Running the Application with Docker Compose

To get the application up and running, follow these simple steps:

1. Navigate to the root directory of the project.

2. Execute the following command in your terminal:
   ```bash
   docker-compose up --build
   ```
   This command will build the necessary images and start two containers: one for the frontend and one for the backend.

## Fixing Backend Connection Issues

1. **If the frontend shows “Backend Not Connected”, simply run the provided batch file:**
   ```
   ./run-backend.bat
   ```
   This script will:

Create a bridge container that resolves database connection conflicts between the backend and TiDB.

Establish a stable link so the Spring Boot backend can communicate properly with the database.

Ensure the frontend can connect to the backend without errors.
 Recommendation:
Keep this extra container running in the background while developing. It’s outside your main docker-compose setup and can be stopped later if needed, but keeping it running during development ensures everything works smoothly..


## Accessing the Application

Once the application is running, you can access it through your browser at the following addresses:

- Frontend: http://localhost:3000
- Backend: http://localhost:8081


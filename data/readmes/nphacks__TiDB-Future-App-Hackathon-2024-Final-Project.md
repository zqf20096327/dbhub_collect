# PaperTrail

This project is a full-stack application designed to manage and search research papers using advanced vector search capabilities. The system is divided into two parts: the backend, which is built using Node.js and Express.js, and the frontend, which is developed using Angular.


## Project Structure

- **Backend Folder**: `backend-research`
- **Frontend Folder**: `frontend`


## Setup Instructions
### Environment Variables

An `.env` file has been sent to the hackathon judges via email:

- **To**: `hackathon-judge@pingcap.com`
- **From**: `nishtha.hackathon@gmail.com`

Please place the provided `.env` file in the `backend-research` folder.
It was also submitted with the project submission at 'Upload a File'.


### Backend Setup

Navigate to the `backend-research` folder and run the following commands:

```bash
cd backend-research
npm install
npm start
```

### Frontend Setup
Navigate to the `frontend` folder and run the following commands:

```bash
cd frontend
npm install
ng serve
```

The frontend will be running on http://localhost:4200.


## Key Features
Vector Search for Research Papers: Advanced vector-based search engine for finding similar research papers.
Responsive Frontend: Built with Angular for an intuitive user experience.


## How to Run the Project
- Ensure the .env file is correctly placed in the backend-research folder.
- Start the backend server using npm start.
- Start the frontend using ng serve.
- Access the application through your browser at http://localhost:4200
- Search for a terms like superconnectivity, superconductors, artificial intelligence or more


### Dependencies
- Backend
    - Node.js
    - Express.js
    - MySQL (TiDB)

- Frontend
    - Angular
    - Angular CLI

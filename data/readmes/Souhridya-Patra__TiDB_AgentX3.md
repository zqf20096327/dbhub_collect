Running the Application with Docker Compose
To get the application up and running, follow these simple steps:

Navigate to the root directory of the project.

Execute the following command in your terminal:

Bash

docker-compose up --build
This command will build the necessary images and start two containers: one for the frontend and one for the backend. The application will then be accessible via your browser.

Accessing the Containers
Once the containers are running, you can access the application through your browser at the following addresses:

Frontend: http://localhost:[port]

Backend: http://localhost:[port]

Note: Be sure to replace [port] with the specific port numbers you have exposed in your docker-compose.yml file.

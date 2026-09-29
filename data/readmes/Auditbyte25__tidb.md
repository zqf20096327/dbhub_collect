This project is created by flexdev using TIDB as a database and the mode of querying and implementation is similar to mysql.
Signup and create TIDB account and create the cluster which will enable to get password and connection code to use || check config > db.js to check the database configuration and connection.
store your password in .env file for security purposes.

Base url - http://localhost:4000/api/v1/
Register url - http://localhost:4000/api/v1/register || post request
post login - http://localhost:4000/api/v1/login

Storing chat in the database
Post chat url - http://localhost:4000/api/v1/chat/create-chat/:id
Get chat url - http://localhost:4000/api/v1/chat/get-chat/:id

Storing Journal
Post journal url - http://localhost:4000/api/v1/journal/create-journal/:id
Get journal url - http://localhost:4000/api/v1/journal/get-journal/:id

Storing Movie
Post movie url - http://localhost:4000/api/v1/movie/create-movie/:id
Get movie url - http://localhost:4000/api/v1/movie/get-movie/:id

To run this code:
run >> npm install
Add TIDB password to .env file.
run >> node index.js || nodemon indes.js

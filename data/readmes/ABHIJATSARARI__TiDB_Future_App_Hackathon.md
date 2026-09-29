# TiDB_Future_App_Hackathon

<!-- README.md -->
<!-- This file provides the documentation for the project -->

# EduNex

EduNex is a decentralized application that combines blockchain technology with TiDB Cloud 33 Serverless to create a tamper-proof and transparent education credential verification system. Educational institutions can issue digital certificates and degrees on the blockchain, and students can share their credentials securely with employers and other stakeholders. EduNex eliminates the need for costly third-party verification services and provides a reliable way to validate educational achievements, reducing fraud and improving trust in the education ecosystem.

# Features

- Certificate issuance: Educational institutions can issue digital certificates on the blockchain
- Certificate verification: Students and employers can verify the authenticity of certificates on the blockchain
- Student registration: Students can register their profiles and credentials on the blockchain

![](https://github.com/ABHIJATSARARI/TiDB_Future_App_Hackathon/blob/main/frontend/public/logo.png)

# Technologies

- Frontend: React.js
- Backend: Node.js, Express.js, MongoDB, Mongoose
- Blockchain: Solidity, Truffle, web3.js
- Database: TiDB Cloud 33 Serverless

# Installation

To run this project locally, you need to have Node.js, MongoDB, Truffle and Ganache installed on your machine.

1. Clone this repository
. Install the dependencies for the frontend and backend modules
Copy
cd frontend && npm install cd backend && npm install

3. Compile and migrate the smart contracts using Truffle and Ganache
Copy
cd blockchain && truffle compile && truffle migrate

4. Start the backend server
Copy
cd backend && npm start

5. Start the frontend server
Copy
cd frontend && npm start

6. Open http://localhost:3000 in your browser to view the app

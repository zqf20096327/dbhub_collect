<div align="center">

# ⚡ Express Backend Framework: Scalable Node.js API with Multi-Database Support

[![Node.js Version](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen)](https://nodejs.org/) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![GitHub Stars](https://img.shields.io/github/stars/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server.svg)](https://github.com/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server/stargazers) [![GitHub Issues](https://img.shields.io/github/issues/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server.svg)](https://github.com/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server/issues) [![Code Coverage](https://img.shields.io/codecov/c/github/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server.svg)](https://codecov.io/gh/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server) [![Last Commit](https://img.shields.io/github/last-commit/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server.svg)](https://github.com/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server/commits/main) [![Contributors](https://img.shields.io/github/contributors/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server.svg)](https://github.com/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server/graphs/contributors) [![GitHub Forks](https://img.shields.io/github/forks/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server.svg)](https://github.com/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server/network/members)

Welcome to the **Scalable-MultiDB-Express-Server** project! This is a robust backend application built with Node.js and Express.js, designed to provide a scalable and flexible foundation for web applications. The project supports multiple database systems, including MySQL and MongoDB, and includes features for user management, customer handling, file uploads, and more. This documentation is tailored for new users to help you get started quickly, understand the project structure, and effectively use and contribute to the codebase.

</div>

<div align="justify">

## Project Overview

- **Framework**: Node.js with Express.js
- **Databases**: Support for MySQL and MongoDB
- **Template Engine**: EJS for server-side rendering
- **Key Features**:
  - RESTful API endpoints
  - User and customer management
  - File upload functionality
  - Database CRUD operations
  - Middleware for handling requests
  - Seeder for initial data population

The project is organized into modular components, making it easy to extend and maintain.

## Project Structure

Here's a breakdown of the main directories and files in the workspace:

- **`src/`**: Core application code
  - **`server.js`**: Main entry point for the Express server
  - **`config/`**: Configuration files
    - **`viewEngine.js`**: EJS view engine setup
    - **`mongodb/database.js`**: MongoDB connection configuration
    - **`mysql/database.js`**: MySQL connection configuration
  - **`controllers/`**: Request handlers
    - **`apiController.js`**: General API controllers
    - **`customerController.js`**: Customer-specific logic
    - **`mongodb/homeController.js`**: Home page logic for MongoDB
    - **`mysql/homeController.js`**: Home page logic for MySQL
  - **`middleware/`**: Custom middleware functions
  - **`migration/`**: Database migration scripts
  - **`models/`**: Data models
    - **`customer.js`**: Customer model
    - **`user.js`**: User model
  - **`routes/`**: Route definitions
    - **`api.js`**: API routes
    - **`mongodb/web.js`**: Web routes for MongoDB
    - **`mysql/web.js`**: Web routes for MySQL
  - **`seeder/`**: Scripts for seeding initial data
  - **`services/`**: Business logic services
    - **`CustomerService.js`**: Customer-related services
    - **`fileService.js`**: File handling services
    - **`mongodb/CRUDService.js`**: CRUD operations for MongoDB
    - **`mysql/CRUDService.js`**: CRUD operations for MySQL
  - **`views/`**: EJS templates
    - **`home.ejs`**: Home page template
    - **`create.ejs`**: Create form template
    - **`edit.ejs`**: Edit form template
    - **`delete.ejs`**: Delete confirmation template
- **`public/`**: Static assets
  - **`css/style.css`**: Stylesheets
  - **`js/`**: Client-side JavaScript
  - **`images/`**: Image files and uploads directory
- **`references/docs.md`**: This documentation file
- **`package.json`**: Project dependencies and scripts
- **`README.md`**: General project information
- **`LICENSE`**: Project license

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Node.js** (version 14 or higher): Download from [nodejs.org](https://nodejs.org/)
- **npm** (comes with Node.js) or **yarn** for package management
- **MySQL** (if using MySQL database): Download from [mysql.com](https://www.mysql.com/)
- **MongoDB** (if using MongoDB): Download from [mongodb.com](https://www.mongodb.com/)

## Installation and Setup

1. **Clone the Repository**:

   ```
   git clone https://github.com/NhanPhamThanh-IT/Scalable-MultiDB-Express-Server.git
   cd Scalable-MultiDB-Express-Server
   ```

2. **Install Dependencies**:

   ```
   npm install
   ```

3. **Configure Environment**:

   - Copy `.env.example` to `.env` (if exists) and fill in your configuration details.
   - For MySQL: Update `config/mysql/database.js` with your database credentials.
   - For MongoDB: Update `config/mongodb/database.js` with your MongoDB connection string.

4. **Set Up Database**:

   - Create a MySQL database and run any migration scripts in `src/migration/`.
   - For MongoDB, ensure your MongoDB instance is running and accessible.

5. **Seed Initial Data** (optional):
   - Run seeder scripts in `src/seeder/` to populate sample data.

## Running the Application

1. **Start the Server**:

   ```
   npm start
   ```

   Or for development with auto-reload:

   ```
   npm run dev
   ```

2. **Access the Application**:
   - Open your browser and navigate to `http://localhost:3000` (or the configured port).
   - API endpoints are available under `/api/`.

## API Documentation

The application provides RESTful API endpoints for managing users, customers, and other resources. Here are the main routes:

### General API Routes (`/api`)

- `GET /api/` - Welcome message
- `GET /api/customers` - Get all customers
- `POST /api/customers` - Create a new customer
- `GET /api/customers/:id` - Get customer by ID
- `PUT /api/customers/:id` - Update customer
- `DELETE /api/customers/:id` - Delete customer

### Web Routes

- `GET /` - Home page
- `GET /create` - Create customer form
- `POST /create` - Submit new customer
- `GET /edit/:id` - Edit customer form
- `POST /edit/:id` - Update customer
- `GET /delete/:id` - Delete confirmation
- `POST /delete/:id` - Confirm delete

For detailed request/response formats, refer to the controller files in `src/controllers/`.

## Database Models

- **User Model** (`src/models/user.js`): Handles user authentication and profiles.
- **Customer Model** (`src/models/customer.js`): Manages customer data and interactions.

## Services

- **CustomerService** (`src/services/CustomerService.js`): Business logic for customer operations.
- **FileService** (`src/services/fileService.js`): Handles file uploads and management.
- **CRUDService** (MongoDB/MySQL): Database-specific CRUD operations.

## Configuration

- **View Engine**: Configured in `src/config/viewEngine.js` to use EJS templates.
- **Database Connections**: Separate configs for MySQL and MongoDB in `src/config/`.

## Troubleshooting

- **Server won't start**: Check if the required ports are available and database connections are valid.
- **Database connection errors**: Verify your database credentials and ensure the database server is running.
- **File upload issues**: Ensure the `public/images/uploads/` directory exists and has write permissions.
- **Package installation fails**: Try clearing npm cache with `npm cache clean --force` and reinstall.

## Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or suggesting enhancements, your help is appreciated.

### Getting Started with Contributing

1. **Fork the Repository**:

   - Click the "Fork" button on the GitHub repository page.
   - Clone your fork: `git clone https://github.com/your-username/Scalable-MultiDB-Express-Server.git`

2. **Set Up Development Environment**:

   - Follow the Installation and Setup instructions above.
   - Install development dependencies: `npm install`

3. **Create a Feature Branch**:

   - `git checkout -b feature/your-feature-name`
   - Use descriptive names like `feature/add-user-authentication` or `fix/database-connection-issue`

4. **Make Your Changes**:

   - Write clear, concise code following the project's coding standards.
   - Add tests for new features or bug fixes.
   - Update documentation if necessary.

5. **Commit Your Changes**:

   - Use meaningful commit messages: `git commit -m 'Add user authentication feature'`
   - Follow conventional commit format if possible (e.g., `feat:`, `fix:`, `docs:`)

6. **Push and Create Pull Request**:
   - Push to your fork: `git push origin feature/your-feature-name`
   - Create a pull request on the main repository.
   - Provide a clear description of your changes and why they're needed.

### Development Guidelines

- **Code Style**: Follow consistent indentation (4 spaces), meaningful variable names, and add comments for complex logic.
- **Testing**: Add unit tests for new functionality. Run `npm test` to execute tests.
- **Documentation**: Update README.md or add JSDoc comments for new functions.
- **Database**: Ensure your changes work with both MySQL and MongoDB configurations.
- **Security**: Be mindful of security implications, especially for user input handling.

### Reporting Issues

If you find a bug or have a feature request:

1. Check existing issues on GitHub.
2. Create a new issue with a clear title and description.
3. Include steps to reproduce, expected vs. actual behavior, and environment details.

### Code Review Process

- All pull requests will be reviewed by maintainers.
- Address any feedback or requested changes.
- Once approved, your contribution will be merged!

Thank you for contributing to Scalable-MultiDB-Express-Server!

## Understanding the Project Architecture

This project follows the MVC (Model-View-Controller) pattern with additional service layers for better separation of concerns.

### MVC Components

- **Models** (`src/models/`): Define data structures and interact with databases.
- **Views** (`src/views/`): EJS templates for rendering HTML pages.
- **Controllers** (`src/controllers/`): Handle HTTP requests, process data, and return responses.

### Service Layer

- **Services** (`src/services/`): Contain business logic, reusable functions, and database operations.
- Separate services for general logic (e.g., `CustomerService.js`, `fileService.js`) and database-specific CRUD operations.

### Routing

- **Routes** (`src/routes/`): Define URL patterns and map them to controller functions.
- Organized by functionality (API routes, web routes) and database type.

### Configuration

- **Config** (`src/config/`): Database connections, view engine setup, and other configurations.
- Supports both MySQL and MongoDB for flexibility.

### Middleware

- **Middleware** (`src/middleware/`): Custom functions that process requests before they reach controllers.
- Handles authentication, logging, error handling, etc.

### Static Assets

- **Public** (`public/`): CSS, JavaScript, images served directly by Express.

This modular structure makes the application easy to maintain, test, and extend.

## Database Setup and Configuration

### Choosing a Database

This project supports both MySQL and MongoDB. Choose based on your needs:

- **MySQL**: Relational database, good for structured data with complex relationships.
- **MongoDB**: NoSQL database, flexible schema, good for rapid prototyping and varying data structures.

You can switch between databases by updating the route imports in `src/server.js`.

### MySQL Setup

1. Install MySQL server from [mysql.com](https://www.mysql.com/).
2. Create a database: `CREATE DATABASE node_express_backend;`
3. Update `src/config/mysql/database.js` with your credentials:

```javascript
const mysql = require("mysql2");

const connection = mysql.createConnection({
  host: "localhost",
  user: "your_username",
  password: "your_password",
  database: "node_express_backend",
});

module.exports = connection;
```

4. Run migrations if any exist in `src/migration/`.

### MongoDB Setup

1. Install MongoDB from [mongodb.com](https://www.mongodb.com/).
2. Start MongoDB service.
3. Update `src/config/mongodb/database.js`:

```javascript
const mongoose = require("mongoose");

mongoose.connect("mongodb://localhost:27017/node_express_backend", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

module.exports = mongoose;
```

### Environment Variables

For production, use environment variables for sensitive data:

```javascript
// Example for MySQL
require("dotenv").config();

const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});
```

Create a `.env` file in the root directory:

```
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=node_express_backend
```

## API Usage and Examples

### Authentication

If your application requires authentication, implement it in middleware and controllers.

### Making API Calls

Here are examples using JavaScript's fetch API:

#### Get All Customers

```javascript
fetch("/api/customers")
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error("Error:", error));
```

#### Create a New Customer

```javascript
const newCustomer = {
  name: "John Doe",
  email: "john@example.com",
  phone: "123-456-7890",
};

fetch("/api/customers", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(newCustomer),
})
  .then((response) => response.json())
  .then((data) => console.log("Customer created:", data))
  .catch((error) => console.error("Error:", error));
```

#### Update a Customer

```javascript
const updatedCustomer = {
  name: "Jane Doe",
  email: "jane@example.com",
};

fetch("/api/customers/123", {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(updatedCustomer),
})
  .then((response) => response.json())
  .then((data) => console.log("Customer updated:", data))
  .catch((error) => console.error("Error:", error));
```

#### Delete a Customer

```javascript
fetch("/api/customers/123", {
  method: "DELETE",
})
  .then((response) => {
    if (response.ok) {
      console.log("Customer deleted");
    } else {
      throw new Error("Failed to delete customer");
    }
  })
  .catch((error) => console.error("Error:", error));
```

### File Upload

To upload files, use the file upload functionality:

```html
<form action="/upload" method="post" enctype="multipart/form-data">
  <input type="file" name="file" />
  <button type="submit">Upload</button>
</form>
```

```javascript
// In your frontend JavaScript
const formData = new FormData();
formData.append("file", fileInput.files[0]);

fetch("/upload", {
  method: "POST",
  body: formData,
})
  .then((response) => response.json())
  .then((data) => console.log("File uploaded:", data))
  .catch((error) => console.error("Error:", error));
```

## Extending the Project

### Adding a New Feature

1. **Plan the Feature**: Define requirements and how it fits into the MVC structure.
2. **Create Model**: Add a new model in `src/models/` if needed.
3. **Implement Service**: Add business logic in `src/services/`.
4. **Create Controller**: Handle requests in `src/controllers/`.
5. **Define Routes**: Map URLs to controller functions in `src/routes/`.
6. **Add Views**: Create EJS templates if it's a web feature.
7. **Update Documentation**: Add to README.md and API docs.

### Example: Adding User Authentication

1. Create `src/models/user.js` with user schema.
2. Add `src/services/AuthService.js` for login/logout logic.
3. Create `src/controllers/authController.js` for auth routes.
4. Add routes in `src/routes/auth.js`.
5. Implement middleware for protected routes.
6. Add login/register views.

### Best Practices for Extensions

- Follow existing code patterns and naming conventions.
- Add appropriate error handling and validation.
- Write tests for new functionality.
- Update dependencies in `package.json` if needed.
- Ensure compatibility with both database types.

## Deployment Guide

### Local Development

For development, use:

```bash
npm run dev
```

This starts the server with nodemon for auto-reload.

### Production Deployment

1. **Environment Setup**:

   - Set `NODE_ENV=production`
   - Configure production database credentials
   - Set up environment variables

2. **Build Optimization**:

   - Minify static assets
   - Use a process manager like PM2

3. **Server Configuration**:

   - Set up reverse proxy with Nginx
   - Configure SSL certificates
   - Set up firewall and security measures

4. **Database**:
   - Use production database servers
   - Set up backups and monitoring

### Example PM2 Configuration

Create `ecosystem.config.js`:

```javascript
module.exports = {
  apps: [
    {
      name: "scalable-multidb-express-server",
      script: "src/server.js",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      env: {
        NODE_ENV: "production",
        PORT: 3000,
      },
    },
  ],
};
```

Start with PM2:

```bash
pm2 start ecosystem.config.js
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM node:14-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

Build and run:

```bash
docker build -t scalable-multidb-express-server .
docker run -p 3000:3000 scalable-multidb-express-server
```

## FAQ

### General Questions

**Q: Can I use this project for commercial applications?**
A: Yes, this project is open-source and can be used for commercial purposes. Check the LICENSE file for details.

**Q: How do I switch between MySQL and MongoDB?**
A: Update the route imports in `src/server.js` to use either `mysql/web.js` or `mongodb/web.js`.

**Q: Is there a frontend for this backend?**
A: This is a backend-only project. You can integrate it with any frontend framework like React, Vue, or Angular.

### Technical Questions

**Q: How do I handle file uploads larger than the default limit?**
A: Configure the file upload middleware in `src/server.js`:

```javascript
app.use(
  fileUpload({
    limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  })
);
```

**Q: How do I add custom middleware?**
A: Create your middleware function in `src/middleware/` and use it in `src/server.js`:

```javascript
const myMiddleware = require("./middleware/myMiddleware");
app.use(myMiddleware);
```

**Q: How do I add API versioning?**
A: Create versioned routes like `src/routes/v1/api.js` and mount them:

```javascript
app.use("/api/v1", require("./routes/v1/api"));
```

### Troubleshooting

**Q: Server won't start - port already in use**
A: Kill the process using the port or change the port in `src/server.js`.

**Q: Database connection fails**
A: Check your database credentials, ensure the database server is running, and verify network connectivity.

**Q: Static files not loading**
A: Ensure the `public` directory exists and is correctly configured in `src/server.js`.

## Support and Community

### Getting Help

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions and share ideas
- **Documentation**: Check this README and inline code comments

### Community Guidelines

- Be respectful and constructive in communications
- Help others when possible
- Follow the code of conduct

### Related Projects

- [Express.js Boilerplate](https://github.com/hagopj13/node-express-boilerplate) - The original boilerplate this project is based on
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices) - Best practices for Node.js development

Thank you for using Scalable-MultiDB-Express-Server! We hope this project helps you build amazing applications.

## References

- Boilerplate GitHub Repository: https://github.com/hagopj13/node-express-boilerplate
- Node.js Documentation: https://nodejs.org/docs/latest/api/
- Express.js Documentation: https://expressjs.com/en/starter/installing.html
- npm package manager: https://www.npmjs.com/
- yarn package manager: https://classic.yarnpkg.com/en/
- Nodemon GitHub Repository: https://github.com/remy/nodemon#nodemon
- EJS Template Engine Documentation: https://ejs.co/#docs
- MySQL Database: https://www.mysql.com/
- mysql Package: https://www.npmjs.com/package/mysql
- mysql2 Package: https://www.npmjs.com/package/mysql2
- MongoDB Drivers: https://www.mongodb.com/docs/drivers/
- Mongoose-delete Plugin: https://www.npmjs.com/package/mongoose-delete
- Express-fileupload Package: https://www.npmjs.com/package/express-fileupload
- api-query-params Package: https://www.npmjs.com/package/api-query-params

</div>

---

<div align="center">

⭐ If you like this project, give it a star!  
🐛 Found a bug? Help us improve by reporting it.  
🧩 Pull requests are always welcome.

</div>

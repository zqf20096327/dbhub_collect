# EMS - Event Management System

<div align="center">
  <img width="500px" src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/icon/EMS_Icon.png">
</div>

<div align="center">
  <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/VoxDroid/Event-Management-System/total?style=flat-square&svg=true">
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/VoxDroid/Event-Management-System?style=flat-square&svg=true">
  <img alt="Last Commit" src="https://img.shields.io/github/last-commit/VoxDroid/Event-Management-System?style=flat-square&svg=true">
  <img alt="License" src="https://img.shields.io/github/license/VoxDroid/Event-Management-System?style=flat-square&svg=true">
</div>

<p align="center">
  <a href="https://ko-fi.com/O4O6LO7Q1" target="_blank">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="ko-fi" style="border: 0;">
  </a>
</p>

## Introduction

EMS (Event Management System) is an open-source platform designed to streamline event organization and facility management. It offers a user-friendly, centralized solution for scheduling events, managing event details, and fostering community engagement through interactive features. Built with PHP and compatible with modern web servers and databases, EMS is ideal for organizations, communities, or individuals looking to manage events efficiently.

## Features

- **Event Data Management:** Store and manage event details such as date, time, location, and facilities in a centralized database.
- **Online Event Scheduling:** Schedule events seamlessly through an intuitive web interface.
- **Interactive Calendar:** View scheduled events and check facility availability with a dynamic calendar system.
- **User Profiles:** Create and customize user profiles with personalized settings and preferences.
- **Event Request and Approval Workflow:** Users can submit event requests, which admins can approve or deny with remarks.
- **Comment and Feedback System:** Engage with events through comments, likes, and dislikes, fostering interaction between users and organizers.
- **User Management:** Admins can manage user roles, permissions, and event approvals.
- **Security Features:** Includes secure login, password reset, user registration, and data protection mechanisms.
- **Event Status Tracking:** Monitor events through statuses like ongoing, approved, pending, completed, or denied.
- **Responsive Design:** Accessible on various devices with a modern, responsive interface.

## Prerequisites

Before installing EMS, ensure your system meets the following requirements:

- **Operating System:** Windows, macOS, Linux, or any modern OS.
- **Web Server:** Apache (with `mod_rewrite`), Nginx, or equivalent.
- **Database:** MySQL 5.7+, PostgreSQL 10+, or equivalent.
- **PHP:** Version 7.4 or higher (8.0+ recommended) with extensions:
  - `pdo_mysql` or `pdo_pgsql`
  - `mbstring`
  - `json`
  - `openssl`
- **Composer:** For managing PHP dependencies (optional, if using additional packages).
- **Node.js and npm:** For building front-end assets (if using custom JavaScript or CSS).
- **Git:** For cloning the repository.
- **Web Browser:** Latest version of Chrome, Firefox, Safari, or Edge.

## Installation

Follow these steps to set up EMS on your local or production server:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/VoxDroid/EMS.git
   cd EMS
   ```

2. **Configure the Web Server:**
   - Point your web server to the `EMS` directory as the document root.
   - For Apache, ensure `.htaccess` is enabled and `mod_rewrite` is active.
   - For Nginx, configure a server block (example configuration available in the [docs](#documentation) section).

3. **Set Up the Database:**
   - Create a database in MySQL or PostgreSQL.
   - Run the `database_setup.php` script to initialize the database schema:
     ```bash
     php database_setup.php
     ```
   - Alternatively, import the SQL schema from `database/schema.sql` if provided.

4. **Configure Database Credentials:**
   - Copy `db_connection_settings.example.php` to `db_connection_settings.php`:
     ```bash
     cp db_connection_settings.example.php db_connection_settings.php
     ```
   - Edit `db_connection_settings.php` with your database credentials:
     ```php
     <?php
     define('DB_HOST', 'localhost');
     define('DB_NAME', 'ems_database');
     define('DB_USER', 'your_username');
     define('DB_PASS', 'your_password');
     ?>
     ```

5. **Install Dependencies (if applicable):**
   - If using Composer for additional PHP packages:
     ```bash
     composer install
     ```
   - If using npm for front-end assets:
     ```bash
     npm install
     npm run build
     ```

6. **Set File Permissions:**
   - Ensure the web server has write permissions for directories like `uploads/` or `cache/`:
     ```bash
     chmod -R 775 uploads cache
     chown -R www-data:www-data uploads cache
     ```

7. **Access the Application:**
   - Open your web browser and navigate to `http://your-server/EMS`.
   - Log in with default credentials:
     - **Admin:** `username: admin`, `password: admin_password`
     - **User:** `username: user`, `password: user_password`
   - Change default passwords immediately after first login.

## Usage

1. **Logging In:**
   - Access the EMS URL and log in with your credentials.
   - Admins have access to user management and event approval features.

2. **Creating Events:**
   - Navigate to the "Create Event" section, fill in details (title, date, duration, facility, etc.), and submit for approval.
   - Admins will review and approve/deny requests.

3. **Managing Events:**
   - View ongoing, approved, pending, or archived events via the dashboard or respective sections.
   - Interact with events by liking, disliking, or commenting.

4. **User Management:**
   - Admins can edit user roles, reset passwords, or deactivate accounts from the admin panel.

5. **Calendar View:**
   - Use the interactive calendar to check event schedules and facility availability.

## Testing

EMS includes a basic test suite for core functionalities:

1. **Run Tests:**
   - If PHPUnit is set up, run:
     ```bash
     vendor/bin/phpunit tests
     ```
   - Tests cover database connectivity, event creation, and user authentication.

2. **Manual Testing:**
   - Test event creation, approval workflows, and comment systems manually through the web interface.
   - Verify responsive design on mobile and desktop browsers.

## Troubleshooting

- **Database Connection Errors:**
  - Verify credentials in `db_connection_settings.php`.
  - Ensure the database server is running and accessible.
- **404 Errors:**
  - Check web server configuration and `.htaccess` for Apache.
  - Ensure the correct document root is set.
- **Permission Issues:**
  - Confirm the web server user has write access to `uploads/` and `cache/` directories.
- **Slow Performance:**
  - Enable caching (e.g., OPCache for PHP).
  - Optimize database queries or indexes (see `database/optimization.sql` if provided).

For further assistance, contact [izeno.contact@gmail.com](mailto:izeno.contact@gmail.com) or open an issue on [GitHub](https://github.com/VoxDroid/Event-Management-System/issues).

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

## Security

Found a security vulnerability? Please report it responsibly by emailing [izeno.contact@gmail.com](mailto:izeno.contact@gmail.com). Do not disclose vulnerabilities publicly until they are resolved. See [SECURITY.md](SECURITY.md) for our security policy.

## Documentation

Additional documentation is available in the `docs/` directory or online at [GitHub Pages](#) (coming soon). Topics include:

- Web server configuration (Apache/Nginx).
- Database schema and optimization.
- API endpoints (planned).
- Developer setup for contributing.

## Demo Images

<div align="center">
  <img src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/demo_img/Demo1.png">
  <img src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/demo_img/Demo2.png">
  <img src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/demo_img/Demo3n.png">
  <img src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/demo_img/Demo4.png">
  <img src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/demo_img/Demo5.png">
  <img src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/demo_img/Demo6.png">
  <img src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/demo_img/Demo7.png">
  <img src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/demo_img/Demo8.png">
  <img src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/demo_img/Demo9.png">
  <img src="https://raw.githubusercontent.com/VoxDroid/Event-Management-System/main/assets/demo_img/Demo10.png">
</div>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

- [@VoxDroid](https://github.com/VoxDroid) - Project Lead
- [Contribute to become a listed contributor!](CONTRIBUTING.md)

## Contact

For questions, feedback, or support, reach out to:

- **Email:** [izeno.contact@gmail.com](mailto:izeno.contact@gmail.com)
- **GitHub:** [@VoxDroid](https://github.com/VoxDroid)
- **Issues:** [GitHub Issues](https://github.com/VoxDroid/Event-Management-System/issues)

---

Thank you for using EMS! We look forward to your contributions and feedback.
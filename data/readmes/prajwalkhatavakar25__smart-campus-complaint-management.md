# Smart Campus Complaint Management System

A Java-based campus complaint management application developed as an Object-Oriented Programming mini-project. The system enables students to submit campus complaints, administrators to manage and assign complaints to staff, and staff members to track and update complaint progress.

## Features

### Authentication and User Management

* **Role-based authentication:** Separate login access for students, staff, and administrators.
* **Role-specific dashboards:** Dedicated interfaces for each user role.

### Student Features

* **Complaint submission:** Submit complaints related to campus facilities and services.
* **Complaint categorization:** Organize complaints by category and priority.
* **My Complaints:** View submitted complaints, their statuses, and assigned staff.
* **Complaint history:** View recorded updates associated with submitted complaints.

### Staff Features

* **Assigned complaints:** View complaints assigned to the logged-in staff member.
* **Status management:** Update complaint statuses as work progresses.
* **Update messages:** Provide comments when changing complaint statuses.
* **Complaint history:** Maintain records of complaint status changes and associated messages.

### Administrator Features

* **Admin dashboard:** Access administrative complaint-management functions.
* **View all complaints:** View student complaints, categories, priorities, assigned staff, and statuses.
* **Staff assignment:** Assign complaints to staff members.
* **Complaint monitoring:** Review complaints and track their progress.

### Technical Features

* **MySQL integration:** Store and retrieve application data using JDBC.
* **Java Swing interface:** Graphical interfaces for students, staff, and administrators.
* **Console interface:** Console application entry point.
* **Report generation:** Report-generation functionality using Java threading.

## Complaint Workflow

1. A student logs in and submits a complaint.
2. The complaint is stored in the MySQL database.
3. The administrator reviews submitted complaints.
4. The administrator assigns a complaint to a staff member.
5. The staff member views the assigned complaint.
6. Staff members update the complaint status as work progresses.
7. Status changes and update messages are recorded in the complaint history.
8. Students and administrators can review complaint details and current statuses.

**Complaint status progression:**

`SUBMITTED → ASSIGNED → IN_PROGRESS → RESOLVED`

## Tech Stack

| Technology     | Purpose                                 |
| -------------- | --------------------------------------- |
| Java 21        | Application development                 |
| MySQL          | Relational database management          |
| JDBC           | Database connectivity                   |
| Java Swing     | Graphical user interface                |
| Eclipse IDE    | Development environment                 |
| Git and GitHub | Version control and source-code hosting |

## Project Structure

```text
SmartCampusComplaintManagement/
├── src/
│   └── com/smartcampus/cms/
│       ├── dao/
│       ├── exception/
│       ├── model/
│       ├── service/
│       ├── ui/
│       ├── util/
│       ├── Main.java
│       └── GuiMain.java
├── sql/
│   └── smart_campus_cms_schema.sql
├── docs/
│   └── screenshot/
├── .gitignore
├── .classpath
├── .project
└── README.md
```

## Prerequisites

* Java Development Kit (JDK) 21
* MySQL Server
* MySQL Connector/J
* Eclipse IDE or another compatible Java IDE
* Git

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/prajwalkhatavakar25/smart-campus-complaint-management.git
```

Import the downloaded project into Eclipse as an existing Java project.

### 2. Create the Database

Open MySQL Workbench and execute:

```text
sql/smart_campus_cms_schema.sql
```

This script creates the `smart_campus_cms` database, the required tables, and the default complaint categories.

### 3. Configure the Database Connection

| Setting  | Value                     |
| -------- | ------------------------- |
| Host     | `localhost`               |
| Port     | `3307`                    |
| Database | `smart_campus_cms`        |
| Username | Your local MySQL username |
| Password | Your local MySQL password |

If your MySQL server uses a different port, update the JDBC URL in `DBConnection.java`.

The database password is read from the `DB_Password` environment variable.

On Windows PowerShell, set the variable for the current terminal session:

```powershell
$env:DB_Password = "YOUR_LOCAL_MYSQL_PASSWORD"
```

Replace the placeholder with your local MySQL password. Never commit your actual password to GitHub.

If Eclipse is already running, ensure it can access the environment variable or configure it in the application's run configuration.

### 4. Configure MySQL Connector/J

1. Right-click the project in Eclipse.
2. Select **Build Path → Configure Build Path**.
3. Open the **Libraries** tab.
4. Select **Add External JARs**.
5. Choose your MySQL Connector/J JAR.
6. Apply the changes.

### 5. Run the Application

Run one of the following classes:

* `com.smartcampus.cms.Main` — Console application.
* `com.smartcampus.cms.GuiMain` — Java Swing application.

A running MySQL server and valid database credentials are required for database-dependent features.

## Application Screenshots

### Login Screen

![Login Screen](docs/screenshot/login.png)

### Student Dashboard

![Student Dashboard](docs/screenshot/Student_Dashboard.png)

### Complaint Submission Form

![Complaint Submission Form](docs/screenshot/Student_Complaint.png)

### Admin Dashboard

![Admin Dashboard](docs/screenshot/Admin_Dashboard.png)

### All Student Complaints

![All Student Complaints](docs/screenshot/Admin_Complaints.png)

### Assign Complaints to Staff

![Assign Complaints to Staff](docs/screenshot/Assign_Complaints.png)

### Staff Dashboard

![Staff Dashboard](docs/screenshot/Staff_Dashboard.png)

### Staff Complaint Management

![Staff Complaint Management](docs/screenshot/Staff_Complaints.png)

## Database Design

The application uses MySQL tables to store user accounts, complaint categories, complaints, and complaint updates.

* **Users:** Stores user details, roles, and department information.
* **Categories:** Stores complaint categories.
* **Complaints:** Stores complaint descriptions, locations, priorities, statuses, and staff assignments.
* **Complaint updates:** Records complaint status changes and associated messages.

The `assigned_staff_id` field links a complaint to its assigned staff member. Complaint-update records are linked to the relevant complaint and the user who made the update.

## Security Considerations

* Keep database passwords and credentials out of source code.
* Configure database credentials locally.
* Do not upload reports containing confidential or personal information.
* Use demonstration data when showcasing the application.
* Restrict administrative functionality to authorized users.
* Use secure password-storage practices.

## Future Enhancements

* Improve authentication and password security.
* Add automated unit and integration tests.
* Add complaint filtering by status, priority, category, and assigned staff.
* Introduce administrator dashboard statistics.
* Record administrator assignments in the complaint history.
* Enhance complaint reporting and export capabilities.
* Improve database configuration portability.
* Enhance the graphical interface and error handling.

---

Developed as a Java Object-Oriented Programming mini-project.

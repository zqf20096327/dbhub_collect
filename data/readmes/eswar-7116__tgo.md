# TGO - CLI Task Manager

TGO is a simple, efficient command-line task manager implemented in Go. It serves as a practical solution for managing your daily tasks directly from the terminal, using SQLite for persistent storage and providing a clean CLI interface.

## Features

- ### Task Management:
  Create, update, and delete tasks with simple commands. Each task includes a description and completion status, making it easy to track your progress.

- ### Status Tracking:
  Mark tasks as complete or incomplete with dedicated commands. Filter your task list to show only pending or completed items.

- ### Persistent Storage:
  All tasks are stored in a local SQLite database, ensuring your data persists across sessions and system restarts.

- ### Fast and Lightweight:
  Built with Go's efficiency in mind, TGO provides instant responses with minimal resource usage.

- ### Type-Safe Database Operations:
  Uses sqlc to generate type-safe Go code from SQL queries, reducing runtime errors and improving code maintainability.

- ### Modern CLI Framework:
  Powered by [Cobra](https://cobra.dev/), providing a familiar command structure with built-in help and subcommand support.

## Installation

### Using Go Install (Recommended):

```bash
go install github.com/eswar-7116/tgo@latest
```

Make sure your `$GOPATH/bin` is in your `PATH`.

### From Source:

```bash
git clone https://github.com/eswar-7116/tgo.git
cd tgo
go build -o tgo
```

## Usage

### Add a new task:

```bash
tgo add "Complete project documentation"
```

### List all tasks:

```bash
tgo list
```

### Search a task with a part of the title:

```bash
tgo list --title 'partial title'
```

### Update a task title:

```bash
tgo update <task-id> --title "Updated task description"
```

### Delete a task:

```bash
tgo rm <task-id>
```

### Clear all completed tasks:

```bash
tgo rm --all
```

### Help menu

There are many options for the `add`, `list`, `update` and `rm` commands. You can check them by adding a `-h` or `--help` flag.

For example:
```bash
tgo -h
```

```bash
tgo list -h
```

## Technology Stack

- **Go** - High-performance programming language
- **Cobra** - Modern CLI framework for building command-line applications
- **sqlc** - Generates type-safe Go code from SQL queries
- **SQLite** - Lightweight, embedded relational database

## Limitations

- ### Single User:
  TGO is designed for individual use and stores tasks locally. It does not support multi-user environments or task sharing.

- ### No Cloud Sync:
  Tasks are stored locally in a SQLite database. There is no built-in synchronization across devices or backup to cloud storage.

## Conclusion

This project is a minimal, practical CLI task manager designed to help you manage tasks efficiently from the terminal. It demonstrates core concepts of CLI application development, database integration, and clean code architecture in Go. While functional for daily use, it serves as a foundation that can be extended with additional features based on your needs.

> Submitted as a solution for https://roadmap.sh/projects/task-tracker

---
#### <div align="center">If you like this project, please give this repo a star 🌟</div>
---
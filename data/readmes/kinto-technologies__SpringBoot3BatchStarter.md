# Spring Batch 5 Starter

**Accelerate Your Spring Boot 3 Batch Development** 🚀


[![GitHub stars](https://img.shields.io/github/stars/kinto-technologies/SpringBoot3BatchStarter?style=social)](https://github.com/kinto-technologies/SpringBoot3BatchStarter/stargazers)
[![Build](https://github.com/kinto-technologies/SpringBoot3BatchStarter/actions/workflows/build.yml/badge.svg)](https://github.com/kinto-technologies/SpringBoot3BatchStarter/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/kinto-technologies/SpringBoot3BatchStarter/branch/main/graph/badge.svg)](https://codecov.io/gh/kinto-technologies/SpringBoot3BatchStarter)
![Java 21](https://img.shields.io/badge/Java-21%2B-blue)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-CC2233.svg)](https://opensource.org/licenses/Apache-2.0)

## 🌐 Language Support
🇯🇵 日本語版 README は [こちら](README.ja.md).

## 📋 Requirements
- JDK 21 (automatically downloaded by Gradle toolchain)
- Docker Desktop
- Gradle 8.5+ (not required if using gradlew)

> 💡 This project uses JDK 21, but thanks to Gradle's toolchain feature, it will be automatically downloaded even if not installed locally.

## 🔍 Overview

This comprehensive starter kit is designed specifically for Spring Boot 3 and Spring Batch 5, providing a production-ready foundation for enterprise batch processing applications. It offers two main components:

### Skeleton Batch
A minimal, ready-to-use batch application where you can:

- Start development immediately by adding your business logic
- Focus on implementation without complex configuration
- Run in any environment with H2 in-memory database

### DB and CSV Batch
A practical example implementing common batch operations:

- Export data from database to CSV with customizable queries
- Import CSV data to database with efficient bulk operations
- Demonstrate multi-database configuration best practices

Both components are built with industry best practices and utilize the latest Spring framework features to accelerate your batch development process.

## 🚀 Quick Start Guide

### 1️⃣ Try Skeleton Batch
```bash
# Clone repository
git clone https://github.com/kinto-technologies/SpringBoot3BatchStarter.git

# Build and Run
./gradlew :skeletonBatch:bootRun
```

### 2️⃣ Try DB and CSV Batch
```bash
# Start MySQL container
docker compose up -d

# Run DB to CSV export
./gradlew :dbAndCsvBatch:bootRun --args="--spring.batch.job.name=DB_TO_CSV --spring.profiles.active=local"

# Run CSV to DB import
./gradlew :dbAndCsvBatch:bootRun --args="--spring.batch.job.name=CSV_TO_DB --spring.profiles.active=local"
```

## 📁 Project Structure
```text
.
├── gradlew                # Gradle wrapper
├── settings.gradle
├── compose.yaml           # Docker Compose configuration
├── init-scripts           # Database initialization
│   ├── 1-create-table.sql
│   └── 2-insert-data.sql
├── dbAndCsvBatch          # DB-CSV batch project
│   ├── README.md
│   ├── build.gradle
│   └── src/
└── skeletonBatch          # Skeleton batch project
    ├── README.md
    ├── build.gradle
    └── src/
```

## 💡 Core Features

### 🏗️ Foundation Components
- **Production-Ready Batch Framework**:
    - Pre-configured skeleton structure
    - Ready for immediate development
    - H2 in-memory database for simple setup

### 🔄 Data Operations
- **DB to CSV Export**:
    - Dynamic query support
    - Configurable data extraction
- **CSV to DB Import**:
    - Bulk insert operations
    - High-performance data loading

### 🛠️ Technical Stack
- **Spring Integration**:
    - Spring Batch job/step management
    - Type-safe SQL with jOOQ
    - CSV processing with OpenCSV
- **Dual Database Setup**:
    - H2 for batch metadata
    - MySQL for business data

### 💻 Development Tools
- **Dynamic Configuration**:
    - Environment profiles (local/server)
    - Runtime job configuration
    - Customizable queries
- **Development Support**:
    - Hot reload support
    - Debug configuration
    - IDE integration

### 🔍 Quality Assurance
- **Code Quality**:
    - Google Java Format (Spotless)
    - Static analysis (SpotBugs)
    - Test coverage (Jacoco)
- **CI Pipeline**:
    - GitHub Actions integration
    - Automated testing
    - Quality gates

## ❓ Troubleshooting

### Entity Classes Not Found
- **Cause**: jOOQ auto-generation not executed
- **Solution**: Run `../gradlew generateJooq`
- **Alternative**: Copy from `build/generated-src/jooq` to `src/main/java`

### Database Connection Error
- **Cause**: MySQL container not running
- **Solution**: Run `docker compose up -d`
- **Verify**: Check with `docker ps`

### Multiple Jobs Error
- **Symptom**: "Job name must be specified" error
- **Cause**: Job name required when multiple jobs exist
- **Solution**: Add `--spring.batch.job.name=DB_TO_CSV`

## 🔄 Continuous Integration

### GitHub Actions
- Automated build and test
- Code formatting check
- Static analysis
- Coverage measurement

### Codecov
- Coverage visualization
- Automatic PR reports
- Change tracking

### Workflow
1. Triggers on push/pull request
2. Sets up MySQL container
3. Configures JDK 21
4. Runs Gradle build and tests
5. Uploads coverage reports

## 📌 Version Information
- Spring Boot: 3.4.1
- Spring Dependency Management: 1.1.7
- Spotless (Google Java Format): 6.22.0
- jOOQ: 9.0
- OpenCSV: 5.9
- SpotBugs: 6.0.27

## 📜 License
Licensed under the **[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)**.

Copyright © 2024 KINTO Technologies Corporation

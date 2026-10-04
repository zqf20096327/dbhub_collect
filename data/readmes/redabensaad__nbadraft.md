![Java](https://img.shields.io/badge/Java-21-orange)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.4.5-brightgreen)
![Maven](https://img.shields.io/badge/Maven-4.x-blue)
![Jsoup](https://img.shields.io/badge/Jsoup-HTML_Parsing-green)
![Jackson](https://img.shields.io/badge/Jackson-JSON_Processing-black)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue)
![Swagger](https://img.shields.io/badge/Swagger-OpenAPI_3-85EA2D)
![Angular](https://img.shields.io/badge/Angular-19+-dd0031)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue)
![Angular_Material](https://img.shields.io/badge/Angular_Material-UI_Framework-1976D2)
![Nginx](https://img.shields.io/badge/Nginx-Reverse_Proxy-009639)
![Docker](https://img.shields.io/badge/Docker-Container-2496ed)

# NBADraft • Fullstack NBA Expansion Draft Platform (Spring Boot 3 + Angular 19)

NBA Expansion Draft simulation platform combining automated data collection, REST APIs, and modern frontend visualization.

The project allows users to explore NBA players, analyze contracts, manage salary cap constraints, and simulate expansion draft scenarios using real-world data gathered through a custom scraping engine.

This repository is organized as a monorepo containing the backend API, frontend application, and NBA data acquisition pipeline.

## ✨ Key Features

* Automated NBA player and contract data collection
* NBA Expansion Draft simulation
* Salary Cap management and validation
* Player statistics visualization
* Team and roster exploration
* Interactive dashboards and analytics
* RESTful API architecture
* OpenAPI / Swagger documentation
* Modern Angular user experience
* Centralized data ingestion and synchronization

## 🏀 Core Modules

### Frontend Application

* Interactive NBA dashboards
* Expansion Draft simulation workflows
* Salary Cap calculations
* Player and contract exploration
* Responsive Angular Material interface

### Backend API

* NBA player management
* Team and roster management
* Contract management
* Data synchronization engine
* REST API exposure

### Data Scraper

* Basketball-Reference scraping
* ESPN hidden API integration
* Player headshot collection
* Team logo collection
* Automated JSON dataset generation

## 🏗️ Architecture

### Data Acquisition Layer

The scraper gathers player statistics, contracts, headshots, and team assets from multiple sources and transforms them into structured JSON datasets.

### Backend Layer

Spring Boot API exposing NBA data through REST endpoints while managing persistence, synchronization, and business rules.

### Frontend Layer

Angular application responsible for data visualization, roster management, and expansion draft simulations.

### Deployment Layer

Containerized architecture designed for deployment using Docker and Nginx.

## 🛠️ Technologies Used

### Backend

* Java 21
* Spring Boot 3
* Spring Data JPA
* MySQL
* Swagger / OpenAPI
* Lombok

### Frontend

* Angular 19
* Angular Signals
* Angular Standalone Components
* Angular Material
* TypeScript
* RxJS

### Scraping & Data Processing

* Java Records
* Jsoup
* Jackson
* JSON Data Pipelines

### DevOps

* Docker
* Nginx

## 📊 Data Sources

The platform combines information from multiple public NBA-related sources, including:

* Player statistics
* Team information
* Contract details
* Player headshots
* Team branding assets

All collected data is transformed into structured datasets consumed by the backend API.

## 🎯 Project Goals

* Simulate the NBA Expansion Draft process
* Provide realistic roster-building scenarios
* Analyze contracts and salary cap implications
* Centralize NBA player information
* Demonstrate modern full-stack and data engineering practices

## 🚀 Future Enhancements

* User authentication and profiles
* Saved draft simulations
* Advanced player comparison tools
* Predictive analytics
* Historical draft scenarios
* Multi-season simulations
* AI-assisted roster recommendations

## 📦 Project Status

**Active Development**

NBADraft is currently under active development, with ongoing improvements focused on data quality, business rules, simulation capabilities, user experience, and long-term maintainability.

The project serves as a complete showcase of data acquisition, backend engineering, API design, and modern Angular frontend development within a sports analytics domain.

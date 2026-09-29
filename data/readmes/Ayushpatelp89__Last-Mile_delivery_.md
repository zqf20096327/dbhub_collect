# Last-Mile Route Planning from Delivery Centers

A smart logistics and delivery route planning web application built with Laravel 12. This system helps delivery companies optimize last-mile delivery routes from delivery hubs to customer locations using a nearest-neighbor TSP heuristic and interactive Leaflet maps.

---

## 📂 Folder Structure Explanation

Standard Laravel 12 directory structure with the following key additions:

- **`app/Models/`**: Contains Eloquent models (`DeliveryCenter`, `Vehicle`, `Driver`, `Order`, `Route`, `RouteStop`).
- **`app/Http/Controllers/`**: Contains core logic, notably `RoutePlanningController` and CRUD controllers.
- **`app/Services/`**: Contains `RouteOptimizationService.php` which holds the algorithm for route calculation based on Haversine distance.
- **`database/migrations/`**: Database schemas defining foreign key constraints for the logistics network.
- **`database/seeders/DatabaseSeeder.php`**: Contains dummy locations and logistics data for testing.
- **`resources/views/`**: Contains Bootstrap 5 blade templates.
  - `layouts/app.blade.php`: The main layout with the sidebar.
  - `route-planning/`: Views for generating routes and displaying them on an interactive map.

---

## 🚀 Commands to Run the Project

Follow these steps to set up and run the project locally (XAMPP/WAMP or Laravel Herd/Valet).

1. **Navigate to project directory:**
   ```bash
   cd last-mile-delivery
   ```

2. **Install PHP Dependencies:**
   ```bash
   composer install
   ```

3. **Install NPM Dependencies & Build Assets:**
   ```bash
   npm install
   npm run build
   ```

4. **Environment Setup:**
   - Rename `.env.example` to `.env` (already done by composer create-project).
   - Generate app key if missing: `php artisan key:generate`
   - **For XAMPP / MySQL:** Change the DB configuration in `.env`:
     ```env
     DB_CONNECTION=mysql
     DB_HOST=127.0.0.1
     DB_PORT=3306
     DB_DATABASE=last_mile_delivery
     DB_USERNAME=root
     DB_PASSWORD=
     ```

5. **Run Migrations & Seeders:**
   *(Make sure your database server is running and the database is created if using MySQL)*
   ```bash
   php artisan migrate:fresh --seed
   ```

6. **Start the Laravel Development Server:**
   ```bash
   php artisan serve
   ```

7. **Access the Application:**
   Open `http://localhost:8000` in your browser.
   - **Login:** `admin@example.com`
   - **Password:** `password`

---

## 📊 Sample Dummy Data

The `DatabaseSeeder` automatically populates the system with:
- **1 Delivery Center:** Downtown Hub (Metro City)
- **1 Vehicle:** VAN-001 (Diesel, Capacity 1000kg)
- **1 Driver:** John Doe (Assigned to VAN-001)
- **2 Orders:** Pending deliveries with coordinates in the Metro City area.

---

## 📸 Screenshots Ideas for Documentation

If you are presenting this project, capture these screens:
1. **Login Page:** Standard secure authentication screen.
2. **Dashboard Overview:** Show the stats cards (Total Centers, Pending Orders) and the live map with markers.
3. **Delivery Centers Index:** Show the data table listing the hubs.
4. **Plan New Route:** Show the dropdowns selecting the hub and driver.
5. **Optimized Route Overview (Core Feature):** Capture the interactive Leaflet map displaying the generated route (Polyline) connecting the delivery stops sequentially.

---

## 🎓 Viva Questions and Answers

**Q1: What is the main objective of this application?**
**A1:** To optimize last-mile delivery routes from distribution centers to customer locations, minimizing travel distance, fuel usage, and delivery time.

**Q2: Which algorithm is used for route optimization in this project?**
**A2:** The project uses a Nearest-Neighbor heuristic based on the Traveling Salesperson Problem (TSP). It calculates the Haversine distance between coordinates and selects the closest unvisited stop iteratively.

**Q3: How are maps integrated into the application?**
**A3:** Maps are integrated using Leaflet JS, an open-source JavaScript library, rendering OpenStreetMap tiles. This avoids the need for paid Google Maps API keys during development.

**Q4: Explain the relationships in your database schema.**
**A4:** 
- A `Vehicle` `hasOne` `Driver`.
- A `DeliveryCenter` `hasMany` `Orders`.
- A `Route` `belongsTo` a `Driver` and `Vehicle`, and `hasMany` `RouteStops`.
- A `RouteStop` is a pivot/association that links a `Route` to an `Order`.

**Q5: What architecture pattern does Laravel follow?**
**A5:** MVC (Model-View-Controller). The Models interact with the database, Views display the UI using Blade, and Controllers handle the business logic and requests.

---

## 📄 Mini Project Report Summary

### 1. Introduction
The Last-Mile Route Planning System is a web-based logistics application developed to automate and optimize delivery dispatch operations. In urban logistics, the "last mile" represents the most expensive and time-consuming part of the supply chain. This project aims to mitigate these inefficiencies.

### 2. Technology Stack
- **Backend:** PHP 8.3, Laravel 12 Framework
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript, Leaflet Maps
- **Database:** MySQL / SQLite
- **Architecture:** MVC Pattern, Service Repository Pattern for optimization logic.

### 3. Core Modules Developed
- **Authentication & Authorization:** Secure login system.
- **Entity Management (CRUD):** Complete management of Delivery Centers, Vehicles, Drivers, and Orders.
- **Route Engine:** A custom optimization service that processes geo-coordinates (latitude/longitude) using the Haversine formula to generate the shortest sequential path.
- **Interactive Map:** Real-time visualization of hubs, delivery stops, and polyline routes.

### 4. Conclusion
The application successfully demonstrates a scalable approach to logistics management. By separating complex algorithmic logic into a Service class and providing a clean, responsive admin dashboard, it lays the groundwork for a production-ready SaaS logistics product. Future scope could include real-time GPS tracking and live traffic-aware routing using premium APIs.

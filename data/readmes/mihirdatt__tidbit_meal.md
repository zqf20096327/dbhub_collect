# Tidbit Meal 🍱

A full-stack web platform connecting **home cooks (food providers)** offering homemade tiffin services with **customers** looking to order home-style meals. Built with PHP and MySQL, it supports dual user roles, tiffin browsing, cart management, and cash-on-delivery checkout.

## Features

### Customer
- Sign up / log in as a customer
- Browse home food providers and their tiffin/dish listings
- Add tiffins to a session-based cart
- Checkout with order summary and cash-on-delivery payment
- View order history and track past orders
- Edit profile details

### Food Provider (Home Cook)
- Separate sign up / log in for food providers
- Dedicated admin panel to manage listed tiffins/dishes
- View and manage incoming customer orders

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | PHP |
| Database | MySQL |
| Frontend | HTML, CSS, SCSS, JavaScript |
| Styling/UI | Bootstrap, custom SCSS, Font Awesome |
| JS Libraries | jQuery, Isotope, Animsition, Headroom.js |

## Project Structure

```
tidbit_meal/
├── Foodprovider_panel/   # Home cook dashboard & tiffin/order management
├── Fp_img/                # Food provider images
├── SQL/                   # Database schema
├── admin/                 # Admin panel
├── connection/            # Database connection config
├── css/                   # Compiled stylesheets
├── scss/                  # SCSS source files
├── js/                    # JavaScript libraries & custom scripts
├── icons/                 # Flag icons, etc.
├── images/ images2/       # Static assets
├── checkout.php           # Cart summary & order placement
├── dishes.php             # Tiffin/dish listings
├── restaurants.php        # Food provider (home cook) listings
├── login_customer.php     # Customer login
├── registration_customer.php
├── registration_fp.php    # Food provider registration
├── edit_customer.php      # Profile editing
├── your_orders.php        # Customer order history
├── view_order.php
├── delete_orders.php
├── product-action.php     # Cart/session logic
├── logout.php
└── index.php              # Landing page
```

## Getting Started

### Prerequisites
- A local server stack with PHP and MySQL (e.g. [XAMPP](https://www.apachefriends.org/) or [WAMP](https://www.wampserver.com/))
- A web browser

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mihirdatt/tidbit_meal.git
   ```

2. **Move the project into your server's web root**
   - For XAMPP: copy the folder into `htdocs/`
   - For WAMP: copy the folder into `www/`

3. **Create the database**
   - Open phpMyAdmin (or your preferred MySQL client)
   - Create a new database
   - Import the schema/SQL file(s) from the `SQL/` folder

4. **Configure the database connection**
   - Open `connection/connect.php`
   - Update the host, username, password, and database name to match your local MySQL setup

5. **Run the app**
   - Start Apache and MySQL via your server stack's control panel
   - Visit `http://localhost/tidbit_meal/index.php` in your browser

## Known Limitations / Roadmap

This project was built as a learning exercise and has a few areas worth improving before production use:

- [ ] Replace raw, concatenated SQL queries with prepared statements (mysqli/PDO) to prevent SQL injection
- [ ] Add server-side input validation and sanitization across forms
- [ ] Re-enable and handle PHP error reporting instead of suppressing it
- [ ] Add password hashing (if not already implemented) for stored credentials
- [ ] Add a proper online payment option alongside cash-on-delivery

## License

This project currently has no license specified. Feel free to fork and build on it for learning purposes.

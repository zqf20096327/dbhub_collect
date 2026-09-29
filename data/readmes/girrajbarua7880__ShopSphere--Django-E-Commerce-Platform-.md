# 🛍️ ShopSphere — Django E-Commerce Platform

> A full-stack e-commerce web application built with **Python and Django**, featuring product discovery, authentication, favorites, cart management, checkout, Razorpay payments, order management, user profiles, and Django Admin.

[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge)](https://shopsphere-ln4m.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/girrajbarua7880/ShopSphere--Django-E-Commerce-Platform-)
[![Django](https://img.shields.io/badge/Django-5.2.17-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)

---

## 🌐 Live Demo

### 🚀 Live Application
**[Open ShopSphere →](https://shopsphere-ln4m.onrender.com/)**

### 🛒 Product Listing
**[Browse Products →](https://shopsphere-ln4m.onrender.com/products/)**

### 💻 Source Code
**[View GitHub Repository →](https://github.com/girrajbarua7880/ShopSphere--Django-E-Commerce-Platform-)**

> **Note:** The Render service may take a little longer to respond after being idle.

---

# 📸 Application Preview

> **Recommended:** Add screenshots of the actual ShopSphere website UI to `docs/`.  
> The paths below are ready for your screenshots. You only need to replace the image files; the Markdown does not need to change.

## 🏠 Home Page

![ShopSphere Home Page](doc/hero.png)

The home page introduces the store, featured products, categories, and main shopping navigation.

---

## 🛍️ Products & Search

![ShopSphere Products Page](doc/products.png)

The product listing page allows customers to browse products, search by name or description, and filter products by category.

---

## 📦 Product Details

![ShopSphere Product Details](doc/productdetailS.png)

The product detail page displays product information, pricing, discount information, stock availability, favorites, add-to-cart functionality, and related products.

---

## 🔐 Login

![ShopSphere Login](doc/login.png)

Customers can log in using their email address or phone number and password.

---

## 📝 Registration

![ShopSphere Signup](doc/signup.png)

New customers can create an account using an email address or phone number.

---

## ❤️ Favorites

![ShopSphere Favorites](doc/fav.png)

Authenticated customers can save products for later and manage their favorite products.

---

## 🛒 Shopping Cart

![ShopSphere Shopping Cart](doc/cart.png)

The cart provides product quantities, item removal, stock-aware quantity updates, and the calculated cart total.

---

## 💳 Checkout

![ShopSphere Checkout](doc/checkout.png)
![ShopSphere Checkout](doc/checkout2.png)

Customers enter shipping information and choose between Cash on Delivery and Razorpay online payment.

---

## 💰 Razorpay Payment

![ShopSphere Razorpay Payment](doc/razorpay.png)

ShopSphere supports online payments through Razorpay.

---

## ✅ Order Success

![ShopSphere Order Success](doc/order-success.png)

After successful order processing, customers receive an order confirmation page.

---

## 📋 My Orders

![ShopSphere My Orders](doc/my-orders.png)

Customers can view their previous orders along with order and payment information.

---

## 👤 Profile

![ShopSphere Profile](doc/profile.png)

Customers can manage their name, phone number, avatar, address, city, and postal code.

---

## ⚙️ Django Admin — Products

![ShopSphere Admin Products](doc/product.png)

Administrators can manage products, categories, pricing, discounts, stock, and product information.

---


# ✨ Features

## 🛍️ Product Catalog
- Product listing
- Product detail pages
- Product search
- Category filtering
- Discount pricing
- Stock availability
- Related products

## 👤 Authentication
- User registration
- Login with email or phone
- Django authentication
- Password validation
- Logout
- Protected user pages

## ❤️ Favorites
- Add/remove favorites
- User-specific favorites
- Favorite state on products
- Duplicate favorites prevented with database constraints

## 🛒 Shopping Cart
- Persistent user-specific cart
- Add products
- Increase/decrease quantity
- Remove items
- Automatic cart total
- Stock validation

## 💳 Checkout & Payments
- Shipping information
- Cash on Delivery
- Razorpay online payment
- Payment verification
- Order confirmation
- Payment status tracking

## 📦 Orders
- Order creation
- Order history
- Order items
- Payment status
- Order status
- Inventory validation
- Razorpay transaction IDs

## 👤 User Profile
- First name and last name
- Phone number
- Profile avatar
- Address
- City
- Postal code

## ⚙️ Django Admin
- Category management
- Product management
- Cart management
- Order management
- Favorite management
- Search and filters
- Inline order/cart items

---

# 🧰 Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Backend | Django 5.2.17 |
| Database | TiDB Cloud / MySQL-compatible backend |
| ORM | Django ORM |
| Frontend | Django Templates, HTML, CSS, JavaScript |
| Authentication | Django Authentication System |
| Payment | Razorpay |
| Production Server | Gunicorn |
| Static Files | WhiteNoise |
| Deployment | Render |
| Environment | python-dotenv / Environment Variables |
| Image Processing | Pillow |
| Database Driver | PyMySQL |

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │       Browser        │
                         │    HTML / CSS / JS   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Django URLs      │
                         │     URL Routing      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │        Views         │
                         │   Business Logic     │
                         └──────────┬───────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     ▼                             ▼
             ┌─────────────────┐          ┌─────────────────┐
             │  Django Forms   │          │   Django ORM    │
             │   Validation    │          │ Database Layer  │
             └─────────────────┘          └────────┬────────┘
                                                    │
                                                    ▼
                                           ┌─────────────────┐
                                           │   TiDB Cloud     │
                                           │ MySQL Compatible │
                                           └─────────────────┘

                                    │
                                    ▼
                              ┌─────────────┐
                              │  Razorpay   │
                              │   Payment   │
                              └─────────────┘
```

ShopSphere follows Django's **MVT (Model–View–Template)** architecture.

---

# 📁 Project Structure

```text
ShopSphere/
│
├── manage.py
├── requirements.txt
├── build.sh
├── ca.pem
├── .env.example
├── .gitignore
├── README.md
│
├── docs/
│   └── screenshots/
│       ├── home.png
│       ├── products.png
│       ├── product-detail.png
│       ├── login.png
│       ├── signup.png
│       ├── favorites.png
│       ├── cart.png
│       ├── checkout.png
│       ├── razorpay.png
│       ├── order-success.png
│       ├── my-orders.png
│       ├── profile.png
│       ├── admin-products.png
│       ├── admin-orders.png
│       └── mobile.png
│
├── shopsphere/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── store/
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    ├── static/
    └── templates/
```

---

# 🗄️ Database Design

## Main Relationships

```text
Category
   │
   └── Product
          │
          ├── CartItem
          ├── Favorite
          └── OrderItem

User
 ├── Profile
 ├── Cart
 │    └── CartItem
 ├── Favorite
 └── Order
      └── OrderItem
```

## Category

```text
id
name
slug
```

`name` and `slug` are unique.

## Product

```text
id
category
name
slug
description
price
discount_price
stock
image
created_at
updated_at
```

The `current_price` property uses the discount price when available; otherwise it uses the original price.

## Cart

```text
User
 │
 └── Cart
      └── CartItem
             └── Product
```

A unique cart/product constraint prevents duplicate cart items.

## Favorite

```text
User
 │
 └── Favorite
        └── Product
```

A unique user/product constraint prevents duplicate favorites.

## Order

```text
Order
 │
 └── OrderItem
        └── Product
```

`OrderItem` stores the product name and price at the time of purchase so historical orders remain consistent if product data changes later.

---

# 💳 Payment Flow

```text
Customer
   │
   ▼
Cart
   │
   ▼
Checkout
   │
   ├── COD ────────────────┐
   │                       │
   └── Razorpay ──► Payment
                           │
                           ▼
                       Order Created
                           │
                           ▼
                       Fulfillment
```

Razorpay configuration:

```env
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
```

Payment-related routes:

```text
/place-order/
/verify-payment/
/order-success/<order_id>/
```

---

# 📦 Inventory & Order Fulfillment

The application validates stock during cart and order operations.

Critical fulfillment logic uses:

```python
select_for_update()
```

This provides row-level locking during inventory-sensitive operations and helps prevent inconsistent stock updates during concurrent transactions.

Successful fulfillment results in:

```text
Payment Status → PAID
Order Status   → PROCESSING
```

---

# 🔗 URL Reference

| URL | Purpose | Authentication |
|---|---|---|
| `/` | Home | Public |
| `/products/` | Product listing | Public |
| `/products/<slug>/` | Product detail | Public |
| `/products/<slug>/add-to-cart/` | Add product to cart | Required |
| `/favorites/` | Favorites | Required |
| `/favorites/toggle/<slug>/` | Toggle favorite | Required |
| `/cart/` | Shopping cart | Required |
| `/cart/update/<id>/` | Update cart item | Required |
| `/cart/remove/<id>/` | Remove cart item | Required |
| `/signup/` | Registration | Public |
| `/login/` | Login | Public |
| `/logout/` | Logout | Required |
| `/profile/` | User profile | Required |
| `/checkout/` | Checkout | Required |
| `/place-order/` | Create order | Required |
| `/verify-payment/` | Payment verification | Required |
| `/order-success/<id>/` | Order success | Required |
| `/my-orders/` | Customer orders | Required |
| `/admin/` | Django administration | Staff/Admin |

---

# 🔐 Security

The project uses Django security mechanisms including:

- Password hashing
- CSRF protection
- Authentication middleware
- `@login_required` protected views
- Password validation
- Database transactions
- Environment-based configuration

> Never commit database passwords, Django secret keys, or Razorpay secret keys to GitHub.

---

# ⚡ Performance

Current implementation includes:

- `select_related()` for suitable foreign-key relationships
- `prefetch_related()` for related collections
- Database unique constraints
- Transaction handling
- `select_for_update()` for inventory-sensitive operations

---

# 🚀 Deployment

ShopSphere is configured for **Render** deployment.

```text
Render
  │
  ▼
Install Dependencies
  │
  ▼
collectstatic
  │
  ▼
migrate
  │
  ▼
Gunicorn
  │
  ▼
Django Application
  │
  ├── TiDB Cloud
  └── Razorpay
```

### Build Script

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### Start Command

```bash
gunicorn shopsphere.wsgi:application
```

---

# 🗃️ Environment Configuration

Example `.env`:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

TIDB_DB_NAME=your-database
TIDB_USER=your-user
TIDB_PASSWORD=your-password
TIDB_HOST=your-host
TIDB_PORT=4000

RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
```

For production, use hosting-provider environment variables and set:

```env
DJANGO_DEBUG=False
```

---

# 💻 Installation

## 1. Clone Repository

```bash
git clone https://github.com/girrajbarua7880/ShopSphere--Django-E-Commerce-Platform-.git
cd ShopSphere--Django-E-Commerce-Platform-
```

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

## 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

## 4. Configure Environment

Create `.env` and add the required database and Razorpay variables.

## 5. Run Migrations

```powershell
python manage.py migrate
```

## 6. Create Admin User

```powershell
python manage.py createsuperuser
```

## 7. Run Development Server

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🔮 Future Improvements

- Automated unit and integration tests
- Production object storage for uploaded media
- Transactional email service
- Django REST Framework API
- React/mobile frontend
- Redis caching
- Background task processing
- Monitoring and logging
- Advanced analytics

---

# 🏆 Project Highlights

```text
✓ Full-stack Django application
✓ Django MVT architecture
✓ TiDB Cloud integration
✓ Relational database design
✓ Email / phone authentication
✓ Product search
✓ Category filtering
✓ Favorites
✓ Persistent shopping cart
✓ Stock validation
✓ Checkout
✓ Cash on Delivery
✓ Razorpay payments
✓ Payment verification
✓ Order management
✓ User profiles
✓ Django Admin
✓ Database transactions
✓ Inventory row locking
✓ Render deployment
✓ Gunicorn
✓ WhiteNoise
✓ Environment-based configuration
```

---

# 🎯 Interview Explanation

> **ShopSphere is a full-stack Django e-commerce platform that I developed to implement a complete online shopping workflow. It includes product catalog management, category filtering, email/phone authentication, favorites, persistent shopping carts, checkout, Cash on Delivery, Razorpay payments, order management, stock validation, user profiles, and Django Admin. The application uses Django ORM with a MySQL-compatible TiDB Cloud database and is deployed on Render using Gunicorn and WhiteNoise.**

---

# 📄 Resume Description

**ShopSphere — Django E-Commerce Platform**

Developed and deployed a full-stack e-commerce platform using **Python and Django**, featuring product catalog, category filtering, authentication, favorites, shopping cart, checkout, Razorpay payments, order management, inventory validation, user profiles, and Django Admin. Integrated **TiDB Cloud** through Django's MySQL-compatible backend and deployed the application on **Render** using Gunicorn and WhiteNoise.

---

# 🌐 Project Links

| Resource | Link |
|---|---|
| 🌐 Live Application | [ShopSphere](https://shopsphere-ln4m.onrender.com/) |
| 🛒 Products | [Browse Products](https://shopsphere-ln4m.onrender.com/products/) |
| 💻 GitHub Repository | [ShopSphere GitHub](https://github.com/girrajbarua7880/ShopSphere--Django-E-Commerce-Platform-) |

---

## ⭐ Like the Project?

**[🌐 Try ShopSphere Live](https://shopsphere-ln4m.onrender.com/)** · **[💻 View Source Code](https://github.com/girrajbarua7880/ShopSphere--Django-E-Commerce-Platform-)**

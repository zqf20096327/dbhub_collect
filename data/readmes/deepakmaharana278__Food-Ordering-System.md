# 🍽️ Food Ordering System

A full-stack **Food Ordering System** built using **React (Frontend)** and **Django REST Framework (Backend)**.  
This application enables users to browse food items, filter and sort products, manage cart and wishlist, place orders using cash or card payment, and submit reviews.  
A **custom admin dashboard** provides sales analytics, order management, and review moderation.

The backend exposes RESTful APIs consumed by the React frontend.

---

## 🔗 Live Demo

Check out the site live here:  
[Deepak-Taste-Ride](https://food-ordering-system-1-mfnt.onrender.com) 

## 📌 Tech Stack

### 🔹 Frontend
- React.js
- Bootstrap 5
- Axios
- React Router DOM

### 🔹 Backend
- Django
- Django REST Framework
- SQLite Database
- Supabase Object Storage (for media files)
- Django REST Framework (DRF)
- SQLite
- django-cors-headers

---

## 🧩 Project Architecture
```bash
Food-Ordering-System/
│
├── backend/
│ ├── backend/
│ ├── foodordering/
│ ├── manage.py
│ ├── requirements.txt
│
├── frontend/
│ ├── src/
│ ├── public/
│ ├── package.json
│
└── README.md

```


---

## ✨ Features

### 👤 User Features
- User Registration & Login (JWT / Session-based)
- View food items with images
- Search food items
- Filter by category
- Price range filtering
- Sort by price / relevance
- **Wishlist**
  - Add items to wishlist
  - Remove items from wishlist
- **Cart Management**
  - Add to cart
  - Remove from cart
  - Update item quantity
- **Checkout & Payment**
  - Cash on Delivery (COD)
  - Card payment (gateway-ready)
- Place orders
- View order history and Track
- Submit food reviews & ratings
- Fully responsive UI (Mobile / Tablet / Desktop)

---

### 🛠️ Admin Dashboard Features (Custom)

#### 📊 Sales & Analytics
- Today’s sales
- Monthly sales
- Total revenue
- Total orders count

#### 🍔 Product Management
- Add new food items
- Update food details
- Delete food items
- Manage food categories
- Upload food images

#### 🧾 Order Management
- View all orders
- Update order status (Pending / Delivered / Cancelled)
- Filter orders by date

#### ⭐ Review Management
- View customer reviews
- Approve or reject reviews
- Delete inappropriate reviews

#### 👥 User Management
- View registered users
- Monitor user activity

---

## 🔗 API Endpoints (Sample)

| Method | Endpoint | Description |
|------|------------------------|----------------------------|
| GET  | `/api/foods/`          | Get all food items         |
| GET  | `/api/categories/`     | Get all categories         |
| POST | `/api/login/`          | User login                 |
| POST | `/api/register/`       | User registration          |
| POST | `/api/cart/add/`       | Add item to cart           |
| GET  | `/api/cart/`           | View cart                  |
| POST | `/api/wishlist/add/`   | Add item to wishlist       |
| GET  | `/api/wishlist/`       | View wishlist              |
| POST | `/api/order/`          | Place order                |
| POST | `/api/payment/cod/`    | Cash on Delivery payment   |
| POST | `/api/payment/card/`   | Card payment               |
| GET  | `/api/admin/sales/today/`   | Today sales report     |
| GET  | `/api/admin/sales/monthly/` | Monthly sales report   |
| GET  | `/api/admin/reviews/`       | Manage reviews         |

---

## ⚙️ Backend Setup (Django)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/deepakmaharana278/Food-Ordering-System.git
cd Food-Ordering-System/backend

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
Backend will run at: http://127.0.0.1:8000/
```

### 2️⃣ Configure Supabase Storage (Optional)
For production deployment, configure Supabase object storage for media files:

1. Create a Supabase account and project at [supabase.com](https://supabase.com)
2. Create a storage bucket named `food-images` (set as public)
3. Copy your project credentials from Settings → API
4. Update the `.env` file in the backend directory with your Supabase credentials:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co/storage/v1/s3
   SUPABASE_ACCESS_KEY=your-anon-key
   SUPABASE_SECRET_KEY=your-service-role-key
   SUPABASE_BUCKET_NAME=food-images
   SUPABASE_PROJECT_ID=your-project-id
   SUPABASE_REGION=us-east-1
   ```
5. See `SUPABASE_SETUP.md` for detailed instructions

```markdown
## ⚛️ Frontend Setup (React)
```bash
cd frontend
npm install
npm start
Frontend will run at: http://localhost:3000/
```

# 👨‍💻 Author

**Deepak Maharana**

- 📧 Email: deepakmaharana3500@gmail.com  
- 💼 LinkedIn: https://www.linkedin.com/in/deepak-maharana-3a7728325  
- 🌐 Portfolio: https://my-portfolio-chi-nine-4vbjyr31n2.vercel.app/  
- 🐙 GitHub: https://github.com/deepakmaharana278

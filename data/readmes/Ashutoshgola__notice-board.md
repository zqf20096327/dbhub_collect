# Notice Board

A simple Notice Board application built using Next.js, Prisma and MySQL (TiDB Cloud). It allows users to create, view, edit and delete notices.

## Tech Stack

- Next.js (Pages Router)
- React
- Prisma
- MySQL (TiDB Cloud)
- Tailwind CSS
- Vercel

## Features

- Create a new notice
- View all notices
- Edit a notice
- Delete a notice with confirmation
- Responsive design
- Server-side validation
- Urgent notices are shown before normal notices

## Run Locally

1. Clone the repository

```bash
git clone https://github.com/Ashutoshgola/notice-board.git
cd notice-board
```

2. Install dependencies

```bash
npm install
```

3. Create a `.env` file and add your database URL

```env
DATABASE_URL="your_database_url"
```

4. Generate Prisma Client

```bash
npx prisma generate
```

5. Run database migrations

```bash
npx prisma migrate dev
```

6. Start the development server

```bash
npm run dev
```

Open:

```
http://localhost:3000
```

## What I would improve

If I had more time, I would add image upload for notices and improve the UI with better notifications and search functionality also I will add search and paging option for the notice

## AI Usage
I used AI as a development assistant during this assignment. It helped me with:

- Setting up Prisma and connecting it to the database
- Understanding the project structure and folder organization
- Fixing errors during development and debugging
- Learning how to use Next.js API Routes and Prisma
- Improving the UI design and reusable components
- Writing the README file

## 👨‍💻 Author

Ashutosh Gola

GitHub: https://github.com/Ashutoshgola/notice-board
Live URL: https://notice-board-tawny.vercel.app/
LinkedIn: https://www.linkedin.com/in/ashutoshgola91/

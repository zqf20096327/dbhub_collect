# Instaclone Pro

A full-featured Instagram-inspired social app built with React, Node.js, and TiDB.

## Features
- Authentication and protected routes
- User profile and follow system
- Feed, posts, likes, comments, bookmarks
- Reels with comments and likes
- Stories with expiration
- Direct messages and online presence
- Notifications
- Explore / search / trending tags
- Responsive UI

## Stack
- Frontend: React + Vite + Tailwind CSS
- Backend: Node.js + Express
- Database: TiDB (MySQL-compatible)
- Realtime: Socket.IO

## Local setup

1. Clone the repository
2. Create a `.env` file in `backend` with your TiDB config.
3. Install dependencies:

```bash
npm install --workspaces
```

4. Start backend:

```bash
npm run dev:backend
```

5. Start frontend:

```bash
npm run dev:frontend
```

## Backend env example

```env
PORT=5000
JWT_SECRET=supersecretjwtkey
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USER=root
TIDB_PASSWORD=password
TIDB_DATABASE=instaclone
TIDB_SSL=false
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Database setup

Import the schema file:

```bash
mysql -h 127.0.0.1 -P 4000 -u root -p < backend/sql/schema.sql
```

## Notes
This is a starter project intended to be cloned, customized, and extended for your own product.

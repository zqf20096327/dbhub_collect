# Portfolio Real-time Chat

Real-time chat widget for my portfolio site, built with React, Node.js, Socket.io and MySQL. Visitors can message me directly from the site; I reply live from a password-protected admin inbox.

## Features

- Floating chat widget on the portfolio
- Live admin inbox at `/admin`
- Typing indicators, online/away status, unread badges
- Chat history saved in MySQL
- Optional email alerts when a visitor messages while I'm offline

## Tech stack

- **Client:** React (Vite), Socket.io-client
- **Server:** Node.js, Express, Socket.io
- **Database:** MySQL

## Structure
portfolio-chat/
├── server/ Node.js + Express + Socket.io + MySQL
└── client/ React (Vite): ChatWidget + AdminPanel


## Setup

1. Import `server/schema.sql` into MySQL
2. `cd server && npm install`, copy `.env.example` to `.env` and fill in your values, then `npm run dev`
3. `cd client && npm install`, copy `.env.example` to `.env`, then `npm run dev`

Visitor view: `localhost:5173` · Admin inbox: `localhost:5173/admin`

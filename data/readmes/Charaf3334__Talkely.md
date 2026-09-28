# Talkely
Talkely is a web-based real-time chat application designed to demonstrate how WebSockets enable instant communication. Built as a learning project, it also covers core CRUD operations and showcases how modern applications manage dynamic data and user interactions efficiently. For more, you can try it [here](https://talkely.app).

![overview](/screenshots/talkely.PNG)

# Features
- You can create an account and log in using either your email address or your Google account.
- You can set a profile picture and update your username, email address, and password.
- You can chat with Talkely Ai assistant if you have any questions regarding the application.
- You can delete your account at any time.
- You can reset your password if you forget it.
- Users who have not verified their account cannot chat with others.
- You can have multiple conversations with different users.
- You can send unlimited messages, including text and photos.
- You can delete unwanted messages and conversations.
- Group chat is not currently supported but will be added in future versions.

# Learning Resources
- Socket.IO [documentation](https://socket.io/docs/v4/).
- PostgreSQL [database design](https://www.tigerdata.com/learn/guide-to-postgresql-database-design).
- Image uploading to [Cloudinary](https://www.youtube.com/watch?v=3Gj_mL9JJ6k).

# The Tech Stack
- **Frontend**: Next.js, TailwindCSS.
- **Backend**: Node.js, Express, Socket.IO.
- **Storage**: PostgreSQL, Cloudinary.

# Architecture
The schema below shows the database design I used for the application.

![schema](/screenshots/schema.PNG)

# Note
I’ve tested most of the application, but mistakes can happen. If you find any, feel free to open an issue.

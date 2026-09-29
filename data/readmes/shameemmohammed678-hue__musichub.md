# MusicHub 🎵

MusicHub is a full-stack music player web application built using React and Django REST Framework.

Users can register and log in, search and play songs, manage favorites and playlists, while administrators can upload new songs.

## Live Demo

https://musichub-brown.vercel.app/

## Features

### User Features

- User registration and login
- JWT authentication
- Search songs
- Play and pause songs
- Previous and next song controls
- Automatic next-song playback
- Song progress and seek control
- Volume and mute controls
- Add songs to favorites
- Add songs to playlists
- Responsive design for desktop and mobile

### Admin Features

- Admin-only song upload
- Upload song title and artist
- Upload MP3 audio files
- Upload cover images
- Cloudinary media storage
- Uploaded songs are automatically available in the application

## Technologies Used

### Frontend

- React
- JavaScript
- HTML
- CSS
- React Router
- Context API
- Lucide React

### Backend

- Python
- Django
- Django REST Framework
- JWT Authentication

### Database

- TiDB Cloud
- MySQL-compatible database

### Media Storage

- Cloudinary

### Deployment & Tools

- Vercel
- Git
- GitHub
- VS Code

## Project Architecture


User
  |
  v
React Frontend
  |
  | REST API
  v
Django REST Framework
  |
  +-------------> TiDB Cloud
  |
  +-------------> Cloudinary
                    |
                    +--> Audio Files
                    +--> Cover Images


musichub/
│
├── backend/
│   ├── accounts/
│   ├── music/
│   ├── config/
│   ├── manage.py
│   └── requirements.txt
│
├── public/
│   ├── images/
│   └── songs/
│
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Player.jsx
│   │   ├── Sidebar.jsx
│   │   └── SongCard.jsx
│   │
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   └── MusicContext.jsx
│   │
│   ├── pages/
│   │   ├── AdminUpload.jsx
│   │   ├── Favorites.jsx
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── PlayList.jsx
│   │   └── Register.jsx
│   │
│   ├── api.js
│   ├── App.jsx
│   └── main.jsx
│
└── README.md


##Authentication flow
User Login
    |
    v
React
    |
    v
Django Login API
    |
    v
JWT Access + Refresh Token
    |
    v
React stores authentication data



##Admin upload flow

Admin
  |
  v
React Admin Upload Page
  |
  v
Django Upload API
  |
  +----> Cloudinary
  |        |
  |        +--> Audio
  |        +--> Cover Image
  |
  v
TiDB Cloud
  |
  +--> Song details
  +--> Cloudinary URLs




 Security
i.JWT authentication is used for protected API requests.
ii.Admin upload access is checked on the backend.
iii.Database credentials are stored using environment variables.
iv.Cloudinary credentials are stored using environment variables.
v .env files are excluded from Git.


  Future Improvements
i.User profile management
ii.More playlist management features
iii.Improved media upload handling for larger files
iv.Music recommendations
v.Additional player features
vi.Improved error handling and token management




Author

Mohammed Shameem

BSc Computer Science

GitHub:
https://github.com/shameemmohammed678-hue

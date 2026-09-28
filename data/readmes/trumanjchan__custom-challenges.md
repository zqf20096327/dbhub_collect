# Custom Challenges
Paired a MySQL database with Socket.io to bring real-time challenges to you and your friend!
The inspiration: sometimes when my friends and I play video games one of us would jokingly say, "if we lose this next round, we're both doing 10 push ups each." With Custom Challenges users can create an account, challenge their friends, and see exactly when they've finished their push ups.

## Features
- Database - nicknames, passwords, and challenges are stored
- Bcrypt - passwords are hashed
- Paramaterized Queries & Sanitized Inputs - protects against SQL injection
- Pseudonymity - nicknames can be anything
- Socket.io - real-time interactions
- Responsive - view the site on your pc or phone

### App Workflow

[Watch Demo Video](https://youtu.be/OQpqbeDHH1E?si=AMmgzJBK1rxg4F2V)

---

<details>

<summary>Local Development</summary>

```bash
git clone https://github.com/trumanjchan/custom-challenges.git
npm install
```

Create a `.env` file with:
```
DB_HOST=
DB_PORT=
DB_USERNAME=
DB_PASSWORD=
DB_DATABASE=
```

Then run:
```bash
npm start
```

Navigate to `http://localhost:3000/`

</details>
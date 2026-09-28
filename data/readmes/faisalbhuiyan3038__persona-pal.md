# PersonaPal

> Create and chat with AI companions inspired by real or fictional personalities

[Live Demo](https://persona-pal-sigma.vercel.app/) • [Case Study](https://faisalbhuiyan.vercel.app/work/persona-pal)

## About PersonaPal

PersonaPal is a modern web application that lets you create and interact with AI companions inspired by historical figures, entrepreneurs, or any personality you can imagine. Want to discuss relativity with Einstein, talk innovation with Elon Musk, or create your own unique AI companion? PersonaPal makes it possible.

Key Features:
- Create custom AI companions by providing:
  - Personality traits and background
  - Seed conversations that shape their behavior
  - Detailed descriptions of their knowledge and expertise
- Chat with AI companions created by the community
- Real-time conversations with context-aware responses
- User authentication and profile management
- Persistent chat history
- Vector-based memory system for more natural conversations
- Only a user who created the companion can edit it.

## Limitations
- Currently supports English language only
- Rate limit: 10 requests per 10 seconds
- All API services (OpenAI, Replicate, etc.) are on free tier with their respective limitations
- Chat may stop working soon as the free tier is very limited.

## Screenshots

![image](/assets/homepage.png)

![image](/assets/create-page.png)

![image](/assets/chat-page.png)

<image width="300" src="assets/chat_page_mobile.png" />

## Tech Stack

### Frontend
- Next.js 14 (React Framework)
- TailwindCSS
- TypeScript

### Backend
- Node.js
- Prisma ORM
- MySQL / TiDB (Database)
- Upstash Redis (Caching)
- Pinecone (Vector Database)
- Cloudinary (Optimized storage for images)

### AI/ML
- Replicate (AI Model Hosting)
- OpenAI API (Language Processing)

### Authentication & Security
- Clerk (Authentication)

### Infrastructure
- Vercel (Deployment)

## Getting Started

### Prerequisites
- Node.js 18+
- TiDB MySQL or any equivalent db instance
- Replicate API key
- OpenAI API key
- Clerk account
- Upstash Redis instance
- Pinecone account

### Environment Variables

Create a `.env` file in the root directory following the `.env.example` file.

### Installation

1. Clone the repository
```bash
git clone https://github.com/faisalbhuiyan3038/persona-pal.git
cd persona-pal
```

2. Install dependencies
```bash
npm install
# or
yarn install
```

3. Set up the database
```bash
npx prisma generate
npx prisma db push
```

4. Run the development server
```bash
npm run dev
# or
yarn dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Creating a Companion

1. Sign up or log in to your account
2. Click on "Create"
3. Provide the following details:
   - Name and avatar for your companion
   - Background information and personality traits
   - Seed conversations to establish behavior patterns
   - Areas of expertise and knowledge
4. Submit and start chatting!

Note: There is no limit to how many companions you can create.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

[Faisal Bhuiyan] - [faisalbhuiyan3038@gmail.com]

Project Link: [https://github.com/faisalbhuiyan3038/persona-pal](https://github.com/faisalbhuiyan3038/persona-pal)

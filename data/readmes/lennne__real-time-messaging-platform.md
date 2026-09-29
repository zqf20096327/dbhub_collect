This is a [Next.js](https://nextjs.org) typescript project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

# Tools I Used 
### Front-End
- NextJs
- TailwindCSS
- Radix-Ui
- Zustand
- Zod
- LiveKit Library
 
### Back-End
- SocketIO
- Prisma
- NodeJs
- TanStack Query
- UploadThing Library


## Getting Started

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

# Code Setup

### 1. Environment Setup
Make sure your .env file has all the right details:
- Clerk Authentication details
- Prisma connection to serverless database - TiDB Database
- Get the database credentials, copy the password from the db and paste into the database_url in your .env file
  - run "npm i -D prisma"
  - run "npm prisma init"
  - run "npm prisma generate"
  - run "npm prisma db push"

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

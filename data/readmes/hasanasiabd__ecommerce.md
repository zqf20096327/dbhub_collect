# MyShop

Next.js App Router e-commerce application using TypeScript, Prisma, MySQL/TiDB, Resend, Cloudinary and Stripe.

## Setup

1. Copy `.env.example` to `.env.local`.
2. Fill the server-side secrets locally.
3. Install dependencies:
   `npm install`
4. Generate Prisma client:
   `npx prisma generate`
5. Apply the latest migration:
   `npx prisma migrate dev`
6. Run:
   `npm run dev`

## Architecture

- Customer accounts are verified through email OTP.
- Admin accounts are created and managed by Developers.
- Developer and Admin panel paths come from server-side environment variables.
- Admin credentials are database-managed; no admin credentials belong in `.env.local`.
- Product images use Cloudinary.
- Cart and Wishlist are persistent database records for authenticated users.

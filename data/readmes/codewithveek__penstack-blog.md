# Penstack - Modern Blog Platform

Penstack is a modern, clean, and customizable blog platform built with Next.js, featuring robust analytics, user management, and content creation capabilities.

## 🌟 Features

### Content Management

- Rich text editor with TipTap integration
- Markdown support
- Dynamic table of contents generation
- Post categorization and tagging
- Draft and publishing workflow
- Reading time calculation

### Analytics

- Comprehensive post view tracking
- User engagement metrics
- Device and browser analytics
- Geographic tracking
- Weekly/monthly growth statistics
- Customizable date range analytics
- Integration with Mixpanel, Google Analytics, and Google Tag Manager

### User Management

- Role-based access control
- Permission system
- User authentication (NextAuth.js)
- Email verification
- Profile management

### Technical Features

- Server-side rendering with Next.js
- TiDB (MySQL compatible) database with Drizzle ORM
- TypeScript support
- API rate limiting
- Secure encryption handling
- Responsive design with Chakra UI
- Real-time data updates with React Query

## 🚀 Getting Started

1. Clone the repository

```bash
git clone <repository-url>
cd penstack-blog
```

2. Install dependencies:

```bash
npm install
```

3. Set up your environment variables:

```bash
cp .env.example .env
```

4. Initialize the database:

```bash
npm run db:setup
```

5. Start the development server:

```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) to see your application.

## 📊 Database Setup

The project uses MySQL with Drizzle ORM. Available database commands:

```bash
npm run db:push     # Push schema changes
npm run db:migrate  # Run migrations
npm run db:gen      # Generate migration files
npm run db:create   # Create database
npm run db:seeds    # Seed initial data
npm run db:setup    # Complete setup
```

## 🔐 Security

- Built-in XSS protection
- CSRF protection
- Secure session handling
- Encrypted sensitive data
- Rate limiting on API routes

## 🛠️ Project Structure

```
src/
├── app/              # Next.js app directory
├── components/       # React components
├── db/              # Database schemas and config
├── lib/             # Utility libraries
├── utils/           # Helper functions
└── types/           # TypeScript definitions
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🔧 Configuration

The platform can be configured through the admin dashboard, including:

- Site settings
- Analytics preferences
- Email configuration
- User roles and permissions
- Content moderation settings

## 📚 Documentation

For more detailed documentation about specific features:

- [Next.js Documentation](https://nextjs.org/docs)
- [Chakra UI Documentation](https://chakra-ui.com/docs/getting-started)
- [TipTap Editor Documentation](https://tiptap.dev/docs)

## 🌐 Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DB_PORT=3306
DB_USER_NAME=your_username # Required
DB_USER_PASS=your_password # Required
DB_HOST=localhost # Required
DB_NAME=penstack_db # Required
DB_SSL_CONFIG={"rejectUnauthorized": true}

# Site URL
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# Authentication
NEXTAUTH_SECRET=your_nextauth_secret # Required
NEXTAUTH_URL=http://localhost:3000
GOOGLE_CLIENT_ID= # Required
GOOGLE_CLIENT_SECRET= # Required
ADMIN_EMAIL= # Required
ADMIN_PASSWORD= # Required
```

## 🚀 Deployment

The project supports deployment on both Vercel and Netlify platforms, with automatic environment configuration.

### Automatic Environment Configuration

The `next.config.mjs` automatically handles the site URL configuration based on the deployment platform:

- On Vercel: Uses `VERCEL_PROJECT_PRODUCTION_URL` (automatically set)
- On Netlify: Uses `URL` (automatically set)
- Local Development: Defaults to `http://localhost:3000`

### Deployment Options

1. **Vercel (Recommended)**

   - Deploy directly from your GitHub repository using [Vercel Platform](https://vercel.com/new)
   - Vercel will automatically detect your Next.js project and configure the build settings
   - No additional URL configuration needed

2. **Netlify**

   - Deploy using the [Netlify Platform](https://app.netlify.com/start)
   - Netlify will automatically configure the site URL
   - No additional URL configuration needed

3. **Custom Domain**
   - After deployment, you can configure a custom domain on either platform
   - The site URL will automatically update to match your custom domain

For more detailed deployment instructions, refer to:

- [Next.js Deployment Documentation](https://nextjs.org/docs/deployment)
- [Vercel Documentation](https://vercel.com/docs)
- [Netlify Documentation](https://docs.netlify.com/)

<h1 align="center">
  Next.js TypeScript SaaS Starter
</h1>

<p align="center">
  A modern Next.js starter template with TypeScript, Tailwind CSS, and more
</p>

---

## Features

- ⚡️ Next.js 15 with App Router
- 🎨 Tailwind CSS with Typography plugin
- 🔒 Better Auth for authentication
- 🗄️ Drizzle ORM with NeonDB integration
- 📝 MDX support for content
- 🎭 Framer Motion for animations
- 🔔 Sonner for toast notifications
- 🎵 use-sound for sound effects
- 🎨 Akar Icons for beautiful icons
- 🔍 SEO optimized(with metadata and schema.org)
- 🎯 TypeScript for type safety
- 🧹 ESLint + Prettier for code quality
- 🐶 Husky for git pre commit
- 🚀 View transitions for smooth page navigation

## Project Structure

```
├── app/                 # Next.js app directory
├── components/          # React components
│   ├── atoms/          # Basic UI components
│   └── ...
├── hooks/              # Custom React hooks
├── styles/             # Global styles
├── utils/              # Utility functions
├── public/             # Static assets
├── assets/             # Project assets
└── ...
```

## Included

- `not found page` page to handle 404 routes
- `config.ts` container site information to be used for seo and schema.org data
- `seo.ts` util to generate SEO metadata and schema.org
- `manifest.json` for site info
- `classnames` util for easily managing classes
- `components/atoms/Button.tsx` a button component with variants
- `hooks/useClickOutside` hook to check if user clicked outside the element
- `hooks/useModal` hook to create modals, which can close with esc
- `hooks/useDynamicHeight`
- `auth pages` - Auth page for login

## Additional Packages Used

- next-view-transitions - for page smooth transitions
- Tailwind CSS - for styling(with typography plugin)
- Framer Motion - for animations
- Akar Icons - library for rounded icons
- Sonner - for toast messages
- use-sound - for using sounds
- Class Variance Authority - for type-safely managing class names

## Getting Started

1. Clone and install: `git clone https://github.com/nirnejak/nextjs-typescript-saas.git && cd nextjs-typescript-saas && bun install`

2. Set up environment: `cp .env.example .env` and update `.env` with your config

3. Start dev server: `bun run dev`

## Available Scripts

- `bun install` - Install dependencies
- `bun run prepare` - Setup pre-commit hooks
- `bun run dev` - Start development server
- `bun run lint` - Run ESLint
- `bun run format` - Format with Prettier
- `bun run type-check` - Run TypeScript type checking
- `bun run db:generate` - Generate database migrations
- `bun run db:migrate` - Run database migrations
- `bun run build` - Build for production
- `bun run start` - Start production server

## Configuration

Update the `config.ts` file with your site's information:

```typescript
const config = {
  baseUrl: "https://your-site.com",
  appName: "Your App Name",
  appDescription: "Your app description",
  creator: "Your Name",
  authorName: "Your Name",
  authorUrl: "Your URL or Email",
  keywords: ["your", "keywords"],
  twitterSite: "@your-site",
  twitterCreator: "@your-username",
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [Jitendra Nirnejak](https://github.com/nirnejak)

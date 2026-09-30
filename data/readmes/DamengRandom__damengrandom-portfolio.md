# DamenGRandom - Portfolio Site

Welcome to my personal portfolio website! This is a modern, responsive web application showcasing my work, skills, and experience as a developer.

## 🚀 Technologies Used

### Frontend Framework
- **[Next.js 15.5.4](https://nextjs.org)** - React framework with App Router
- **[React 19.1.0](https://reactjs.org)** - Latest React with concurrent features
- **[TypeScript 5](https://www.typescriptlang.org)** - Type-safe JavaScript

### Styling & UI
- **[Tailwind CSS 4](https://tailwindcss.com)** - Utility-first CSS framework
- **[Radix UI](https://www.radix-ui.com)** - Unstyled, accessible UI components
  - Avatar, Hover Card, Scroll Area, Separator, Slot, Tabs, Tooltip
- **[Lucide React](https://lucide.dev)** - Beautiful & consistent icon library
- **[React Icons](https://react-icons.github.io/react-icons/)** - Popular icon library with brand icons
- **[Framer Motion](https://www.framer.com/motion/)** - Production-ready motion library

### Development Tools
- **[ESLint 9](https://eslint.org)** - Code linting and formatting
- **[PostCSS](https://postcss.org)** - CSS processing
- **Class Variance Authority** - Type-safe component variants
- **clsx & Tailwind Merge** - Conditional CSS class utilities

### Deployment & CI/CD
- **[Vercel](https://vercel.com)** - Deployment platform
- **GitHub Actions** - Automated CI/CD pipeline
- **Turbopack** - Fast bundler for development

## ✨ Features

- 🎨 **Modern Design** - Clean, professional interface
- 📱 **Responsive Layout** - Optimized for all devices
- ⚡ **Performance Optimized** - Fast loading with Next.js optimizations
- 🎭 **Smooth Animations** - Engaging user experience with Framer Motion
- 🔧 **Technology Slider** - Interactive showcase of technical skills
- 📊 **Visit Counter** - Track site engagement
- 🌐 **SEO Optimized** - Built-in Next.js SEO features
- ♿ **Accessible** - WCAG compliant with Radix UI components

## 🛠️ Getting Started

### Prerequisites
- Node.js 18.x or 20.x
- npm, yarn, pnpm, or bun

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd damengrandom
```

2. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

3. Run the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📝 Available Scripts

- `npm run dev` - Start development server with Turbopack
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## 🚀 Deployment

This project is configured for automatic deployment to Vercel with GitHub Actions CI/CD pipeline.

### Manual Deployment
```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

## 📁 Project Structure

```
src/
├── app/                 # Next.js App Router
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   └── globals.css     # Global styles
├── components/         # React components
│   ├── TechSlider.tsx  # Technology showcase slider
│   ├── VisitCounter.tsx # Site visit tracking
│   └── ui/             # Reusable UI components
├── hooks/              # Custom React hooks
├── lib/                # Utility functions
└── ...
```

## 🤝 Contributing

This is a personal portfolio project, but feedback and suggestions are always welcome!

## 📄 License

This project is private and proprietary.

---

Built with ❤️ using Next.js and modern web technologies.

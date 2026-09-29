# Bruce Tidball - Professional Website

A modern, responsive single-page website for a construction and project management professional. Built with Angular and designed for GitHub Pages deployment.

## Features

- **Single-page design** with smooth scrolling navigation
- **Responsive layout** optimized for mobile, tablet, and desktop
- **Modern minimal design** with professional aesthetics
- **Contact integration** with direct email and phone links
- **GitHub Pages ready** for free hosting

## Sections

1. **Hero/Header** - Professional introduction with navigation
2. **About** - Professional summary and core values
3. **Experience** - Project portfolio and expertise areas
4. **Contact** - Direct contact information and availability

## Technology Stack

- Angular 19
- Angular Material
- TypeScript
- CSS3 with custom properties
- GitHub Pages for hosting

## Development

### Prerequisites

- Node.js (version 18 or higher)
- npm or yarn

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd bruce-tidball-website

# Install dependencies
npm install

# Start development server
ng serve
```

Navigate to `http://localhost:4200/` to view the website.

### Building for Production

```bash
# Build for production
ng build

# The build artifacts will be stored in the `dist/` directory
```

## Deployment to GitHub Pages

This project is configured for automatic deployment to GitHub Pages:

1. Push changes to the `main` branch
2. GitHub Actions will automatically build and deploy the site
3. The site will be available at `https://[username].github.io/[repository-name]`

### Manual Deployment

If you prefer manual deployment:

1. Build the project: `ng build`
2. Copy the contents of `dist/bruce-tidball-website/` to your GitHub Pages repository
3. Push the changes

## Customization

### Content Updates

To update the content for your specific professional:

1. **Header Component** (`src/app/components/header/`):
   - Update the name and title in the template
   - Modify the hero text and call-to-action buttons
   - Replace placeholder text with actual professional information
   - Update years of experience and core values
   - Replace the image placeholder with a professional photo

2. **Experience Component** (`src/app/components/experience/`):
   - Update project examples with real projects
   - Modify expertise areas to match your field
   - Update professional achievements and statistics

3. **Contact Component** (`src/app/components/contact/`):
   - Replace contact information with actual details
   - Update email, phone, and location information
   - Modify LinkedIn profile link

### Styling Customization

- **Colors**: Update CSS custom properties in `src/styles.css`
- **Fonts**: Modify font imports in `src/index.html`
- **Layout**: Adjust component-specific styles in individual CSS files

### Adding New Sections

To add new sections:

1. Generate a new component: `ng generate component components/[section-name]`
2. Add the component to `app.component.html`
3. Import the component in `app.component.ts`
4. Update navigation in the header component

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or support, please contact [your-email@example.com].
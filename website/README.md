# KPA Documentation Website

This folder contains the Docusaurus-based documentation website for the Kubernetes Practice Assistant (KPA).

## Quick Start

### Development

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The site will be available at `http://localhost:3000`

### Build

```bash
# Build static files
npm run build

# Test production build locally
npm run serve
```

## Deployment

The website is automatically deployed to GitHub Pages when changes are pushed to the main branch. The deployment is handled by the GitHub Actions workflow at `.github/workflows/deploy-docs.yml`.

### Before Deploying

1. Update `docusaurus.config.ts` with your GitHub username:
   - Replace `your-github-username` with your actual GitHub username
   - Update the `url` if using a custom domain

2. Enable GitHub Pages in your repository settings:
   - Go to Settings → Pages
   - Select "GitHub Actions" as the source

### Manual Deployment

If you need to deploy manually:

```bash
# Deploy using SSH
USE_SSH=true npm run deploy

# Or using HTTPS
GIT_USER=<Your GitHub username> npm run deploy
```

## Project Structure

```
website/
├── docs/                 # Documentation pages
│   ├── intro.md         # Getting started guide
│   ├── installation.md  # Installation instructions
│   ├── usage.md         # Usage guide
│   └── deployment.md    # Deployment instructions
├── src/
│   ├── components/      # React components
│   ├── css/            # Custom styles
│   └── pages/          # Additional pages
├── static/             # Static assets
├── docusaurus.config.ts # Main configuration
└── sidebars.ts         # Sidebar configuration
```

## Adding Documentation

1. Create new markdown files in the `docs/` directory
2. Add frontmatter for metadata:
   ```markdown
   ---
   sidebar_position: 5
   title: Your Page Title
   ---
   ```
3. The sidebar will automatically include new pages

## Customization

- **Theme**: Edit `src/css/custom.css` for styling
- **Configuration**: Update `docusaurus.config.ts`
- **Homepage**: Modify `src/pages/index.tsx`
- **Features**: Edit `src/components/HomepageFeatures/index.tsx`

## Learn More

- [Docusaurus Documentation](https://docusaurus.io/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)

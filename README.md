# Chrome Wrapped

A Spotify Wrapped-style Chrome extension that transforms your browsing history into beautiful, shareable insights.

## Features

- **Website Analytics** — Discover your most visited websites and browsing patterns
- **Time Insights** — Understand your daily browsing rhythms and peak hours
- **Category Breakdown** — See how you spend time across different website categories
- **Yearly Overview** — Visualize your browsing habits throughout the year
- **Browser Clubs** — Get assigned a personality archetype based on your browsing style
- **Share Cards** — Export beautiful, shareable images of your stats

## Architecture

```
chrome_wrapped/
├── extension/     # Chrome Extension (MV3 + WXT + React + TypeScript)
├── web/           # Next.js 15 Wrapped Story UI (Bootstrap + Framer Motion)
├── backend/       # FastAPI Python backend (analytics + categorization)
└── shared/        # Shared TypeScript types
```

## Tech Stack

- **Extension**: Manifest V3, WXT, React 18, TypeScript, Vite
- **Web App**: Next.js 15, TypeScript, Bootstrap 5, Framer Motion, Recharts
- **Backend**: Python 3.12, FastAPI, Pydantic v2, SQLModel, SQLite
- **Tooling**: pnpm workspaces, Turborepo, ESLint, Prettier, Ruff, Black

## Getting Started

### Prerequisites

- Node.js >= 20.0.0
- pnpm >= 9.0.0
- Python >= 3.12

### Installation

```bash
# Install JS dependencies
pnpm install

# Set up Python backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[dev]"
```

### Development

```bash
# Start all services (extension, web, backend)
pnpm dev

# Or run individually:

# Extension (opens Chrome with extension loaded)
cd extension && pnpm dev

# Web app
cd web && pnpm dev

# Backend
cd backend && uvicorn app.main:app --reload --port 8000
```

### Building

```bash
# Build all packages
pnpm build

# Build extension for distribution
cd extension && pnpm build
```

## Privacy

- Your browsing history is only processed to generate your Wrapped
- Data is automatically purged from the backend after 24 hours
- No third-party trackers in the web app
- Future: local-only mode for complete privacy

## License

MIT

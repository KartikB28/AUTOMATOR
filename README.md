# The Automator

Fully autonomous content automation desktop application. Runs 24/7 to discover trends, generate content, create visuals, publish to 6 platforms, and analyze performance.

## Architecture

- **Electron** - Desktop shell (Windows/macOS/Linux)
- **React + Vite + Tailwind** - Frontend UI
- **FastAPI + SQLAlchemy + APScheduler** - Python backend
- **SQLite** - Local data store with optional Supabase cloud sync

## The 5 Bots

1. **Scout Bot** (every 2h) - Scrapes Google Trends, Reddit, Twitter, TikTok, YouTube, RSS for trending topics
2. **Builder Bot** (every 1h) - Uses Claude Sonnet 4.6 to generate platform-specific content
3. **Creator Bot** (every 1h) - Generates visuals via DALL-E 3 -> Stability AI -> Pexels -> Unsplash fallback chain
4. **Publisher Bot** (every 15min) - Posts to Instagram, TikTok, YouTube, Twitter, LinkedIn, Facebook
5. **Analyst Bot** (every 6h) - Pulls metrics, calculates engagement, generates weekly AI digests

## Setup

```bash
# Unix / macOS
./setup.sh

# Windows
setup.bat
```

Then edit `config/.env` with your API keys and run:

```bash
npm start
```

## Required API Keys

- `ANTHROPIC_API_KEY` (required for content generation)
- At least one platform API for posting

See `config/.env.example` for the full list.

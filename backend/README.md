# Chrome Wrapped Backend

FastAPI backend for Chrome Wrapped analytics.

## Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -e ".[dev]"

# Run development server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest

# Format code
black .
ruff check --fix .
```

## API Endpoints

- `POST /runs` - Create a new Wrapped run from browsing history
- `GET /runs/{runId}/insights` - Get computed insights for a run
- `GET /health` - Health check endpoint

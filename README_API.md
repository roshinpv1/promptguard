# PromptShield API & Frontend

## Quick Start

### Development

1. **Start API server:**
```bash
cd /Users/roshinpv/Documents/next/promptguard
pip install -e .
pip install -r api/requirements.txt
uvicorn api.main:app --reload --port 8000
```

2. **Start Frontend:**
```bash
cd frontend
npm install
npm start
```

Frontend will be available at http://localhost:3000
API will be available at http://localhost:8000
API docs at http://localhost:8000/docs

### Docker

```bash
docker-compose up --build
```

API: http://localhost:8000
Frontend: http://localhost:80

## API Endpoints

### Scans
- `POST /api/v1/scans` - Create new scan
- `GET /api/v1/scans` - List scans (with pagination)
- `GET /api/v1/scans/{run_id}` - Get scan details
- `GET /api/v1/scans/{run_id}/results` - Get full results JSON
- `DELETE /api/v1/scans/{run_id}` - Delete scan

### Test External API
- `POST /api/v1/test-api` - Test external LLM API for security

### Config
- `GET /api/v1/config` - Get default config
- `PUT /api/v1/config` - Update config template
- `POST /api/v1/config/validate` - Validate config YAML

## Frontend Pages

- `/scans` - Scan Dashboard (create scans, view history)
- `/test-api` - Test External LLM APIs
- `/results/:runId` - View detailed scan results
- `/config` - Configuration editor

## Environment Variables

- `CORS_ORIGINS` - Comma-separated list of allowed origins (default: `http://localhost:3000,http://localhost:8080`)
- `REACT_APP_API_URL` - API base URL for frontend (default: `http://localhost:8000`)


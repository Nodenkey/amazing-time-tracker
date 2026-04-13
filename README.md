# Amazing Time Tracker Backend (feat/backend)

This branch implements the backend API for the **Amazing Time Tracker** project.

## Tech Stack
- FastAPI (Python 3.11+)
- In-memory store (no external database)
- uv as Python package/dependency manager

## Time Entry Model
Each time entry has the following fields:
- `id` (string, generated UUID)
- `date` (string, ISO date `YYYY-MM-DD`)
- `person_name` (string, required, non-blank)
- `activity` (string, required, non-blank)
- `duration_minutes` (integer, required, > 0)
- `notes` (string, optional)
- `created_at` (ISO datetime, server-generated)

## API Base URL
All endpoints are prefixed with `/api/v1`.

### Health Check
- `GET /health`
  - **Response 200**: `{ "status": "ok" }`

### Time Entries

#### List time entries
- `GET /api/v1/time-entries/`
- **Response 200**: `[{...TimeEntry}, ...]`

#### Get time entry by id
- `GET /api/v1/time-entries/{id}`
- **Response 200**: `{...TimeEntry}`
- **404**: `{ "error": "not_found", "message": "Time entry with id {id} does not exist", "detail": null }`

#### Create time entry
- `POST /api/v1/time-entries/`
- **Request body**:
```json
{
  "date": "2026-04-13",
  "person_name": "Jane Doe",
  "activity": "Pair programming",
  "duration_minutes": 60,
  "notes": "Worked on API design"
}
```
- **Response 201**:
```json
{
  "id": "generated-uuid",
  "date": "2026-04-13",
  "person_name": "Jane Doe",
  "activity": "Pair programming",
  "duration_minutes": 60,
  "notes": "Worked on API design",
  "created_at": "2026-04-13T10:00:00.000000"
}
```

#### Update time entry (partial)
- `PATCH /api/v1/time-entries/{id}`
- **Request body** (any subset of fields):
```json
{
  "activity": "Updated activity description",
  "duration_minutes": 90
}
```
- **Response 200**: updated `TimeEntry`
- **404**: same error shape as above

#### Delete time entry
- `DELETE /api/v1/time-entries/{id}`
- **Response 204**: no body
- **404**: same error shape as above

## Error Responses
All custom errors use the following structure:
```json
{
  "error": "not_found",
  "message": "Time entry with id {id} does not exist",
  "detail": null
}
```

FastAPI/Pydantic validation errors return the default 422 response body.

## Running Locally

```bash
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or via Docker Compose from the repo root:

```bash
docker compose up --build
```

## Tests

Backend tests live under `backend/tests/` and can be run with:

```bash
cd backend
pytest
```

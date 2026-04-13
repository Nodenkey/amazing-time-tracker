# Amazing Time Tracker

Amazing Time Tracker is a simple internal tool for logging daily time and activities.

## Backend

The backend is a FastAPI application exposing a small CRUD API for time entries under `/api/v1`.

Key endpoints:
- `GET /health` – health check
- `GET /api/v1/time-entries/` – list all entries
- `POST /api/v1/time-entries/` – create a new entry
- `DELETE /api/v1/time-entries/{id}` – delete an entry

## Frontend (HTML/CSS/JS)

The frontend is a single static page in the `frontend/` directory, built with plain HTML, CSS, and JavaScript (no framework).

### Files

- `frontend/index.html` – main page with:
  - A form to add a new time entry (date, person name, activity, duration in minutes, optional notes).
  - A table listing all existing entries with columns: Date, Person, Activity, Duration (min), Notes, Actions.
  - A Delete button per row to remove an entry.
- `frontend/styles.css` – basic, responsive styling for the layout, form, and table.
- `frontend/app.js` – all client-side logic:
  - Loads entries from `GET /api/v1/time-entries/` on page load and when the user clicks **Refresh**.
  - Submits the form via `POST /api/v1/time-entries/` and refreshes the list on success.
  - Deletes entries via `DELETE /api/v1/time-entries/{id}` and refreshes the list on success.
  - Shows simple loading and error messages and disables the submit button while a request is in-flight.
- `frontend/Dockerfile` – nginx-based image that serves the static files from `/usr/share/nginx/html` on port 3000.
- `frontend/nginx.conf` – nginx configuration used by the Dockerfile.
- `frontend/railway.toml` – Railway configuration for building and running the frontend service using the Dockerfile.

### API base URL

The frontend uses the following logic for the API base URL:

```js
const API_BASE_URL = (window.__API_BASE_URL__ || "http://localhost:8000/api/v1").replace(/\/$/, "");
```

- For local development, it defaults to `http://localhost:8000/api/v1` (matching `docker-compose.yml`).
- In production (Railway), DevOps can inject `window.__API_BASE_URL__` via a small inline script or template so the frontend points at the deployed backend domain.

### Local development

With Docker and docker-compose installed:

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

The frontend will call the backend at `http://localhost:8000/api/v1`.

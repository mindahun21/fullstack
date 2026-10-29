# Safaricom Ethiopia — Task Manager Assessment

Full-stack task management application 

- **Stack:** Django 6.x + DRF (Backend), React + TypeScript + Vite + Tailwind CSS (Frontend), Docker (Backend).
- **API URL:** `http://localhost:8080/api/tasks`
- **Frontend URL:** `http://localhost:5173`

---

## 1. Directory Structure

```text
fullstack/
├── backend/
│   ├── core/                  # Django project settings & custom exception handler
│   ├── tasks/                 # Task model, serializer, Class-Based ViewSet, and URLs
│   ├── Dockerfile             # Container image exposing port 8080
│   ├── requirements.txt       # Dependencies (Django, DRF, CORS, Spectacular, Gunicorn)
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── api/tasks.ts       # Axios client adhering to /api/tasks contract
│   │   ├── App.tsx            # Clean, functional React client
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

---

## 2. Running Locally

### Backend (Django)
```bash
cd backend
source .venv/bin/activate    
python manage.py runserver 8080
```
- API Endpoint: `http://localhost:8080/api/tasks`
- Swagger UI Documentation: `http://localhost:8080/api/docs/`

### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** 

---

## 3. Running Backend in Docker

```bash
cd backend
docker build -t task-manager-backend .
docker run -p 8080:8080 task-manager-backend
```

Verify with:
```bash
curl http://localhost:8080/api/tasks
```

---

## 4. API Contract & Validation Rules

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/tasks` | Return all tasks | 200 OK |
| `GET` | `/api/tasks/{id}` | Return one task | 200 OK (404 if missing) |
| `POST` | `/api/tasks` | Create task | 201 Created (400 if invalid) |
| `PUT` | `/api/tasks/{id}` | Update task | 200 OK (400 / 404 as relevant) |
| `DELETE` | `/api/tasks/{id}` | Delete task | 204 No Content (404 if missing) |

**Validation Rules:**
- `title`: Required, 3–100 characters.
- `description`: Optional, maximum 500 characters.
- `status`: One of `TODO`, `IN_PROGRESS`, `DONE` (defaults to `TODO` when omitted).
- Consistent JSON error response: `{ "status": 400, "message": "...", "errors": {...} }`.

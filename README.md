# travel-planner-47086-47095

Travel Planner project with a Flask backend API.

Backend dev server will expose OpenAPI at /docs and JSON at /openapi.json.

Quick start:
1. Install: pip install -r travel_planner_backend/requirements.txt
2. Run: cd travel_planner_backend && python run.py
3. Swagger UI: http://localhost:3001/docs
4. Health: GET http://localhost:3001/

Flask CLI alternative:
- From travel_planner_backend:
  FLASK_APP=app:create_app flask run --host=0.0.0.0 --port=3001

Notes on circular imports:
- Route modules only export a Blueprint object (blp) and do not import the Flask app.
- The app factory (app/__init__.py:create_app) lazily imports and registers blueprints to avoid circular imports.
- Environment variables are loaded via python-dotenv inside create_app(), which is safe and non-global at import time.

Container/Preview notes:
- The backend binds to 0.0.0.0:3001 for container health checks.
- FLASK_APP (for CLI) is app:create_app
- Do not enable FLASK_ENV=development in container/production. The run.py disables reloader and debug by default.

Alternative run via Flask CLI:
- From travel_planner_backend: FLASK_APP=app:create_app flask run --host=0.0.0.0 --port=3001

CORS:
- Defaults to allow http://localhost:3000. Override via FRONTEND_ORIGIN env var.

Environment variables (placeholders):
- FRONTEND_ORIGIN=http://localhost:3000
- USE_IN_MEMORY_STORE=true
- DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname (future integration)
- PORT=3001 (optional override)

API overview (in-memory persistence):
- Users
  - GET    /api/users
  - POST   /api/users
  - GET    /api/users/{user_id}
  - PATCH  /api/users/{user_id}
  - DELETE /api/users/{user_id}
- Trips
  - GET    /api/trips
  - POST   /api/trips
  - GET    /api/trips/{trip_id}
  - PATCH  /api/trips/{trip_id}
  - DELETE /api/trips/{trip_id}
- Itineraries
  - GET    /api/itineraries?trip_id=<id>
  - POST   /api/itineraries
  - GET    /api/itineraries/{itinerary_id}
  - PATCH  /api/itineraries/{itinerary_id}
  - DELETE /api/itineraries/{itinerary_id}
- Destinations
  - GET    /api/destinations?itinerary_id=<id>
  - POST   /api/destinations
  - GET    /api/destinations/{destination_id}
  - PATCH  /api/destinations/{destination_id}
  - DELETE /api/destinations/{destination_id}
- Activities
  - GET    /api/activities?itinerary_id=<id>&destination_id=<id>
  - POST   /api/activities
  - GET    /api/activities/{activity_id}
  - PATCH  /api/activities/{activity_id}
  - DELETE /api/activities/{activity_id}

OpenAPI generation file:
- travel_planner_backend/generate_openapi.py
This script writes interfaces/openapi.json using flask-smorest spec.

Notes:
- Persistence is in-memory; restart clears data.
- TODO: If travel_planner_database container is available, replace in-memory with SQLAlchemy models and Alembic migrations.
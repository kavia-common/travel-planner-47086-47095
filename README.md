# travel-planner-47086-47095

Travel Planner project with a Flask backend API.

Backend dev server will expose OpenAPI at /docs and JSON at /openapi.json.

Quick start:
1. Install: pip install -r travel_planner_backend/requirements.txt
2. Run: cd travel_planner_backend && python run.py
3. Swagger UI: http://localhost:5000/docs
4. Health: GET http://localhost:5000/

CORS:
- Defaults to allow http://localhost:3000. Override via FRONTEND_ORIGIN env var.

Environment variables (placeholders):
- FRONTEND_ORIGIN=http://localhost:3000
- USE_IN_MEMORY_STORE=true
- DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname (future integration)

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
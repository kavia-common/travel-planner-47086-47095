"""Flask application factory for the Travel Planner backend.

FLASK_APP discovery:
- You can run with Flask CLI using: FLASK_APP=app:create_app flask run --host=0.0.0.0 --port=3001

This module avoids heavy imports and side effects at module import time
to ensure fast container startup and predictable behavior.
"""
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from dotenv import load_dotenv
import os

# PUBLIC_INTERFACE
def create_app() -> Flask:
    """Application factory for the Travel Planner API.

    Creates and configures the Flask app, loads environment variables via python-dotenv,
    sets up CORS, configures OpenAPI/Swagger via flask-smorest, and registers all route blueprints.

    Returns:
        Flask: Configured Flask application instance.
    """
    # Load env from .env if present (non-fatal if missing)
    load_dotenv()

    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # CORS: allow React dev server on port 3000 and same-origin by default
    frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
    CORS(app, resources={r"/*": {"origins": [frontend_origin, "*"]}})

    # OpenAPI / Swagger configuration
    app.config["API_TITLE"] = "Travel Planner API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Public tags for organization in Swagger UI
    openapi_tags = [
        {"name": "Health", "description": "Health check route"},
        {"name": "Users", "description": "Manage users (placeholder until auth is integrated)."},
        {"name": "Trips", "description": "Manage trips."},
        {"name": "Itineraries", "description": "Manage itineraries linked to trips."},
        {"name": "Destinations", "description": "Manage destinations linked to itineraries."},
        {"name": "Activities", "description": "Manage activities linked to itineraries or destinations."},
    ]
    app.config["OPENAPI_TAGS"] = openapi_tags

    api = Api(app)

    # Import blueprints lazily to avoid circular imports and keep import time low.
    from .routes.health import blp as health_blp
    from .routes.users import blp as users_blp
    from .routes.trips import blp as trips_blp
    from .routes.itineraries import blp as itineraries_blp
    from .routes.destinations import blp as destinations_blp
    from .routes.activities import blp as activities_blp

    # Register blueprints one-by-one to make isolating apispec errors straightforward.
    # If a registration raises InvalidParameterError, comment out subsequent registrations
    # temporarily to pinpoint the offending blueprint. Current order prioritizes suspected modules last.
    api.register_blueprint(health_blp)
    api.register_blueprint(users_blp)
    api.register_blueprint(trips_blp)
    # Suspected offender (kept last among core entities to ease isolation)
    api.register_blueprint(itineraries_blp)
    api.register_blueprint(destinations_blp)
    api.register_blueprint(activities_blp)

    # Attach api to app for tooling (e.g., generate_openAPI)
    app.extensions = getattr(app, "extensions", {})
    app.extensions["smorest_api"] = api

    return app

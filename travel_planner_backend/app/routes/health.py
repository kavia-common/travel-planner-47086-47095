from flask_smorest import Blueprint
from flask.views import MethodView

# PUBLIC_INTERFACE
blp = Blueprint(
    "Health",
    "health",
    url_prefix="/",
    description="Health check route. Returns a simple JSON payload to indicate service status.",
)


@blp.route("/")
class HealthCheck(MethodView):
    """Health check endpoints."""

    def get(self):
        """Simple health check endpoint that returns a small JSON document.

        Returns:
            dict: {"message": "Healthy"} to indicate the API is running.
        """
        return {"message": "Healthy"}

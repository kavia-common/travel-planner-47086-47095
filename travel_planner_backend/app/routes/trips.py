from flask_smorest import Blueprint, abort
from flask.views import MethodView
from webargs.flaskparser import use_args
from ..schemas import TripCreateSchema, TripUpdateSchema, TripSchema
from ..models import list_trips, create_trip, get_trip, update_trip, delete_trip

blp = Blueprint(
    "Trips",
    "trips",
    url_prefix="/api/trips",
    description="Endpoints to manage trips.",
)


@blp.route("")
class TripsCollection(MethodView):
    """Trips collection endpoints."""

    @blp.response(200, TripSchema(many=True))
    def get(self):
        """List trips."""
        return list_trips()

    @use_args(TripCreateSchema, location="json")
    @blp.response(201, TripSchema)
    def post(self, args):
        """Create a trip."""
        try:
            t = create_trip(
                title=args["title"],
                description=args.get("description"),
                user_id=args.get("user_id"),
                start_date=args.get("start_date"),
                end_date=args.get("end_date"),
            )
            return t
        except ValueError as e:
            abort(400, message=str(e))


@blp.route("/<int:trip_id>")
class TripsItem(MethodView):
    """Trip item endpoints."""

    @blp.response(200, TripSchema)
    def get(self, trip_id: int):
        """Get a trip by ID."""
        t = get_trip(trip_id)
        if not t:
            abort(404, message="Trip not found")
        return t

    @use_args(TripUpdateSchema, location="json")
    @blp.response(200, TripSchema)
    def patch(self, args, trip_id: int):
        """Update a trip."""
        try:
            t = update_trip(
                trip_id,
                title=args.get("title"),
                description=args.get("description"),
                user_id=args.get("user_id"),
                start_date=args.get("start_date"),
                end_date=args.get("end_date"),
            )
            if not t:
                abort(404, message="Trip not found")
            return t
        except ValueError as e:
            abort(400, message=str(e))

    @blp.response(204)
    def delete(self, trip_id: int):
        """Delete a trip and cascade its children."""
        ok = delete_trip(trip_id)
        if not ok:
            abort(404, message="Trip not found")
        return ""

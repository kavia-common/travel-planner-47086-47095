from flask_smorest import Blueprint, abort
from flask.views import MethodView
from webargs.flaskparser import use_args
from webargs import fields as arg_fields
from ..schemas import ItineraryCreateSchema, ItineraryUpdateSchema, ItinerarySchema
from ..models import (
    list_itineraries,
    create_itinerary,
    get_itinerary,
    update_itinerary,
    delete_itinerary,
)

blp = Blueprint(
    "Itineraries",
    "itineraries",
    url_prefix="/api/itineraries",
    description="Endpoints to manage itineraries linked to trips.",
)


@blp.route("")
class ItinerariesCollection(MethodView):
    """Itineraries collection endpoints."""

    @blp.arguments({"trip_id": arg_fields.Int(required=False)}, location="query")
    @blp.response(200, ItinerarySchema(many=True))
    def get(self, args):
        """List itineraries. Optionally filter by trip_id."""
        trip_id = args.get("trip_id")
        return list_itineraries(trip_id=trip_id)

    @use_args(ItineraryCreateSchema, location="json")
    @blp.response(201, ItinerarySchema)
    def post(self, args):
        """Create an itinerary within a trip."""
        try:
            it = create_itinerary(
                trip_id=args["trip_id"],
                name=args["name"],
                start_date=args.get("start_date"),
                end_date=args.get("end_date"),
                notes=args.get("notes"),
            )
            return it
        except ValueError as e:
            abort(400, message=str(e))


@blp.route("/<int:itinerary_id>")
class ItinerariesItem(MethodView):
    """Itinerary item endpoints."""

    # Explicit OpenAPI param for path itinerary_id
    @blp.doc(parameters=[{
        "name": "itinerary_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "Itinerary ID"
    }])
    @blp.response(200, ItinerarySchema)
    def get(self, itinerary_id: int):
        """Get itinerary by ID."""
        it = get_itinerary(itinerary_id)
        if not it:
            abort(404, message="Itinerary not found")
        return it

    # Explicit OpenAPI param for path itinerary_id
    @blp.doc(parameters=[{
        "name": "itinerary_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "Itinerary ID"
    }])
    @use_args(ItineraryUpdateSchema, location="json")
    @blp.response(200, ItinerarySchema)
    def patch(self, args, itinerary_id: int):
        """Update an itinerary."""
        it = update_itinerary(
            itinerary_id,
            name=args.get("name"),
            start_date=args.get("start_date"),
            end_date=args.get("end_date"),
            notes=args.get("notes"),
        )
        if not it:
            abort(404, message="Itinerary not found")
        return it

    # Explicit OpenAPI param for path itinerary_id
    @blp.doc(parameters=[{
        "name": "itinerary_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "Itinerary ID"
    }])
    @blp.response(204)
    def delete(self, itinerary_id: int):
        """Delete an itinerary and cascade its destinations and activities."""
        ok = delete_itinerary(itinerary_id)
        if not ok:
            abort(404, message="Itinerary not found")
        return ""

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from webargs.flaskparser import use_args
from webargs import fields as arg_fields
from ..schemas import DestinationCreateSchema, DestinationUpdateSchema, DestinationSchema
from ..models import (
    list_destinations,
    create_destination,
    get_destination,
    update_destination,
    delete_destination,
)

blp = Blueprint(
    "Destinations",
    "destinations",
    url_prefix="/api/destinations",
    description="Endpoints to manage destinations linked to itineraries.",
)


@blp.route("")
class DestinationsCollection(MethodView):
    """Destinations collection endpoints."""

    @blp.arguments({"itinerary_id": arg_fields.Int(required=False)}, location="query")
    @blp.response(200, DestinationSchema(many=True))
    def get(self, args):
        """List destinations. Optionally filter by itinerary_id."""
        itinerary_id = args.get("itinerary_id")
        return list_destinations(itinerary_id=itinerary_id)

    @use_args(DestinationCreateSchema, location="json")
    @blp.response(201, DestinationSchema)
    def post(self, args):
        """Create a destination within an itinerary."""
        try:
            d = create_destination(
                itinerary_id=args["itinerary_id"],
                name=args["name"],
                location=args.get("location"),
                arrival_date=args.get("arrival_date"),
                departure_date=args.get("departure_date"),
                notes=args.get("notes"),
            )
            return d
        except ValueError as e:
            abort(400, message=str(e))


@blp.route("/<int:destination_id>")
class DestinationsItem(MethodView):
    """Destination item endpoints."""

    @blp.doc(parameters=[{
        "name": "destination_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "Destination ID"
    }])
    @blp.response(200, DestinationSchema)
    def get(self, destination_id: int):
        """Get destination by ID."""
        d = get_destination(destination_id)
        if not d:
            abort(404, message="Destination not found")
        return d

    @blp.doc(parameters=[{
        "name": "destination_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "Destination ID"
    }])
    @use_args(DestinationUpdateSchema, location="json")
    @blp.response(200, DestinationSchema)
    def patch(self, args, destination_id: int):
        """Update a destination."""
        d = update_destination(
            destination_id,
            name=args.get("name"),
            location=args.get("location"),
            arrival_date=args.get("arrival_date"),
            departure_date=args.get("departure_date"),
            notes=args.get("notes"),
        )
        if not d:
            abort(404, message="Destination not found")
        return d

    @blp.doc(parameters=[{
        "name": "destination_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "Destination ID"
    }])
    @blp.response(204)
    def delete(self, destination_id: int):
        """Delete a destination and cascade its activities."""
        ok = delete_destination(destination_id)
        if not ok:
            abort(404, message="Destination not found")
        return ""

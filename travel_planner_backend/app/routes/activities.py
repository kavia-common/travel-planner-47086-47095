from flask_smorest import Blueprint, abort
from flask.views import MethodView
from webargs.flaskparser import use_args
from webargs import fields as arg_fields
from ..schemas import ActivityCreateSchema, ActivityUpdateSchema, ActivitySchema
from ..models import (
    list_activities,
    create_activity,
    get_activity,
    update_activity,
    delete_activity,
)

blp = Blueprint(
    "Activities",
    "activities",
    url_prefix="/api/activities",
    description="Endpoints to manage activities linked to itineraries or destinations.",
)


@blp.route("")
class ActivitiesCollection(MethodView):
    """Activities collection endpoints."""

    @blp.arguments(
        {"itinerary_id": arg_fields.Int(required=False), "destination_id": arg_fields.Int(required=False)},
        location="query",
    )
    @blp.response(200, ActivitySchema(many=True))
    def get(self, args):
        """List activities, optionally filtering by itinerary_id or destination_id."""
        return list_activities(itinerary_id=args.get("itinerary_id"), destination_id=args.get("destination_id"))

    @use_args(ActivityCreateSchema, location="json")
    @blp.response(201, ActivitySchema)
    def post(self, args):
        """Create an activity linked to an itinerary or destination."""
        try:
            act = create_activity(
                name=args["name"],
                itinerary_id=args.get("itinerary_id"),
                destination_id=args.get("destination_id"),
                time=args.get("time"),
                details=args.get("details"),
            )
            return act
        except ValueError as e:
            abort(400, message=str(e))


@blp.route("/<int:activity_id>")
class ActivitiesItem(MethodView):
    """Activity item endpoints."""

    @blp.response(200, ActivitySchema)
    def get(self, activity_id: int):
        """Get activity by ID."""
        a = get_activity(activity_id)
        if not a:
            abort(404, message="Activity not found")
        return a

    @use_args(ActivityUpdateSchema, location="json")
    @blp.response(200, ActivitySchema)
    def patch(self, args, activity_id: int):
        """Update an activity."""
        try:
            a = update_activity(
                activity_id,
                name=args.get("name"),
                itinerary_id=args.get("itinerary_id"),
                destination_id=args.get("destination_id"),
                time=args.get("time"),
                details=args.get("details"),
            )
            if not a:
                abort(404, message="Activity not found")
            return a
        except ValueError as e:
            abort(400, message=str(e))

    @blp.response(204)
    def delete(self, activity_id: int):
        """Delete an activity."""
        ok = delete_activity(activity_id)
        if not ok:
            abort(404, message="Activity not found")
        return ""

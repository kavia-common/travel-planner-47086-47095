from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request
from webargs.flaskparser import use_args
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

    @blp.doc(
        summary="List activities with optional filters.",
        parameters=[
            {
                "name": "itinerary_id",
                "in": "query",
                "required": False,
                "schema": {"type": "integer"},
                "description": "Filter activities by itinerary ID",
            },
            {
                "name": "destination_id",
                "in": "query",
                "required": False,
                "schema": {"type": "integer"},
                "description": "Filter activities by destination ID",
            },
        ],
    )
    @blp.response(200, ActivitySchema(many=True))
    def get(self):
        """List activities, optionally filtering by itinerary_id or destination_id."""
        return list_activities(
            itinerary_id=request.args.get("itinerary_id", type=int),
            destination_id=request.args.get("destination_id", type=int),
        )

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

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from webargs.flaskparser import use_args
from ..schemas import UserCreateSchema, UserUpdateSchema, UserSchema
from ..models import (
    list_users,
    create_user,
    get_user,
    update_user,
    delete_user,
)

blp = Blueprint(
    "Users",
    "users",
    url_prefix="/api/users",
    description="Endpoints to manage users (placeholder until auth is integrated).",
)


@blp.route("")
class UsersCollection(MethodView):
    """Users collection endpoints."""

    @blp.response(200, UserSchema(many=True))
    def get(self):
        """List users."""
        return list_users()

    @use_args(UserCreateSchema, location="json")
    @blp.response(201, UserSchema)
    def post(self, args):
        """Create a new user."""
        user = create_user(name=args["name"], email=args["email"])
        return user


@blp.route("/<int:user_id>")
class UsersItem(MethodView):
    """User item endpoints."""

    @blp.doc(parameters=[{
        "name": "user_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "User ID"
    }])
    @blp.response(200, UserSchema)
    def get(self, user_id: int):
        """Get a user by ID."""
        u = get_user(user_id)
        if not u:
            abort(404, message="User not found")
        return u

    @blp.doc(parameters=[{
        "name": "user_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "User ID"
    }])
    @use_args(UserUpdateSchema, location="json")
    @blp.response(200, UserSchema)
    def patch(self, args, user_id: int):
        """Update a user."""
        u = update_user(user_id, name=args.get("name"), email=args.get("email"))
        if not u:
            abort(404, message="User not found")
        return u

    @blp.doc(parameters=[{
        "name": "user_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "User ID"
    }])
    @blp.response(204)
    def delete(self, user_id: int):
        """Delete a user."""
        ok = delete_user(user_id)
        if not ok:
            abort(404, message="User not found")
        return ""

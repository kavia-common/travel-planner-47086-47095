"""
Marshmallow schemas for Travel Planner API.

These schemas are used by flask-smorest to validate payloads and generate OpenAPI spec.
"""

from marshmallow import Schema, fields, validate

# Basic reusable fields
name_field = fields.String(required=True, validate=validate.Length(min=1, max=255))
desc_field = fields.String(required=False, allow_none=True, validate=validate.Length(max=2000))


class UserCreateSchema(Schema):
    name = name_field
    email = fields.Email(required=True)


class UserUpdateSchema(Schema):
    name = fields.String(required=False, validate=validate.Length(min=1, max=255))
    email = fields.Email(required=False)


class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)


class TripCreateSchema(Schema):
    title = name_field
    description = desc_field
    user_id = fields.Int(required=False, allow_none=True, description="Owner user ID (optional placeholder)")
    start_date = fields.String(required=False, allow_none=True, description="ISO date YYYY-MM-DD")
    end_date = fields.String(required=False, allow_none=True, description="ISO date YYYY-MM-DD")


class TripUpdateSchema(Schema):
    title = fields.String(required=False, validate=validate.Length(min=1, max=255))
    description = desc_field
    user_id = fields.Int(required=False, allow_none=True)
    start_date = fields.String(required=False, allow_none=True)
    end_date = fields.String(required=False, allow_none=True)


class TripSchema(Schema):
    id = fields.Int()
    title = fields.String()
    description = fields.String(allow_none=True)
    user_id = fields.Int(allow_none=True)
    start_date = fields.String(allow_none=True)
    end_date = fields.String(allow_none=True)


class ItineraryCreateSchema(Schema):
    trip_id = fields.Int(required=True)
    name = name_field
    start_date = fields.String(required=False, allow_none=True)
    end_date = fields.String(required=False, allow_none=True)
    notes = desc_field


class ItineraryUpdateSchema(Schema):
    name = fields.String(required=False, validate=validate.Length(min=1, max=255))
    start_date = fields.String(required=False, allow_none=True)
    end_date = fields.String(required=False, allow_none=True)
    notes = desc_field


class ItinerarySchema(Schema):
    id = fields.Int()
    trip_id = fields.Int()
    name = fields.String()
    start_date = fields.String(allow_none=True)
    end_date = fields.String(allow_none=True)
    notes = fields.String(allow_none=True)


class DestinationCreateSchema(Schema):
    itinerary_id = fields.Int(required=True)
    name = name_field
    location = fields.String(required=False, allow_none=True, validate=validate.Length(max=255))
    arrival_date = fields.String(required=False, allow_none=True)
    departure_date = fields.String(required=False, allow_none=True)
    notes = desc_field


class DestinationUpdateSchema(Schema):
    name = fields.String(required=False, validate=validate.Length(min=1, max=255))
    location = fields.String(required=False, allow_none=True, validate=validate.Length(max=255))
    arrival_date = fields.String(required=False, allow_none=True)
    departure_date = fields.String(required=False, allow_none=True)
    notes = desc_field


class DestinationSchema(Schema):
    id = fields.Int()
    itinerary_id = fields.Int()
    name = fields.String()
    location = fields.String(allow_none=True)
    arrival_date = fields.String(allow_none=True)
    departure_date = fields.String(allow_none=True)
    notes = fields.String(allow_none=True)


class ActivityCreateSchema(Schema):
    name = name_field
    itinerary_id = fields.Int(required=False, allow_none=True)
    destination_id = fields.Int(required=False, allow_none=True)
    time = fields.String(required=False, allow_none=True)
    details = desc_field


class ActivityUpdateSchema(Schema):
    name = fields.String(required=False, validate=validate.Length(min=1, max=255))
    itinerary_id = fields.Int(required=False, allow_none=True)
    destination_id = fields.Int(required=False, allow_none=True)
    time = fields.String(required=False, allow_none=True)
    details = desc_field


class ActivitySchema(Schema):
    id = fields.Int()
    name = fields.String()
    itinerary_id = fields.Int(allow_none=True)
    destination_id = fields.Int(allow_none=True)
    time = fields.String(allow_none=True)
    details = fields.String(allow_none=True)

"""
Routes package initializer.

Exports blueprint objects for convenient imports and registration.
"""

# PUBLIC_INTERFACE
def get_registered_blueprints():
    """Return a dict of available route blueprints keyed by name."""
    from .health import blp as health_blp
    from .users import blp as users_blp
    from .trips import blp as trips_blp
    from .itineraries import blp as itineraries_blp
    from .destinations import blp as destinations_blp
    from .activities import blp as activities_blp

    return {
        "health": health_blp,
        "users": users_blp,
        "trips": trips_blp,
        "itineraries": itineraries_blp,
        "destinations": destinations_blp,
        "activities": activities_blp,
    }

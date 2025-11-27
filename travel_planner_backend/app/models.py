"""
Domain models and in-memory persistence for the Travel Planner backend.

Note:
- This version uses an in-memory store for simplicity. It includes clear TODOs and
  environment variable placeholders for future database integration using SQLAlchemy.
- IDs are simple incrementing integers scoped per model.
- Relationships:
  - Trip belongs to User (optional placeholder).
  - Itinerary belongs to Trip.
  - Destination belongs to Itinerary.
  - Activity belongs to Destination OR Itinerary (one of them is required).
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, List
import threading
import os

# Configuration placeholders (do not assume values; to be provided via .env)
# Example expected env vars for future DB integration:
# - DATABASE_URL (SQLAlchemy URL), or service-specific variables if a DB container is added.
DB_URL = os.getenv("DATABASE_URL", None)  # Not used in this in-memory implementation
USE_IN_MEMORY = os.getenv("USE_IN_MEMORY_STORE", "true").lower() != "false"  # default True


class _IdGenerator:
    """Thread-safe simple incremental ID generator."""
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._id = 0

    def next(self) -> int:
        with self._lock:
            self._id += 1
            return self._id


# In-memory "database"
_USERS: Dict[int, dict] = {}
_TRIPS: Dict[int, dict] = {}
_ITINERARIES: Dict[int, dict] = {}
_DESTINATIONS: Dict[int, dict] = {}
_ACTIVITIES: Dict[int, dict] = {}

_USERS_ID = _IdGenerator()
_TRIPS_ID = _IdGenerator()
_ITINERARIES_ID = _IdGenerator()
_DESTINATIONS_ID = _IdGenerator()
_ACTIVITIES_ID = _IdGenerator()


@dataclass
class User:
    id: int
    name: str
    email: str


@dataclass
class Trip:
    id: int
    user_id: Optional[int]
    title: str
    description: Optional[str] = ""
    start_date: Optional[str] = None  # ISO date string
    end_date: Optional[str] = None    # ISO date string


@dataclass
class Itinerary:
    id: int
    trip_id: int
    name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    notes: Optional[str] = ""


@dataclass
class Destination:
    id: int
    itinerary_id: int
    name: str
    location: Optional[str] = ""
    arrival_date: Optional[str] = None
    departure_date: Optional[str] = None
    notes: Optional[str] = ""


@dataclass
class Activity:
    id: int
    itinerary_id: Optional[int]
    destination_id: Optional[int]
    name: str
    time: Optional[str] = None  # ISO datetime string or freeform
    details: Optional[str] = ""


def _save(store: Dict[int, dict], obj) -> dict:
    """Save dataclass object into the given store as a dict."""
    data = asdict(obj)
    store[obj.id] = data
    return data


# PUBLIC_INTERFACE
def list_users() -> List[dict]:
    """List all users from the in-memory store."""
    return list(_USERS.values())


# PUBLIC_INTERFACE
def create_user(name: str, email: str) -> dict:
    """Create a new user with basic validation."""
    uid = _users_next_id()
    user = User(id=uid, name=name.strip(), email=email.strip())
    return _save(_USERS, user)


# PUBLIC_INTERFACE
def get_user(user_id: int) -> Optional[dict]:
    """Get a user by ID or None."""
    return _USERS.get(user_id)


# PUBLIC_INTERFACE
def update_user(user_id: int, name: Optional[str], email: Optional[str]) -> Optional[dict]:
    """Update a user if exists."""
    u = _USERS.get(user_id)
    if not u:
        return None
    if name is not None:
        u["name"] = name.strip()
    if email is not None:
        u["email"] = email.strip()
    _USERS[user_id] = u
    return u


# PUBLIC_INTERFACE
def delete_user(user_id: int) -> bool:
    """Delete a user; returns True if deleted."""
    return _USERS.pop(user_id, None) is not None


# PUBLIC_INTERFACE
def list_trips() -> List[dict]:
    """List all trips."""
    return list(_TRIPS.values())


# PUBLIC_INTERFACE
def create_trip(title: str, description: Optional[str], user_id: Optional[int], start_date: Optional[str], end_date: Optional[str]) -> dict:
    """Create a trip. If user_id is provided, ensure user exists."""
    if user_id is not None and user_id not in _USERS:
        raise ValueError("User not found")
    tid = _trips_next_id()
    trip = Trip(
        id=tid,
        user_id=user_id,
        title=title.strip(),
        description=(description or "").strip(),
        start_date=start_date,
        end_date=end_date,
    )
    return _save(_TRIPS, trip)


# PUBLIC_INTERFACE
def get_trip(trip_id: int) -> Optional[dict]:
    """Get a trip by ID."""
    return _TRIPS.get(trip_id)


# PUBLIC_INTERFACE
def update_trip(trip_id: int, title: Optional[str], description: Optional[str], user_id: Optional[int], start_date: Optional[str], end_date: Optional[str]) -> Optional[dict]:
    """Update a trip if exists. Validate user when provided."""
    t = _TRIPS.get(trip_id)
    if not t:
        return None
    if user_id is not None:
        if user_id not in _USERS:
            raise ValueError("User not found")
        t["user_id"] = user_id
    if title is not None:
        t["title"] = title.strip()
    if description is not None:
        t["description"] = description.strip()
    if start_date is not None:
        t["start_date"] = start_date
    if end_date is not None:
        t["end_date"] = end_date
    _TRIPS[trip_id] = t
    return t


# PUBLIC_INTERFACE
def delete_trip(trip_id: int) -> bool:
    """Delete a trip and cascade delete itineraries/destinations/activities within."""
    if trip_id not in _TRIPS:
        return False
    # cascade for itineraries
    to_delete_itins = [i["id"] for i in _ITINERARIES.values() if i["trip_id"] == trip_id]
    for iid in to_delete_itins:
        delete_itinerary(iid)
    _TRIPS.pop(trip_id, None)
    return True


# PUBLIC_INTERFACE
def list_itineraries(trip_id: Optional[int] = None) -> List[dict]:
    """List itineraries optionally filtered by trip_id."""
    if trip_id is None:
        return list(_ITINERARIES.values())
    return [i for i in _ITINERARIES.values() if i["trip_id"] == trip_id]


# PUBLIC_INTERFACE
def create_itinerary(trip_id: int, name: str, start_date: Optional[str], end_date: Optional[str], notes: Optional[str]) -> dict:
    """Create itinerary within a trip."""
    if trip_id not in _TRIPS:
        raise ValueError("Trip not found")
    iid = _itineraries_next_id()
    it = Itinerary(
        id=iid,
        trip_id=trip_id,
        name=name.strip(),
        start_date=start_date,
        end_date=end_date,
        notes=(notes or "").strip(),
    )
    return _save(_ITINERARIES, it)


# PUBLIC_INTERFACE
def get_itinerary(itinerary_id: int) -> Optional[dict]:
    """Get itinerary by ID."""
    return _ITINERARIES.get(itinerary_id)


# PUBLIC_INTERFACE
def update_itinerary(itinerary_id: int, name: Optional[str], start_date: Optional[str], end_date: Optional[str], notes: Optional[str]) -> Optional[dict]:
    """Update itinerary."""
    it = _ITINERARIES.get(itinerary_id)
    if not it:
        return None
    if name is not None:
        it["name"] = name.strip()
    if start_date is not None:
        it["start_date"] = start_date
    if end_date is not None:
        it["end_date"] = end_date
    if notes is not None:
        it["notes"] = notes.strip()
    _ITINERARIES[itinerary_id] = it
    return it


# PUBLIC_INTERFACE
def delete_itinerary(itinerary_id: int) -> bool:
    """Delete itinerary and cascade delete destinations and activities within."""
    if itinerary_id not in _ITINERARIES:
        return False
    # cascade destinations
    to_delete_dest = [d["id"] for d in _DESTINATIONS.values() if d["itinerary_id"] == itinerary_id]
    for did in to_delete_dest:
        delete_destination(did)
    # cascade activities linked directly to itinerary
    to_delete_acts = [a["id"] for a in _ACTIVITIES.values() if a.get("itinerary_id") == itinerary_id]
    for aid in to_delete_acts:
        _ACTIVITIES.pop(aid, None)
    _ITINERARIES.pop(itinerary_id, None)
    return True


# PUBLIC_INTERFACE
def list_destinations(itinerary_id: Optional[int] = None) -> List[dict]:
    """List destinations optionally filtered by itinerary_id."""
    if itinerary_id is None:
        return list(_DESTINATIONS.values())
    return [d for d in _DESTINATIONS.values() if d["itinerary_id"] == itinerary_id]


# PUBLIC_INTERFACE
def create_destination(itinerary_id: int, name: str, location: Optional[str], arrival_date: Optional[str], departure_date: Optional[str], notes: Optional[str]) -> dict:
    """Create destination within itinerary."""
    if itinerary_id not in _ITINERARIES:
        raise ValueError("Itinerary not found")
    did = _destinations_next_id()
    dest = Destination(
        id=did,
        itinerary_id=itinerary_id,
        name=name.strip(),
        location=(location or "").strip(),
        arrival_date=arrival_date,
        departure_date=departure_date,
        notes=(notes or "").strip(),
    )
    return _save(_DESTINATIONS, dest)


# PUBLIC_INTERFACE
def get_destination(destination_id: int) -> Optional[dict]:
    """Get destination by ID."""
    return _DESTINATIONS.get(destination_id)


# PUBLIC_INTERFACE
def update_destination(destination_id: int, name: Optional[str], location: Optional[str], arrival_date: Optional[str], departure_date: Optional[str], notes: Optional[str]) -> Optional[dict]:
    """Update destination."""
    d = _DESTINATIONS.get(destination_id)
    if not d:
        return None
    if name is not None:
        d["name"] = name.strip()
    if location is not None:
        d["location"] = location.strip()
    if arrival_date is not None:
        d["arrival_date"] = arrival_date
    if departure_date is not None:
        d["departure_date"] = departure_date
    if notes is not None:
        d["notes"] = notes.strip()
    _DESTINATIONS[destination_id] = d
    return d


# PUBLIC_INTERFACE
def delete_destination(destination_id: int) -> bool:
    """Delete destination and cascade delete activities within."""
    if destination_id not in _DESTINATIONS:
        return False
    to_delete_acts = [a["id"] for a in _ACTIVITIES.values() if a.get("destination_id") == destination_id]
    for aid in to_delete_acts:
        _ACTIVITIES.pop(aid, None)
    _DESTINATIONS.pop(destination_id, None)
    return True


# PUBLIC_INTERFACE
def list_activities(itinerary_id: Optional[int] = None, destination_id: Optional[int] = None) -> List[dict]:
    """List activities optionally filtered by itinerary_id or destination_id."""
    results = list(_ACTIVITIES.values())
    if itinerary_id is not None:
        results = [a for a in results if a.get("itinerary_id") == itinerary_id]
    if destination_id is not None:
        results = [a for a in results if a.get("destination_id") == destination_id]
    return results


# PUBLIC_INTERFACE
def create_activity(name: str, itinerary_id: Optional[int], destination_id: Optional[int], time: Optional[str], details: Optional[str]) -> dict:
    """Create an activity; requires at least itinerary_id or destination_id to be valid."""
    if itinerary_id is None and destination_id is None:
        raise ValueError("Either itinerary_id or destination_id is required")
    if itinerary_id is not None and itinerary_id not in _ITINERARIES:
        raise ValueError("Itinerary not found")
    if destination_id is not None and destination_id not in _DESTINATIONS:
        raise ValueError("Destination not found")
    aid = _activities_next_id()
    act = Activity(
        id=aid,
        itinerary_id=itinerary_id,
        destination_id=destination_id,
        name=name.strip(),
        time=time,
        details=(details or "").strip(),
    )
    return _save(_ACTIVITIES, act)


# PUBLIC_INTERFACE
def get_activity(activity_id: int) -> Optional[dict]:
    """Get activity by ID."""
    return _ACTIVITIES.get(activity_id)


# PUBLIC_INTERFACE
def update_activity(activity_id: int, name: Optional[str], itinerary_id: Optional[int], destination_id: Optional[int], time: Optional[str], details: Optional[str]) -> Optional[dict]:
    """Update an activity and validate foreign keys when provided."""
    a = _ACTIVITIES.get(activity_id)
    if not a:
        return None
    if itinerary_id is not None:
        if itinerary_id not in _ITINERARIES:
            raise ValueError("Itinerary not found")
        a["itinerary_id"] = itinerary_id
    if destination_id is not None:
        if destination_id not in _DESTINATIONS:
            raise ValueError("Destination not found")
        a["destination_id"] = destination_id
    if name is not None:
        a["name"] = name.strip()
    if time is not None:
        a["time"] = time
    if details is not None:
        a["details"] = details.strip()
    _ACTIVITIES[activity_id] = a
    return a


# PUBLIC_INTERFACE
def delete_activity(activity_id: int) -> bool:
    """Delete an activity by ID."""
    return _ACTIVITIES.pop(activity_id, None) is not None


def _users_next_id() -> int:
    return _USERS_ID.next()


def _trips_next_id() -> int:
    return _TRIPS_ID.next()


def _itineraries_next_id() -> int:
    return _ITINERARIES_ID.next()


def _destinations_next_id() -> int:
    return _DESTINATIONS_ID.next()


def _activities_next_id() -> int:
    return _ACTIVITIES_ID.next()

import json
import os
from app import create_app

"""
Run this to regenerate OpenAPI JSON:
    cd travel_planner_backend
    python generate_openapi.py
"""

app = create_app()

with app.app_context():
    # flask-smorest stores the spec in the Api instance; we saved it in app.extensions
    api = app.extensions.get("smorest_api")
    openapi_spec = api.spec.to_dict() if api else {}

    output_dir = "interfaces"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")

    with open(output_path, "w") as f:
        json.dump(openapi_spec, f, indent=2)

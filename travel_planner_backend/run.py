from app import create_app
import os

# Create the Flask application via factory. This import is intentionally minimal to keep startup fast.
app = create_app()

# PUBLIC_INTERFACE
def main():
    """Entrypoint to start the Flask development server.

    Notes:
    - Binds to 0.0.0.0:3001 to satisfy container health checks and previews.
    - Avoids enabling debug or reloader in production environments.
    - For container runtime, ensure FLASK_ENV is not set to 'development'.

    Environment variables:
    - PORT (optional): override the default 3001 port.
    """
    port = int(os.getenv("PORT", "3001"))
    # Do not enable reloader or debug; keep startup minimal.
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    # For local dev you can run:
    #   python run.py
    # Or using Flask CLI:
    #   FLASK_APP=app:create_app flask run --host=0.0.0.0 --port=3001
    main()

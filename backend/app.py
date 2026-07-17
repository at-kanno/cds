"""Entry point for the ITIL4 backend with Flutter API support."""

from dotenv import load_dotenv

load_dotenv()

from index import app  # noqa: E402,F401

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)

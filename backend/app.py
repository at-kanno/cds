"""Entry point for the ITIL4 backend with Flutter API support."""

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    import sys
    from pathlib import Path

    venv_python = Path(__file__).resolve().parent / ".venv" / "Scripts" / "python.exe"
    raise SystemExit(
        "python-dotenv is not installed for the Python PyCharm is using.\n"
        f"  Current Python: {sys.executable}\n"
        f"  Expected venv : {venv_python}\n"
        "  Fix: File → Settings → Project: cds → Python Interpreter\n"
        "       Select Existing → backend\\.venv\\Scripts\\python.exe"
    ) from None

load_dotenv(override=True)

import sys


def _configure_stdio_utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


_configure_stdio_utf8()

from index import app  # noqa: E402,F401
import constant  # noqa: E402

if __name__ == "__main__":
    import os

    print(f"APP_PROFILE={os.environ.get('APP_PROFILE', 'CDS')}")
    print(f"DB_PATH={constant.db_path}")

    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)

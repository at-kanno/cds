import os

from werkzeug.middleware.proxy_fix import ProxyFix


class ScriptNameMiddleware:
    """Set WSGI SCRIPT_NAME so Flask generates /cds/... URLs behind a reverse proxy."""

    def __init__(self, app, script_name: str):
        self.app = app
        self.script_name = script_name.rstrip("/")

    def __call__(self, environ, start_response):
        if self.script_name:
            environ["SCRIPT_NAME"] = self.script_name
        return self.app(environ, start_response)


def apply_middleware(app):
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    script_name = os.environ.get("SCRIPT_NAME", "").strip()
    if script_name:
        app.wsgi_app = ScriptNameMiddleware(app.wsgi_app, script_name)

    return app

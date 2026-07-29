from werkzeug.middleware.proxy_fix import ProxyFix


def apply_middleware(app):
    # Apache strips /cds before proxying and sends X-Forwarded-Prefix: /cds.
    # Do NOT set SCRIPT_NAME in gunicorn/systemd; ProxyFix reads the header.
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_prefix=1,
    )
    return app

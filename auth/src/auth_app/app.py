from apiflask import APIFlask
from auth_app import admin, commands, user, social
from auth_app.extensions import db, jwt, redis_client, flask_instrumentator, limiter
from auth_app.tracing import configure_tracer
from flask import request


def create_app(config_object="auth_app.config.config"):
    app = APIFlask(
        __name__, title="Auth-service", root_path="/auth", spec_path="/auth/openapi.yaml", docs_path="/auth/docs"
    )
    app.config.from_object(config_object)
    app.security_schemes = {"BearerAuth": {"scheme": "bearer", "type": "http"}}
    if app.config["ENABLE_TRACING"]:
        configure_tracer()
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    @app.before_request
    def before_request():
        if not app.config["DEBUG"]:
            request_id = request.headers.get("X-Request-Id")
            if not request_id:
                raise RuntimeError("X-Request-Id header is required")

    return app


def register_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    redis_client.init_app(app)
    flask_instrumentator.instrument_app(app)
    limiter.init_app(app)


def register_blueprints(app):
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(admin.views.blueprint)
    app.register_blueprint(social.views.blueprint)


def register_commands(app):
    app.cli.add_command(commands.create_superuser)

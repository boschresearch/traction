from flask import Flask


from config import Config
from extensions import db, migrate, api
from api.resources.liveness import LivenessResource
from api.resources.tenant import (
    TenantListResource,
    TenantResource,
    TenantAccessKeyListResource,
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_resources(app):
    api.add_resource(LivenessResource, "/")
    api.add_resource(TenantListResource, "/tenants")
    api.add_resource(TenantResource, "/tenants/<uuid:tenant_id>")
    api.add_resource(TenantAccessKeyListResource, "/tenants/<uuid:tenant_id>/keys")
    api.init_app(app)
from flask import Flask, jsonify
from flasgger import Swagger

from .config import Config
from .extensions import db
from .routes import api_bp
from .models import Company


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)


    app.config.setdefault(
        "SWAGGER",
        {
            "title": "Cloud Labs Mining API",
            "uiversion": 3,
            "specs_route": "/api/docs/", 
        },
    )

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Cloud Labs Mining API",
            "version": "1.0.0",
            "description": "REST API",
        },
        "basePath": "/",
        "schemes": ["https", "http"],
    }

 
    db.init_app(app)
    print("SQLALCHEMY_DATABASE_URI =", app.config.get("SQLALCHEMY_DATABASE_URI"))


    with app.app_context():
        db.create_all()
        if not Company.query.first():
            default_company = Company(name="Default company")
            db.session.add(default_company)
            db.session.commit()
            print("Created default company with id", default_company.id)

    # Swagger
    Swagger(app, template=swagger_template)

    # API
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def health():
        return jsonify(
            {
                "status": "ok",
                "message": "Mining backend is running",
                "docs_url": "/api/docs/",
                "api_root": "/api",
            }
        )

    return app

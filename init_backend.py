"""
Simple one-shot bootstrap script.

Usage:

    python init_backend.py

It will create the following structure in the current directory:

    db/schema.yml
    backend/
      __init__.py
      run.py
      app/
        __init__.py
        config.py
        extensions.py
        models.py
        routes.py
    requirements.txt

After that you can:

    python -m venv venv
    source venv/bin/activate   # on Windows: venv\Scripts\activate
    pip install -r requirements.txt
    cd backend
    python run.py

You should see the service running on http://127.0.0.1:5000
Swagger UI will be available at http://127.0.0.1:5000/apidocs/
"""

from pathlib import Path

PROJECT_FILES = {
    "db/schema.yml": '\n'
"tables:\n"
"  companies:\n"
"    description: \"Mining companies operating multiple quarries.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      name:\n"
"        type: string(255)\n"
"        nullable: false\n"
"      registration_number:\n"
"        type: string(50)\n"
"        nullable: true\n"
"      country:\n"
"        type: string(100)\n"
"        nullable: true\n"
"      city:\n"
"        type: string(100)\n"
"        nullable: true\n"
"      status:\n"
"        type: string(20)\n"
"        nullable: false\n"
"        default: \"active\"\n"
"    indexes:\n"
"      - [name]\n"
"\n"
"  quarries:\n"
"    description: \"Quarries where vehicles operate.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      company_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: companies.id\n"
"      name:\n"
"        type: string(255)\n"
"        nullable: false\n"
"      location:\n"
"        type: string(255)\n"
"        nullable: true\n"
"      status:\n"
"        type: string(20)\n"
"        nullable: false\n"
"        default: \"active\"\n"
"    indexes:\n"
"      - [company_id]\n"
"      - [status]\n"
"\n"
"  vehicle_types:\n"
"    description: \"Reference table with available vehicle types.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      name:\n"
"        type: string(100)\n"
"        nullable: false\n"
"      description:\n"
"        type: text\n"
"        nullable: true\n"
"      max_speed_kmh:\n"
"        type: integer\n"
"        nullable: true\n"
"      max_payload_tons:\n"
"        type: float\n"
"        nullable: true\n"
"\n"
"  vehicles:\n"
"    description: \"Physical vehicles working in quarries.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      company_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: companies.id\n"
"      vehicle_type_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: vehicle_types.id\n"
"      current_quarry_id:\n"
"        type: integer\n"
"        nullable: true\n"
"        foreign_key: quarries.id\n"
"      plate_number:\n"
"        type: string(50)\n"
"        nullable: false\n"
"        unique: true\n"
"      vin:\n"
"        type: string(100)\n"
"        nullable: true\n"
"        unique: true\n"
"      status:\n"
"        type: string(20)\n"
"        nullable: false\n"
"        default: \"active\"\n"
"    indexes:\n"
"      - [company_id]\n"
"      - [current_quarry_id]\n"
"      - [status]\n"
"\n"
"  drivers:\n"
"    description: \"Drivers who operate vehicles.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      company_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: companies.id\n"
"      full_name:\n"
"        type: string(255)\n"
"        nullable: false\n"
"      license_number:\n"
"        type: string(100)\n"
"        nullable: true\n"
"      license_category:\n"
"        type: string(10)\n"
"        nullable: true\n"
"      status:\n"
"        type: string(20)\n"
"        nullable: false\n"
"        default: \"active\"\n"
"      date_of_birth:\n"
"        type: date\n"
"        nullable: true\n"
"    indexes:\n"
"      - [company_id]\n"
"      - [status]\n"
"\n"
"  driver_assignments:\n"
"    description: \"History of which quarry a driver belongs to.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      driver_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: drivers.id\n"
"      quarry_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: quarries.id\n"
"      start_date:\n"
"        type: date\n"
"        nullable: false\n"
"      end_date:\n"
"        type: date\n"
"        nullable: true\n"
"    indexes:\n"
"      - [driver_id]\n"
"      - [quarry_id]\n"
"\n"
"  shifts:\n"
"    description: \"Work shifts in each quarry.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      quarry_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: quarries.id\n"
"      shift_date:\n"
"        type: date\n"
"        nullable: false\n"
"      start_time:\n"
"        type: time\n"
"        nullable: false\n"
"      end_time:\n"
"        type: time\n"
"        nullable: false\n"
"    indexes:\n"
"      - [quarry_id, shift_date]\n"
"\n"
"  medical_checks:\n"
"    description: \"Pre-shift medical checks for drivers.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      driver_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: drivers.id\n"
"      shift_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: shifts.id\n"
"      check_time:\n"
"        type: datetime\n"
"        nullable: false\n"
"      result:\n"
"        type: string(20)\n"
"        nullable: false\n"
"      heart_rate:\n"
"        type: integer\n"
"        nullable: true\n"
"      blood_pressure:\n"
"        type: string(20)\n"
"        nullable: true\n"
"      notes:\n"
"        type: text\n"
"        nullable: true\n"
"    indexes:\n"
"      - [driver_id]\n"
"      - [shift_id]\n"
"      - [result]\n"
"\n"
"  driver_health_statuses:\n"
"    description: \"Reference table for driver health statuses.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      code:\n"
"        type: string(50)\n"
"        nullable: false\n"
"        unique: true\n"
"      description:\n"
"        type: string(255)\n"
"        nullable: true\n"
"\n"
"  vehicle_shift_assignments:\n"
"    description: \"Which driver used which vehicle in which shift and quarry.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      vehicle_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: vehicles.id\n"
"      driver_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: drivers.id\n"
"      shift_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: shifts.id\n"
"      quarry_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: quarries.id\n"
"      start_time:\n"
"        type: datetime\n"
"        nullable: false\n"
"      end_time:\n"
"        type: datetime\n"
"        nullable: true\n"
"    indexes:\n"
"      - [vehicle_id]\n"
"      - [driver_id]\n"
"      - [shift_id]\n"
"      - [quarry_id]\n"
"\n"
"  telematics_readings:\n"
"    description: \"5-minute sensor data from vehicles.\"\n"
"    columns:\n"
"      id:\n"
"        type: integer\n"
"        primary_key: true\n"
"        autoincrement: true\n"
"      vehicle_id:\n"
"        type: integer\n"
"        nullable: false\n"
"        foreign_key: vehicles.id\n"
"      driver_id:\n"
"        type: integer\n"
"        nullable: true\n"
"        foreign_key: drivers.id\n"
"      shift_id:\n"
"        type: integer\n"
"        nullable: true\n"
"        foreign_key: shifts.id\n"
"      timestamp:\n"
"        type: datetime\n"
"        nullable: false\n"
"      latitude:\n"
"        type: float\n"
"        nullable: true\n"
"      longitude:\n"
"        type: float\n"
"        nullable: true\n"
"      speed_kmh:\n"
"        type: float\n"
"        nullable: true\n"
"      driver_health_status_id:\n"
"        type: integer\n"
"        nullable: true\n"
"        foreign_key: driver_health_statuses.id\n"
"      raw_payload:\n"
"        type: text\n"
"        nullable: true\n"
"    indexes:\n"
"      - [vehicle_id, timestamp]\n"
"      - [driver_id, timestamp]\n"
"      - [shift_id, timestamp]\n",
    "backend/__init__.py": '# This file marks \"backend\" as a Python package.\n',
    "backend/run.py": '\n'
'from app import create_app\n'
'\n'
'app = create_app()\n'
'\n'
'if __name__ == "__main__":\n'
'    # Development entry point.\n'
'    # In production you should use a proper WSGI server like gunicorn.\n'
'    app.run(host="0.0.0.0", port=5000, debug=True)\n',
    "backend/app/__init__.py": '\n'
'from flask import Flask, jsonify\n'
'from flasgger import Swagger\n'
'from .config import Config\n'
'from .extensions import db\n'
'from . import models  # noqa: F401  - ensure models are imported\n'
'from .routes import api_bp\n'
'\n'
'\n'
'def create_app() -> Flask:\n'
'    """Application factory.\n'
'\n'
'    This function creates and configures the Flask application,\n'
'    initializes the database and registers all API routes.\n'
'    """\n'
'    app = Flask(__name__)\n'
'    app.config.from_object(Config)\n'
'\n'
'    # Initialize extensions\n'
'    db.init_app(app)\n'
'\n'
'    # Register blueprints\n'
'    app.register_blueprint(api_bp, url_prefix="/api")\n'
'\n'
'    # Simple health check\n'
'    @app.route("/health", methods=["GET"])\n'
'    def health():\n'
'        """Health check endpoint."""\n'
'        return jsonify({"status": "ok"})\n'
'\n'
'    # Root endpoint\n'
'    @app.route("/", methods=["GET"])\n'
'    def index():\n'
'        """Root endpoint with a short description."""\n'
'        return jsonify(\n'
'            {\n'
'                "service": "Mining fleet monitoring API",\n'
'                "docs": "/apidocs/",\n'
'                "api_prefix": "/api",\n'
'            }\n'
'        )\n'
'\n'
'    # Initialize Swagger after routes are registered\n'
'    Swagger(\n'
'        app,\n'
'        template={\n'
'            "info": {\n'
'                "title": "Mining Fleet Monitoring API",\n'
'                "description": "REST API for managing mining companies, quarries, "\n'
'                "vehicles, drivers and telemetry data.",\n'
'                "version": "1.0.0",\n'
'            },\n'
'            "tags": [\n'
'                {"name": "Drivers", "description": "Operations with drivers."},\n'
'                {"name": "Vehicles", "description": "Operations with vehicles."},\n'
'                {\n'
'                    "name": "Telemetry",\n'
'                    "description": "Operations with telematics data from sensors.",\n'
'                },\n'
'            ],\n'
'        },\n'
'    )\n'
'\n'
'    # Create all tables if they do not exist yet\n'
'    with app.app_context():\n'
'        db.create_all()\n'
'\n'
'    return app\n',
    "backend/app/config.py": '\n'
'import os\n'
'\n'
'BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))\n'
'\n'
'\n'
'class Config:\n'
'    """Application configuration.\n'
'\n'
'    By default the service uses a local SQLite database so that it can\n'
'    start without any extra dependencies. In production you can override\n'
'    DB connection using the DB_URI environment variable.\n'
'    """\n'
'\n'
'    SQLALCHEMY_DATABASE_URI = os.getenv(\n'
"        \"DB_URI\", f\"sqlite:///{os.path.join(BASE_DIR, 'mining.db')}\"\n"
'    )\n'
'    SQLALCHEMY_TRACK_MODIFICATIONS = False\n'
'    DEBUG = True\n',
    "backend/app/extensions.py": '\n'
'from flask_sqlalchemy import SQLAlchemy\n'
'\n'
'db = SQLAlchemy()\n',
    "backend/app/models.py": '\n'
'from datetime import datetime\n'
'from .extensions import db\n'
'\n'
'\n'
'class Company(db.Model):\n'
'    __tablename__ = "companies"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    name = db.Column(db.String(255), nullable=False)\n'
'    registration_number = db.Column(db.String(50))\n'
'    country = db.Column(db.String(100))\n'
'    city = db.Column(db.String(100))\n'
'    status = db.Column(db.String(20), nullable=False, default="active")\n'
'\n'
'    quarries = db.relationship("Quarry", back_populates="company", lazy="dynamic")\n'
'    vehicles = db.relationship("Vehicle", back_populates="company", lazy="dynamic")\n'
'    drivers = db.relationship("Driver", back_populates="company", lazy="dynamic")\n'
'\n'
'\n'
'class Quarry(db.Model):\n'
'    __tablename__ = "quarries"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)\n'
'    name = db.Column(db.String(255), nullable=False)\n'
'    location = db.Column(db.String(255))\n'
'    status = db.Column(db.String(20), nullable=False, default="active")\n'
'\n'
'    company = db.relationship("Company", back_populates="quarries")\n'
'    shifts = db.relationship("Shift", back_populates="quarry", lazy="dynamic")\n'
'    driver_assignments = db.relationship(\n'
'        "DriverAssignment", back_populates="quarry", lazy="dynamic"\n'
'    )\n'
'    vehicle_shift_assignments = db.relationship(\n'
'        "VehicleShiftAssignment", back_populates="quarry", lazy="dynamic"\n'
'    )\n'
'\n'
'\n'
'class VehicleType(db.Model):\n'
'    __tablename__ = "vehicle_types"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    name = db.Column(db.String(100), nullable=False)\n'
'    description = db.Column(db.Text)\n'
'    max_speed_kmh = db.Column(db.Integer)\n'
'    max_payload_tons = db.Column(db.Float)\n'
'\n'
'    vehicles = db.relationship("Vehicle", back_populates="vehicle_type", lazy="dynamic")\n'
'\n'
'\n'
'class Vehicle(db.Model):\n'
'    __tablename__ = "vehicles"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)\n'
'    vehicle_type_id = db.Column(\n'
'        db.Integer, db.ForeignKey("vehicle_types.id"), nullable=False\n'
'    )\n'
'    current_quarry_id = db.Column(db.Integer, db.ForeignKey("quarries.id"))\n'
'    plate_number = db.Column(db.String(50), unique=True, nullable=False)\n'
'    vin = db.Column(db.String(100), unique=True)\n'
'    status = db.Column(db.String(20), nullable=False, default="active")\n'
'\n'
'    company = db.relationship("Company", back_populates="vehicles")\n'
'    vehicle_type = db.relationship("VehicleType", back_populates="vehicles")\n'
'    current_quarry = db.relationship("Quarry")\n'
'    vehicle_shift_assignments = db.relationship(\n'
'        "VehicleShiftAssignment", back_populates="vehicle", lazy="dynamic"\n'
'    )\n'
'    telematics_readings = db.relationship(\n'
'        "TelematicsReading", back_populates="vehicle", lazy="dynamic"\n'
'    )\n'
'\n'
'\n'
'class Driver(db.Model):\n'
'    __tablename__ = "drivers"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)\n'
'    full_name = db.Column(db.String(255), nullable=False)\n'
'    license_number = db.Column(db.String(100))\n'
'    license_category = db.Column(db.String(10))\n'
'    status = db.Column(db.String(20), nullable=False, default="active")\n'
'    date_of_birth = db.Column(db.Date)\n'
'\n'
'    company = db.relationship("Company", back_populates="drivers")\n'
'    assignments = db.relationship(\n'
'        "DriverAssignment", back_populates="driver", lazy="dynamic"\n'
'    )\n'
'    medical_checks = db.relationship(\n'
'        "MedicalCheck", back_populates="driver", lazy="dynamic"\n'
'    )\n'
'    vehicle_shift_assignments = db.relationship(\n'
'        "VehicleShiftAssignment", back_populates="driver", lazy="dynamic"\n'
'    )\n'
'    telematics_readings = db.relationship(\n'
'        "TelematicsReading", back_populates="driver", lazy="dynamic"\n'
'    )\n'
'\n'
'\n'
'class DriverAssignment(db.Model):\n'
'    __tablename__ = "driver_assignments"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)\n'
'    quarry_id = db.Column(db.Integer, db.ForeignKey("quarries.id"), nullable=False)\n'
'    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)\n'
'    end_date = db.Column(db.Date)\n'
'\n'
'    driver = db.relationship("Driver", back_populates="assignments")\n'
'    quarry = db.relationship("Quarry", back_populates="driver_assignments")\n'
'\n'
'\n'
'class Shift(db.Model):\n'
'    __tablename__ = "shifts"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    quarry_id = db.Column(db.Integer, db.ForeignKey("quarries.id"), nullable=False)\n'
'    shift_date = db.Column(db.Date, nullable=False)\n'
'    start_time = db.Column(db.Time, nullable=False)\n'
'    end_time = db.Column(db.Time, nullable=False)\n'
'\n'
'    quarry = db.relationship("Quarry", back_populates="shifts")\n'
'    medical_checks = db.relationship(\n'
'        "MedicalCheck", back_populates="shift", lazy="dynamic"\n'
'    )\n'
'    vehicle_shift_assignments = db.relationship(\n'
'        "VehicleShiftAssignment", back_populates="shift", lazy="dynamic"\n'
'    )\n'
'    telematics_readings = db.relationship(\n'
'        "TelematicsReading", back_populates="shift", lazy="dynamic"\n'
'    )\n'
'\n'
'\n'
'class MedicalCheck(db.Model):\n'
'    __tablename__ = "medical_checks"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)\n'
'    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id"), nullable=False)\n'
'    check_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)\n'
'    result = db.Column(db.String(20), nullable=False)  # fit / unfit\n'
'    heart_rate = db.Column(db.Integer)\n'
'    blood_pressure = db.Column(db.String(20))\n'
'    notes = db.Column(db.Text)\n'
'\n'
'    driver = db.relationship("Driver", back_populates="medical_checks")\n'
'    shift = db.relationship("Shift", back_populates="medical_checks")\n'
'\n'
'\n'
'class DriverHealthStatus(db.Model):\n'
'    __tablename__ = "driver_health_statuses"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    code = db.Column(db.String(50), nullable=False, unique=True)\n'
'    description = db.Column(db.String(255))\n'
'\n'
'    telematics_readings = db.relationship(\n'
'        "TelematicsReading", back_populates="driver_health_status", lazy="dynamic"\n'
'    )\n'
'\n'
'\n'
'class VehicleShiftAssignment(db.Model):\n'
'    __tablename__ = "vehicle_shift_assignments"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)\n'
'    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)\n'
'    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id"), nullable=False)\n'
'    quarry_id = db.Column(db.Integer, db.ForeignKey("quarries.id"), nullable=False)\n'
'    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)\n'
'    end_time = db.Column(db.DateTime)\n'
'\n'
'    vehicle = db.relationship("Vehicle", back_populates="vehicle_shift_assignments")\n'
'    driver = db.relationship("Driver", back_populates="vehicle_shift_assignments")\n'
'    shift = db.relationship("Shift", back_populates="vehicle_shift_assignments")\n'
'    quarry = db.relationship("Quarry", back_populates="vehicle_shift_assignments")\n'
'\n'
'\n'
'class TelematicsReading(db.Model):\n'
'    __tablename__ = "telematics_readings"\n'
'\n'
'    id = db.Column(db.Integer, primary_key=True)\n'
'    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)\n'
'    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"))\n'
'    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id"))\n'
'    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)\n'
'    latitude = db.Column(db.Float)\n'
'    longitude = db.Column(db.Float)\n'
'    speed_kmh = db.Column(db.Float)\n'
'    driver_health_status_id = db.Column(\n'
'        db.Integer, db.ForeignKey("driver_health_statuses.id")\n'
'    )\n'
'    raw_payload = db.Column(db.Text)\n'
'\n'
'    vehicle = db.relationship("Vehicle", back_populates="telematics_readings")\n'
'    driver = db.relationship("Driver", back_populates="telematics_readings")\n'
'    shift = db.relationship("Shift", back_populates="telematics_readings")\n'
'    driver_health_status = db.relationship(\n'
'        "DriverHealthStatus", back_populates="telematics_readings"\n'
'    )\n',
    "backend/app/routes.py": '\n'
'from flask import Blueprint, jsonify, request\n'
'from .extensions import db\n'
'from .models import Driver, Vehicle, TelematicsReading, Quarry, Company\n'
'\n'
'api_bp = Blueprint("api", __name__)\n'
'\n'
'\n'
'@api_bp.route("/drivers", methods=["GET"])\n'
'def list_drivers():\n'
'    """\n'
'    List all drivers.\n'
'\n'
'    ---\n'
'    tags:\n'
'      - Drivers\n'
'    responses:\n'
'      200:\n'
'        description: A list of drivers.\n'
'        schema:\n'
'          type: array\n'
'          items:\n'
'            type: object\n'
'            properties:\n'
'              id:\n'
'                type: integer\n'
'              full_name:\n'
'                type: string\n'
'              license_number:\n'
'                type: string\n'
'              status:\n'
'                type: string\n'
'    """\n'
'    drivers = Driver.query.all()\n'
'    data = []\n'
'    for d in drivers:\n'
'        data.append(\n'
'            {\n'
'                "id": d.id,\n'
'                "full_name": d.full_name,\n'
'                "license_number": d.license_number,\n'
'                "status": d.status,\n'
'            }\n'
'        )\n'
'    return jsonify(data)\n'
'\n'
'\n'
'@api_bp.route("/drivers", methods=["POST"])\n'
'def create_driver():\n'
'    """\n'
'    Create a new driver.\n'
'\n'
'    ---\n'
'    tags:\n'
'      - Drivers\n'
'    consumes:\n'
'      - application/json\n'
'    parameters:\n'
'      - in: body\n'
'        name: body\n'
'        required: true\n'
'        schema:\n'
'          type: object\n'
'          required:\n'
'            - full_name\n'
'          properties:\n'
'            full_name:\n'
'              type: string\n'
'              example: "John Doe"\n'
'            license_number:\n'
'              type: string\n'
'              example: "AB123456"\n'
'            license_category:\n'
'              type: string\n'
'              example: "C"\n'
'    responses:\n'
'      201:\n'
'        description: Driver created.\n'
'        schema:\n'
'          type: object\n'
'          properties:\n'
'            id:\n'
'              type: integer\n'
'            full_name:\n'
'              type: string\n'
'    """\n'
'    payload = request.get_json() or {}\n'
'    driver = Driver(\n'
'        full_name=payload.get("full_name"),\n'
'        license_number=payload.get("license_number"),\n'
'        license_category=payload.get("license_category"),\n'
'        status="active",\n'
'    )\n'
'    db.session.add(driver)\n'
'    db.session.commit()\n'
'    return (\n'
'        jsonify({"id": driver.id, "full_name": driver.full_name}),\n'
'        201,\n'
'    )\n'
'\n'
'\n'
'@api_bp.route("/drivers/<int:driver_id>", methods=["GET"])\n'
'def get_driver(driver_id: int):\n'
'    """\n'
'    Get a single driver by id.\n'
'\n'
'    ---\n'
'    tags:\n'
'      - Drivers\n'
'    parameters:\n'
'      - in: path\n'
'        name: driver_id\n'
'        required: true\n'
'        type: integer\n'
'        description: Driver identifier.\n'
'    responses:\n'
'      200:\n'
'        description: Driver found.\n'
'        schema:\n'
'          type: object\n'
'          properties:\n'
'            id:\n'
'              type: integer\n'
'            full_name:\n'
'              type: string\n'
'            license_number:\n'
'              type: string\n'
'      404:\n'
'        description: Driver not found.\n'
'    """\n'
'    driver = Driver.query.get(driver_id)\n'
'    if not driver:\n'
'        return jsonify({"message": "Driver not found"}), 404\n'
'    return jsonify(\n'
'        {\n'
'            "id": driver.id,\n'
'            "full_name": driver.full_name,\n'
'            "license_number": driver.license_number,\n'
'            "status": driver.status,\n'
'        }\n'
'    )\n'
'\n'
'\n'
'@api_bp.route("/vehicles", methods=["GET"])\n'
'def list_vehicles():\n'
'    """\n'
'    List all vehicles.\n'
'\n'
'    ---\n'
'    tags:\n'
'      - Vehicles\n'
'    responses:\n'
'      200:\n'
'        description: A list of vehicles.\n'
'        schema:\n'
'          type: array\n'
'          items:\n'
'            type: object\n'
'            properties:\n'
'              id:\n'
'                type: integer\n'
'              plate_number:\n'
'                type: string\n'
'              status:\n'
'                type: string\n'
'    """\n'
'    vehicles = Vehicle.query.all()\n'
'    data = []\n'
'    for v in vehicles:\n'
'        data.append(\n'
'            {\n'
'                "id": v.id,\n'
'                "plate_number": v.plate_number,\n'
'                "status": v.status,\n'
'            }\n'
'        )\n'
'    return jsonify(data)\n'
'\n'
'\n'
'@api_bp.route("/vehicles", methods=["POST"])\n'
'def create_vehicle():\n'
'    """\n'
'    Create a new vehicle.\n'
'\n'
'    ---\n'
'    tags:\n'
'      - Vehicles\n'
'    consumes:\n'
'      - application/json\n'
'    parameters:\n'
'      - in: body\n'
'        name: body\n'
'        required: true\n'
'        schema:\n'
'          type: object\n'
'          required:\n'
'            - company_id\n'
'            - vehicle_type_id\n'
'            - plate_number\n'
'          properties:\n'
'            company_id:\n'
'              type: integer\n'
'            vehicle_type_id:\n'
'              type: integer\n'
'            plate_number:\n'
'              type: string\n'
'            vin:\n'
'              type: string\n'
'    responses:\n'
'      201:\n'
'        description: Vehicle created.\n'
'    """\n'
'    payload = request.get_json() or {}\n'
'    vehicle = Vehicle(\n'
'        company_id=payload.get("company_id"),\n'
'        vehicle_type_id=payload.get("vehicle_type_id"),\n'
'        current_quarry_id=payload.get("current_quarry_id"),\n'
'        plate_number=payload.get("plate_number"),\n'
'        vin=payload.get("vin"),\n'
'        status="active",\n'
'    )\n'
'    db.session.add(vehicle)\n'
'    db.session.commit()\n'
'    return jsonify({"id": vehicle.id, "plate_number": vehicle.plate_number}), 201\n'
'\n'
'\n'
'@api_bp.route("/vehicles/<int:vehicle_id>/telemetry", methods=["GET"])\n'
'def list_vehicle_telemetry(vehicle_id: int):\n'
'    """\n'
'    List telemetry readings for a given vehicle.\n'
'\n'
'    ---\n'
'    tags:\n'
'      - Telemetry\n'
'    parameters:\n'
'      - in: path\n'
'        name: vehicle_id\n'
'        required: true\n'
'        type: integer\n'
'        description: Vehicle identifier.\n'
'    responses:\n'
'      200:\n'
'        description: Telemetry readings.\n'
'        schema:\n'
'          type: array\n'
'          items:\n'
'            type: object\n'
'            properties:\n'
'              id:\n'
'                type: integer\n'
'              timestamp:\n'
'                type: string\n'
'              latitude:\n'
'                type: number\n'
'              longitude:\n'
'                type: number\n'
'              speed_kmh:\n'
'                type: number\n'
'    """\n'
'    readings = (\n'
'        TelematicsReading.query.filter_by(vehicle_id=vehicle_id)\n'
'        .order_by(TelematicsReading.timestamp.desc())\n'
'        .limit(100)\n'
'        .all()\n'
'    )\n'
'    data = []\n'
'    for r in readings:\n'
'        data.append(\n'
'            {\n'
'                "id": r.id,\n'
'                "timestamp": r.timestamp.isoformat(),\n'
'                "latitude": r.latitude,\n'
'                "longitude": r.longitude,\n'
'                "speed_kmh": r.speed_kmh,\n'
'            }\n'
'        )\n'
'    return jsonify(data)\n'
'\n'
'\n'
'@api_bp.route("/telemetry", methods=["POST"])\n'
'def create_telematics_reading():\n'
'    """\n'
'    Create a telemetry reading.\n'
'\n'
'    ---\n'
'    tags:\n'
'      - Telemetry\n'
'    consumes:\n'
'      - application/json\n'
'    parameters:\n'
'      - in: body\n'
'        name: body\n'
'        required: true\n'
'        schema:\n'
'          type: object\n'
'          required:\n'
'            - vehicle_id\n'
'          properties:\n'
'            vehicle_id:\n'
'              type: integer\n'
'            driver_id:\n'
'              type: integer\n'
'            latitude:\n'
'              type: number\n'
'            longitude:\n'
'              type: number\n'
'            speed_kmh:\n'
'              type: number\n'
'            driver_health_status_id:\n'
'              type: integer\n'
'    responses:\n'
'      201:\n'
'        description: Telemetry reading created.\n'
'    """\n'
'    payload = request.get_json() or {}\n'
'    reading = TelematicsReading(\n'
'        vehicle_id=payload.get("vehicle_id"),\n'
'        driver_id=payload.get("driver_id"),\n'
'        latitude=payload.get("latitude"),\n'
'        longitude=payload.get("longitude"),\n'
'        speed_kmh=payload.get("speed_kmh"),\n'
'        driver_health_status_id=payload.get("driver_health_status_id"),\n'
'    )\n'
'    db.session.add(reading)\n'
'    db.session.commit()\n'
'    return jsonify({"id": reading.id}), 201\n',
    "requirements.txt": '\n'
'Flask==3.0.0\n'
'Flask-SQLAlchemy==3.1.1\n'
'flasgger==0.9.7.1\n'
'PyYAML==6.0.2\n'
}


def write_file(path: str, content: str) -> None:
    full_path = Path(path)
    if not full_path.parent.exists():
        full_path.parent.mkdir(parents=True, exist_ok=True)

    if full_path.exists():
        print(f"[skip] {path} already exists")
        return

    with full_path.open("w", encoding="utf-8") as f:
        # Strip leading newlines to keep files clean
        f.write(content.lstrip("\n"))
    print(f"[ok]   created {path}")


def main() -> None:
    print("Bootstrapping mining-fleet backend skeleton...\n")
    for path, content in PROJECT_FILES.items():
        write_file(path, content)

    print("\nAll files generated.")
    print("Next steps:")
    print("  1) python -m venv venv")
    print("  2) venv\\Scripts\\activate  (on Windows) or source venv/bin/activate (Linux/macOS)")
    print("  3) pip install -r requirements.txt")
    print("  4) cd backend")
    print("  5) python run.py")
    print("\nThen open http://127.0.0.1:5000/apidocs/ in your browser.")


if __name__ == "__main__":
    main()

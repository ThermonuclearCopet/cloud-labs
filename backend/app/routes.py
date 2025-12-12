from flask import Blueprint, jsonify, request
from .extensions import db
from .models import (
    Driver,
    Vehicle,
    TelematicsReading,
    Quarry,
    Company,
    VehicleType,
)

api_bp = Blueprint("api", __name__)


def get_or_create_default_company() -> Company:
    """Return existing company or create a default one."""
    company = Company.query.first()
    if not company:
        company = Company(
            name="Default Mining Company",
            status="active",
            country="N/A",
            city="N/A",
        )
        db.session.add(company)
        db.session.commit()
    return company


def get_or_create_default_vehicle_type() -> VehicleType:
    """Return existing vehicle type or create a default one."""
    vehicle_type = VehicleType.query.first()
    if not vehicle_type:
        vehicle_type = VehicleType(
            name="Default Truck",
            description="Generic mining truck",
            max_speed_kmh=60,
            max_payload_tons=40.0,
        )
        db.session.add(vehicle_type)
        db.session.commit()
    return vehicle_type


# ---------------------------------------------------------------------------
# Drivers
# ---------------------------------------------------------------------------


@api_bp.route("/drivers", methods=["GET"])
def list_drivers():
    """
    List all drivers.

    ---
    tags:
      - Drivers
    responses:
      200:
        description: A list of drivers.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              full_name:
                type: string
              license_number:
                type: string
              status:
                type: string
    """
    drivers = Driver.query.all()
    data = []
    for d in drivers:
        data.append(
            {
                "id": d.id,
                "full_name": d.full_name,
                "license_number": d.license_number,
                "license_category": d.license_category,
                "status": d.status,
                "company_id": d.company_id,
            }
        )
    return jsonify(data)


@api_bp.route("/drivers", methods=["POST"])
def create_driver():
    """
    Create a new driver.

    If company_id is not provided, a default company will be created
    (if needed) and used.

    ---
    tags:
      - Drivers
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - full_name
          properties:
            full_name:
              type: string
              example: "John Doe"
            license_number:
              type: string
              example: "AB123456"
            license_category:
              type: string
              example: "C"
            company_id:
              type: integer
              example: 1
    responses:
      201:
        description: Driver created.
        schema:
          type: object
          properties:
            id:
              type: integer
            full_name:
              type: string
      400:
        description: Invalid payload.
    """
    payload = request.get_json() or {}

    full_name = payload.get("full_name")
    if not full_name:
        return jsonify({"message": "full_name is required"}), 400

    company_id = payload.get("company_id")
    if company_id is None:
        company = get_or_create_default_company()
        company_id = company.id

    driver = Driver(
        company_id=company_id,
        full_name=full_name,
        license_number=payload.get("license_number"),
        license_category=payload.get("license_category"),
        status="active",
    )
    db.session.add(driver)
    db.session.commit()
    return jsonify({"id": driver.id, "full_name": driver.full_name}), 201


#@api_bp.route("/drivers/<int:driver_id>", methods=["GET"])
def get_driver(driver_id: int):
    """
    Get a single driver by id.

    ---
    tags:
      - Drivers
    parameters:
      - in: path
        name: driver_id
        required: true
        type: integer
        description: Driver identifier.
    responses:
      200:
        description: Driver found.
        schema:
          type: object
          properties:
            id:
              type: integer
            full_name:
              type: string
            license_number:
              type: string
            status:
              type: string
      404:
        description: Driver not found.
    """
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"message": "Driver not found"}), 404
    return jsonify(
        {
            "id": driver.id,
            "full_name": driver.full_name,
            "license_number": driver.license_number,
            "license_category": driver.license_category,
            "status": driver.status,
            "company_id": driver.company_id,
        }
    )


@api_bp.route("/drivers/<int:driver_id>", methods=["PUT"])
def update_driver(driver_id: int):
    """
    Update an existing driver.

    ---
    tags:
      - Drivers
    consumes:
      - application/json
    parameters:
      - in: path
        name: driver_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            full_name:
              type: string
            license_number:
              type: string
            license_category:
              type: string
            status:
              type: string
              example: "active"
            company_id:
              type: integer
    responses:
      200:
        description: Driver updated.
      404:
        description: Driver not found.
    """
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"message": "Driver not found"}), 404

    payload = request.get_json() or {}

    if "full_name" in payload:
        driver.full_name = payload["full_name"]
    if "license_number" in payload:
        driver.license_number = payload["license_number"]
    if "license_category" in payload:
        driver.license_category = payload["license_category"]
    if "status" in payload:
        driver.status = payload["status"]
    if "company_id" in payload:
        driver.company_id = payload["company_id"]

    db.session.commit()
    return jsonify({"message": "Driver updated"})


# @api_bp.route("/drivers/<int:driver_id>", methods=["DELETE"])
def delete_driver(driver_id: int):
    """
    Delete a driver by id.

    ---
    tags:
      - Drivers
    parameters:
      - in: path
        name: driver_id
        required: true
        type: integer
    responses:
      200:
        description: Driver deleted.
      404:
        description: Driver not found.
    """
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"message": "Driver not found"}), 404

    db.session.delete(driver)
    db.session.commit()
    return jsonify({"message": "Driver deleted"})


# ---------------------------------------------------------------------------
# Vehicles
# ---------------------------------------------------------------------------


@api_bp.route("/vehicles", methods=["GET"])
def list_vehicles():
    """
    List all vehicles.

    ---
    tags:
      - Vehicles
    responses:
      200:
        description: A list of vehicles.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              plate_number:
                type: string
              status:
                type: string
              company_id:
                type: integer
              vehicle_type_id:
                type: integer
    """
    vehicles = Vehicle.query.all()
    data = []
    for v in vehicles:
        data.append(
            {
                "id": v.id,
                "plate_number": v.plate_number,
                "status": v.status,
                "company_id": v.company_id,
                "vehicle_type_id": v.vehicle_type_id,
                "current_quarry_id": v.current_quarry_id,
            }
        )
    return jsonify(data)


@api_bp.route("/vehicles", methods=["POST"])
def create_vehicle():
    """
    Create a new vehicle.

    If company_id or vehicle_type_id are not provided, default entities
    will be created (if needed) and used.

    ---
    tags:
      - Vehicles
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            company_id:
              type: integer
            vehicle_type_id:
              type: integer
            current_quarry_id:
              type: integer
            plate_number:
              type: string
            vin:
              type: string
    responses:
      201:
        description: Vehicle created.
    """
    payload = request.get_json() or {}

    plate_number = payload.get("plate_number")
    if not plate_number:
        return jsonify({"message": "plate_number is required"}), 400

    company_id = payload.get("company_id")
    if company_id is None:
        company_id = get_or_create_default_company().id

    vehicle_type_id = payload.get("vehicle_type_id")
    if vehicle_type_id is None:
        vehicle_type_id = get_or_create_default_vehicle_type().id

    vehicle = Vehicle(
        company_id=company_id,
        vehicle_type_id=vehicle_type_id,
        current_quarry_id=payload.get("current_quarry_id"),
        plate_number=plate_number,
        vin=payload.get("vin"),
        status="active",
    )
    db.session.add(vehicle)
    db.session.commit()
    return (
        jsonify(
            {
                "id": vehicle.id,
                "plate_number": vehicle.plate_number,
                "company_id": vehicle.company_id,
                "vehicle_type_id": vehicle.vehicle_type_id,
            }
        ),
        201,
    )


@api_bp.route("/vehicles/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id: int):
    """
    Get a single vehicle by id.

    ---
    tags:
      - Vehicles
    parameters:
      - in: path
        name: vehicle_id
        required: true
        type: integer
    responses:
      200:
        description: Vehicle found.
      404:
        description: Vehicle not found.
    """
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    return jsonify(
        {
            "id": vehicle.id,
            "plate_number": vehicle.plate_number,
            "status": vehicle.status,
            "company_id": vehicle.company_id,
            "vehicle_type_id": vehicle.vehicle_type_id,
            "current_quarry_id": vehicle.current_quarry_id,
        }
    )


@api_bp.route("/vehicles/<int:vehicle_id>", methods=["PUT"])
def update_vehicle(vehicle_id: int):
    """
    Update an existing vehicle.

    ---
    tags:
      - Vehicles
    consumes:
      - application/json
    parameters:
      - in: path
        name: vehicle_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            plate_number:
              type: string
            status:
              type: string
            company_id:
              type: integer
            vehicle_type_id:
              type: integer
            current_quarry_id:
              type: integer
    responses:
      200:
        description: Vehicle updated.
      404:
        description: Vehicle not found.
    """
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    payload = request.get_json() or {}

    if "plate_number" in payload:
        vehicle.plate_number = payload["plate_number"]
    if "status" in payload:
        vehicle.status = payload["status"]
    if "company_id" in payload:
        vehicle.company_id = payload["company_id"]
    if "vehicle_type_id" in payload:
        vehicle.vehicle_type_id = payload["vehicle_type_id"]
    if "current_quarry_id" in payload:
        vehicle.current_quarry_id = payload["current_quarry_id"]

    db.session.commit()
    return jsonify({"message": "Vehicle updated"})


@api_bp.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id: int):
    """
    Delete a vehicle by id.

    ---
    tags:
      - Vehicles
    parameters:
      - in: path
        name: vehicle_id
        required: true
        type: integer
    responses:
      200:
        description: Vehicle deleted.
      404:
        description: Vehicle not found.
    """
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle deleted"})


# ---------------------------------------------------------------------------
# Telemetry
# ---------------------------------------------------------------------------


@api_bp.route("/vehicles/<int:vehicle_id>/telemetry", methods=["GET"])
def list_vehicle_telemetry(vehicle_id: int):
    """
    List telemetry readings for a given vehicle.

    ---
    tags:
      - Telemetry
    parameters:
      - in: path
        name: vehicle_id
        required: true
        type: integer
        description: Vehicle identifier.
    responses:
      200:
        description: Telemetry readings.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              timestamp:
                type: string
              latitude:
                type: number
              longitude:
                type: number
              speed_kmh:
                type: number
    """
    readings = (
        TelematicsReading.query.filter_by(vehicle_id=vehicle_id)
        .order_by(TelematicsReading.timestamp.desc())
        .limit(100)
        .all()
    )
    data = []
    for r in readings:
        data.append(
            {
                "id": r.id,
                "timestamp": r.timestamp.isoformat(),
                "latitude": r.latitude,
                "longitude": r.longitude,
                "speed_kmh": r.speed_kmh,
            }
        )
    return jsonify(data)


@api_bp.route("/telemetry", methods=["POST"])
def create_telematics_reading():
    """
    Create a telemetry reading.

    ---
    tags:
      - Telemetry
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - vehicle_id
          properties:
            vehicle_id:
              type: integer
            driver_id:
              type: integer
            latitude:
              type: number
            longitude:
              type: number
            speed_kmh:
              type: number
            driver_health_status_id:
              type: integer
            raw_payload:
              type: string
    responses:
      201:
        description: Telemetry reading created.
    """
    payload = request.get_json() or {}

    vehicle_id = payload.get("vehicle_id")
    if vehicle_id is None:
        return jsonify({"message": "vehicle_id is required"}), 400

    reading = TelematicsReading(
        vehicle_id=vehicle_id,
        driver_id=payload.get("driver_id"),
        latitude=payload.get("latitude"),
        longitude=payload.get("longitude"),
        speed_kmh=payload.get("speed_kmh"),
        driver_health_status_id=payload.get("driver_health_status_id"),
        raw_payload=payload.get("raw_payload"),
    )
    db.session.add(reading)
    db.session.commit()
    return jsonify({"id": reading.id}), 201

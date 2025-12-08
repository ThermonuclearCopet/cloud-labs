from datetime import datetime
from .extensions import db


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    registration_number = db.Column(db.String(50))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False, default="active")

    quarries = db.relationship("Quarry", back_populates="company", lazy="dynamic")
    vehicles = db.relationship("Vehicle", back_populates="company", lazy="dynamic")
    drivers = db.relationship("Driver", back_populates="company", lazy="dynamic")


class Quarry(db.Model):
    __tablename__ = "quarries"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    status = db.Column(db.String(20), nullable=False, default="active")

    company = db.relationship("Company", back_populates="quarries")
    shifts = db.relationship("Shift", back_populates="quarry", lazy="dynamic")
    driver_assignments = db.relationship(
        "DriverAssignment", back_populates="quarry", lazy="dynamic"
    )
    vehicle_shift_assignments = db.relationship(
        "VehicleShiftAssignment", back_populates="quarry", lazy="dynamic"
    )


class VehicleType(db.Model):
    __tablename__ = "vehicle_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    max_speed_kmh = db.Column(db.Integer)
    max_payload_tons = db.Column(db.Float)

    vehicles = db.relationship("Vehicle", back_populates="vehicle_type", lazy="dynamic")


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    vehicle_type_id = db.Column(
        db.Integer, db.ForeignKey("vehicle_types.id"), nullable=False
    )
    current_quarry_id = db.Column(db.Integer, db.ForeignKey("quarries.id"))
    plate_number = db.Column(db.String(50), unique=True, nullable=False)
    vin = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), nullable=False, default="active")

    company = db.relationship("Company", back_populates="vehicles")
    vehicle_type = db.relationship("VehicleType", back_populates="vehicles")
    current_quarry = db.relationship("Quarry")
    vehicle_shift_assignments = db.relationship(
        "VehicleShiftAssignment", back_populates="vehicle", lazy="dynamic"
    )
    telematics_readings = db.relationship(
        "TelematicsReading", back_populates="vehicle", lazy="dynamic"
    )


class Driver(db.Model):
    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    license_number = db.Column(db.String(100))
    license_category = db.Column(db.String(10))
    status = db.Column(db.String(20), nullable=False, default="active")
    date_of_birth = db.Column(db.Date)

    company = db.relationship("Company", back_populates="drivers")
    assignments = db.relationship(
        "DriverAssignment", back_populates="driver", lazy="dynamic"
    )
    medical_checks = db.relationship(
        "MedicalCheck", back_populates="driver", lazy="dynamic"
    )
    vehicle_shift_assignments = db.relationship(
        "VehicleShiftAssignment", back_populates="driver", lazy="dynamic"
    )
    telematics_readings = db.relationship(
        "TelematicsReading", back_populates="driver", lazy="dynamic"
    )


class DriverAssignment(db.Model):
    __tablename__ = "driver_assignments"

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    quarry_id = db.Column(db.Integer, db.ForeignKey("quarries.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.Date)

    driver = db.relationship("Driver", back_populates="assignments")
    quarry = db.relationship("Quarry", back_populates="driver_assignments")


class Shift(db.Model):
    __tablename__ = "shifts"

    id = db.Column(db.Integer, primary_key=True)
    quarry_id = db.Column(db.Integer, db.ForeignKey("quarries.id"), nullable=False)
    shift_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    quarry = db.relationship("Quarry", back_populates="shifts")
    medical_checks = db.relationship(
        "MedicalCheck", back_populates="shift", lazy="dynamic"
    )
    vehicle_shift_assignments = db.relationship(
        "VehicleShiftAssignment", back_populates="shift", lazy="dynamic"
    )
    telematics_readings = db.relationship(
        "TelematicsReading", back_populates="shift", lazy="dynamic"
    )


class MedicalCheck(db.Model):
    __tablename__ = "medical_checks"

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id"), nullable=False)
    check_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    result = db.Column(db.String(20), nullable=False)  # fit / unfit
    heart_rate = db.Column(db.Integer)
    blood_pressure = db.Column(db.String(20))
    notes = db.Column(db.Text)

    driver = db.relationship("Driver", back_populates="medical_checks")
    shift = db.relationship("Shift", back_populates="medical_checks")


class DriverHealthStatus(db.Model):
    __tablename__ = "driver_health_statuses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))

    telematics_readings = db.relationship(
        "TelematicsReading", back_populates="driver_health_status", lazy="dynamic"
    )


class VehicleShiftAssignment(db.Model):
    __tablename__ = "vehicle_shift_assignments"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id"), nullable=False)
    quarry_id = db.Column(db.Integer, db.ForeignKey("quarries.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)

    vehicle = db.relationship("Vehicle", back_populates="vehicle_shift_assignments")
    driver = db.relationship("Driver", back_populates="vehicle_shift_assignments")
    shift = db.relationship("Shift", back_populates="vehicle_shift_assignments")
    quarry = db.relationship("Quarry", back_populates="vehicle_shift_assignments")


class TelematicsReading(db.Model):
    __tablename__ = "telematics_readings"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"))
    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id"))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    speed_kmh = db.Column(db.Float)
    driver_health_status_id = db.Column(
        db.Integer, db.ForeignKey("driver_health_statuses.id")
    )
    raw_payload = db.Column(db.Text)

    vehicle = db.relationship("Vehicle", back_populates="telematics_readings")
    driver = db.relationship("Driver", back_populates="telematics_readings")
    shift = db.relationship("Shift", back_populates="telematics_readings")
    driver_health_status = db.relationship(
        "DriverHealthStatus", back_populates="telematics_readings"
    )

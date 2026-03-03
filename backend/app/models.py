from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class Vessel(Base):
    __tablename__ = "vessels"
    id = Column(Integer, primary_key=True)
    imo_number = Column(String(7), unique=True, nullable=False, index=True)
    name = Column(String(120), nullable=False, index=True)
    vessel_type = Column(String(60), nullable=False, index=True)
    deadweight_tons = Column(Integer, nullable=False)
    flag_state = Column(String(80), nullable=False)
    status = Column(String(40), nullable=False, index=True)


class CrewMember(Base):
    __tablename__ = "crew_members"
    id = Column(Integer, primary_key=True)
    employee_code = Column(String(12), unique=True, nullable=False, index=True)
    full_name = Column(String(120), nullable=False)
    rank = Column(String(60), nullable=False, index=True)
    certification_level = Column(String(40), nullable=False)
    join_date = Column(Date, nullable=False)
    active = Column(Boolean, default=True, index=True)


class Voyage(Base):
    __tablename__ = "voyages"
    id = Column(Integer, primary_key=True)
    vessel_id = Column(Integer, ForeignKey("vessels.id"), nullable=False, index=True)
    voyage_code = Column(String(20), unique=True, nullable=False, index=True)
    origin_port = Column(String(120), nullable=False, index=True)
    destination_port = Column(String(120), nullable=False, index=True)
    departure_time = Column(DateTime, nullable=False, index=True)
    arrival_time = Column(DateTime)
    cargo_tonnage = Column(Numeric(10, 2), nullable=False)
    status = Column(String(40), nullable=False, index=True)

    vessel = relationship("Vessel")


class FuelPerformanceLog(Base):
    __tablename__ = "fuel_performance_logs"
    id = Column(Integer, primary_key=True)
    voyage_id = Column(Integer, ForeignKey("voyages.id"), nullable=False, index=True)
    log_time = Column(DateTime, nullable=False, index=True)
    fuel_consumption_mt = Column(Numeric(8, 2), nullable=False)
    avg_speed_knots = Column(Numeric(5, 2), nullable=False)
    engine_load_pct = Column(Numeric(5, 2), nullable=False)
    co2_emissions_mt = Column(Numeric(8, 2), nullable=False)


class MaintenanceComplianceRecord(Base):
    __tablename__ = "maintenance_compliance_records"
    id = Column(Integer, primary_key=True)
    vessel_id = Column(Integer, ForeignKey("vessels.id"), nullable=False, index=True)
    record_type = Column(String(40), nullable=False, index=True)
    title = Column(String(180), nullable=False)
    due_date = Column(Date, nullable=False, index=True)
    completed_date = Column(Date)
    status = Column(String(30), nullable=False, index=True)
    severity = Column(String(20), nullable=False, index=True)


class IncidentInspectionLog(Base):
    __tablename__ = "incident_inspection_logs"
    id = Column(Integer, primary_key=True)
    vessel_id = Column(Integer, ForeignKey("vessels.id"), nullable=False, index=True)
    event_type = Column(String(40), nullable=False, index=True)
    event_date = Column(Date, nullable=False, index=True)
    location = Column(String(120), nullable=False)
    summary = Column(Text, nullable=False)
    risk_level = Column(String(20), nullable=False, index=True)


class CargoOperationHistory(Base):
    __tablename__ = "cargo_operation_history"
    id = Column(Integer, primary_key=True)
    voyage_id = Column(Integer, ForeignKey("voyages.id"), nullable=False, index=True)
    cargo_type = Column(String(80), nullable=False, index=True)
    operation_type = Column(String(30), nullable=False)
    terminal = Column(String(120), nullable=False)
    quantity_tons = Column(Numeric(10, 2), nullable=False)
    operation_time = Column(DateTime, nullable=False, index=True)

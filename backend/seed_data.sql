-- Marine Operations Seed Dataset
-- Guarantees: 50+ vessels, 500+ crew, 5,000+ voyages, 20,000+ fuel logs, 10,000+ maintenance/compliance

CREATE TABLE IF NOT EXISTS vessels (
  id SERIAL PRIMARY KEY,
  imo_number VARCHAR(7) UNIQUE NOT NULL,
  name VARCHAR(120) NOT NULL,
  vessel_type VARCHAR(60) NOT NULL,
  deadweight_tons INT NOT NULL,
  flag_state VARCHAR(80) NOT NULL,
  status VARCHAR(40) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_vessels_type ON vessels(vessel_type);
CREATE INDEX IF NOT EXISTS idx_vessels_status ON vessels(status);

CREATE TABLE IF NOT EXISTS crew_members (
  id SERIAL PRIMARY KEY,
  employee_code VARCHAR(12) UNIQUE NOT NULL,
  full_name VARCHAR(120) NOT NULL,
  rank VARCHAR(60) NOT NULL,
  certification_level VARCHAR(40) NOT NULL,
  join_date DATE NOT NULL,
  active BOOLEAN DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS idx_crew_rank ON crew_members(rank);

CREATE TABLE IF NOT EXISTS voyages (
  id SERIAL PRIMARY KEY,
  vessel_id INT NOT NULL REFERENCES vessels(id),
  voyage_code VARCHAR(20) UNIQUE NOT NULL,
  origin_port VARCHAR(120) NOT NULL,
  destination_port VARCHAR(120) NOT NULL,
  departure_time TIMESTAMP NOT NULL,
  arrival_time TIMESTAMP,
  cargo_tonnage NUMERIC(10,2) NOT NULL,
  status VARCHAR(40) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_voyages_vessel_time ON voyages(vessel_id, departure_time);

CREATE TABLE IF NOT EXISTS fuel_performance_logs (
  id SERIAL PRIMARY KEY,
  voyage_id INT NOT NULL REFERENCES voyages(id),
  log_time TIMESTAMP NOT NULL,
  fuel_consumption_mt NUMERIC(8,2) NOT NULL,
  avg_speed_knots NUMERIC(5,2) NOT NULL,
  engine_load_pct NUMERIC(5,2) NOT NULL,
  co2_emissions_mt NUMERIC(8,2) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_fuel_voyage_time ON fuel_performance_logs(voyage_id, log_time);

CREATE TABLE IF NOT EXISTS maintenance_compliance_records (
  id SERIAL PRIMARY KEY,
  vessel_id INT NOT NULL REFERENCES vessels(id),
  record_type VARCHAR(40) NOT NULL,
  title VARCHAR(180) NOT NULL,
  due_date DATE NOT NULL,
  completed_date DATE,
  status VARCHAR(30) NOT NULL,
  severity VARCHAR(20) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_maint_due_status ON maintenance_compliance_records(due_date, status);

CREATE TABLE IF NOT EXISTS incident_inspection_logs (
  id SERIAL PRIMARY KEY,
  vessel_id INT NOT NULL REFERENCES vessels(id),
  event_type VARCHAR(40) NOT NULL,
  event_date DATE NOT NULL,
  location VARCHAR(120) NOT NULL,
  summary TEXT NOT NULL,
  risk_level VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS cargo_operation_history (
  id SERIAL PRIMARY KEY,
  voyage_id INT NOT NULL REFERENCES voyages(id),
  cargo_type VARCHAR(80) NOT NULL,
  operation_type VARCHAR(30) NOT NULL,
  terminal VARCHAR(120) NOT NULL,
  quantity_tons NUMERIC(10,2) NOT NULL,
  operation_time TIMESTAMP NOT NULL
);

TRUNCATE TABLE cargo_operation_history, incident_inspection_logs, maintenance_compliance_records,
fuel_performance_logs, voyages, crew_members, vessels RESTART IDENTITY CASCADE;

INSERT INTO vessels (imo_number, name, vessel_type, deadweight_tons, flag_state, status)
SELECT LPAD((9300000 + gs)::text, 7, '0'),
       'MV Horizon ' || gs,
       (ARRAY['Bulk Carrier','Container Ship','Tanker','LNG Carrier','RoRo'])[(gs % 5) + 1],
       25000 + (random()*120000)::INT,
       (ARRAY['Panama','Liberia','Marshall Islands','Singapore','Malta'])[(gs % 5) + 1],
       (ARRAY['active','dry_dock','maintenance'])[(gs % 3) + 1]
FROM generate_series(1, 60) gs;

INSERT INTO crew_members (employee_code, full_name, rank, certification_level, join_date, active)
SELECT 'CR' || LPAD(gs::text, 6, '0'),
       'Crew Member ' || gs,
       (ARRAY['Captain','Chief Officer','Second Officer','Chief Engineer','Bosun','Able Seaman'])[(gs % 6) + 1],
       (ARRAY['STCW-A','STCW-B','STCW-C'])[(gs % 3) + 1],
       CURRENT_DATE - ((random()*3650)::INT || ' days')::INTERVAL,
       (gs % 11) != 0
FROM generate_series(1, 650) gs;

INSERT INTO voyages (vessel_id, voyage_code, origin_port, destination_port, departure_time, arrival_time, cargo_tonnage, status)
SELECT ((gs - 1) % 60) + 1,
       'VYG-' || LPAD(gs::text, 6, '0'),
       (ARRAY['Singapore','Rotterdam','Shanghai','Dubai','Hamburg','Busan'])[(gs % 6) + 1],
       (ARRAY['Los Angeles','Antwerp','Mumbai','Doha','Tokyo','Santos'])[(gs % 6) + 1],
       NOW() - ((gs % 1200) || ' hours')::INTERVAL,
       CASE WHEN gs % 7 = 0 THEN NULL ELSE NOW() - (((gs % 1200) - (20 + (gs % 120))) || ' hours')::INTERVAL END,
       5000 + (random()*80000)::NUMERIC(10,2),
       CASE WHEN gs % 7 = 0 THEN 'in_progress' ELSE 'completed' END
FROM generate_series(1, 6000) gs;

INSERT INTO fuel_performance_logs (voyage_id, log_time, fuel_consumption_mt, avg_speed_knots, engine_load_pct, co2_emissions_mt)
SELECT ((gs - 1) % 6000) + 1,
       NOW() - ((gs % 2000) || ' hours')::INTERVAL,
       8 + (random()*28)::NUMERIC(8,2),
       9 + (random()*10)::NUMERIC(5,2),
       55 + (random()*45)::NUMERIC(5,2),
       15 + (random()*25)::NUMERIC(8,2)
FROM generate_series(1, 25000) gs;

INSERT INTO maintenance_compliance_records (vessel_id, record_type, title, due_date, completed_date, status, severity)
SELECT ((gs - 1) % 60) + 1,
       (ARRAY['maintenance','certification','inspection','safety'])[(gs % 4) + 1],
       'Task ' || gs,
       CURRENT_DATE + ((gs % 365) || ' days')::INTERVAL,
       CASE WHEN gs % 4 = 0 THEN CURRENT_DATE - ((gs % 120) || ' days')::INTERVAL ELSE NULL END,
       CASE WHEN gs % 4 = 0 THEN 'completed' WHEN gs % 5 = 0 THEN 'overdue' ELSE 'scheduled' END,
       (ARRAY['low','medium','high','critical'])[(gs % 4) + 1]
FROM generate_series(1, 12000) gs;

INSERT INTO incident_inspection_logs (vessel_id, event_type, event_date, location, summary, risk_level)
SELECT ((gs - 1) % 60) + 1,
       (ARRAY['inspection','near_miss','incident','audit'])[(gs % 4) + 1],
       CURRENT_DATE - ((gs % 1000) || ' days')::INTERVAL,
       (ARRAY['Singapore Strait','North Sea','Suez','Malacca','Atlantic'])[(gs % 5) + 1],
       'Event summary ' || gs,
       (ARRAY['low','medium','high'])[(gs % 3) + 1]
FROM generate_series(1, 3000) gs;

INSERT INTO cargo_operation_history (voyage_id, cargo_type, operation_type, terminal, quantity_tons, operation_time)
SELECT ((gs - 1) % 6000) + 1,
       (ARRAY['Crude Oil','Containers','Coal','LNG','Steel Coils'])[(gs % 5) + 1],
       (ARRAY['load','discharge'])[(gs % 2) + 1],
       'Terminal ' || ((gs % 120) + 1),
       800 + (random()*50000)::NUMERIC(10,2),
       NOW() - ((gs % 3000) || ' hours')::INTERVAL
FROM generate_series(1, 9000) gs;

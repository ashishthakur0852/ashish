from sqlalchemy import text
from sqlalchemy.orm import Session
from .schemas import DynamicReportRequest

DATASET_SQL = {
    "fleet_performance": """
        SELECT v.name AS vessel_name, v.vessel_type, y.voyage_code, y.departure_time, y.arrival_time,
               EXTRACT(EPOCH FROM (COALESCE(y.arrival_time, NOW()) - y.departure_time))/3600 AS voyage_hours,
               y.cargo_tonnage
        FROM voyages y
        JOIN vessels v ON y.vessel_id = v.id
    """,
    "fuel_efficiency": """
        SELECT v.name AS vessel_name, y.voyage_code, f.log_time, f.fuel_consumption_mt, f.avg_speed_knots,
               f.co2_emissions_mt, (f.fuel_consumption_mt / NULLIF(f.avg_speed_knots, 0)) AS fuel_per_knot
        FROM fuel_performance_logs f
        JOIN voyages y ON f.voyage_id = y.id
        JOIN vessels v ON y.vessel_id = v.id
    """,
    "crew_compliance": """
        SELECT c.employee_code, c.full_name, c.rank, c.certification_level, c.join_date, c.active
        FROM crew_members c
    """,
    "maintenance_due": """
        SELECT v.name AS vessel_name, m.record_type, m.title, m.due_date, m.completed_date, m.status, m.severity
        FROM maintenance_compliance_records m
        JOIN vessels v ON m.vessel_id = v.id
    """,
    "voyage_delay_analysis": """
        SELECT v.name AS vessel_name, y.voyage_code, y.origin_port, y.destination_port,
               y.departure_time, y.arrival_time,
               CASE WHEN y.arrival_time IS NULL THEN 'ongoing'
                    WHEN y.arrival_time > y.departure_time + INTERVAL '120 hours' THEN 'delayed'
                    ELSE 'on_time' END AS delay_status
        FROM voyages y
        JOIN vessels v ON y.vessel_id = v.id
    """,
    "incident_safety": """
        SELECT v.name AS vessel_name, i.event_type, i.event_date, i.location, i.risk_level
        FROM incident_inspection_logs i
        JOIN vessels v ON i.vessel_id = v.id
    """,
    "emissions_compliance": """
        SELECT v.name AS vessel_name, y.voyage_code, f.log_time, f.co2_emissions_mt,
               CASE WHEN f.co2_emissions_mt > 30 THEN 'alert' ELSE 'compliant' END AS emissions_status
        FROM fuel_performance_logs f
        JOIN voyages y ON f.voyage_id = y.id
        JOIN vessels v ON y.vessel_id = v.id
    """,
    "cargo_throughput": """
        SELECT v.name AS vessel_name, y.voyage_code, c.cargo_type, c.operation_type,
               c.terminal, c.quantity_tons, c.operation_time
        FROM cargo_operation_history c
        JOIN voyages y ON c.voyage_id = y.id
        JOIN vessels v ON y.vessel_id = v.id
    """,
}


def _build_filters(filters, params):
    clauses = []
    for idx, f in enumerate(filters):
        key = f"f_{idx}"
        if f.operator == "contains":
            clauses.append(f"{f.field} ILIKE :{key}")
            params[key] = f"%{f.value}%"
        elif f.operator == "between":
            clauses.append(f"{f.field} BETWEEN :{key}_a AND :{key}_b")
            params[f"{key}_a"] = f.value[0]
            params[f"{key}_b"] = f.value[1]
        elif f.operator == "in":
            values = []
            for v_idx, val in enumerate(f.value):
                list_key = f"{key}_{v_idx}"
                values.append(f":{list_key}")
                params[list_key] = val
            clauses.append(f"{f.field} IN ({', '.join(values)})")
        else:
            clauses.append(f"{f.field} {f.operator} :{key}")
            params[key] = f.value
    return " AND ".join(clauses)


def run_dynamic_report(db: Session, req: DynamicReportRequest):
    base = DATASET_SQL[req.dataset]
    params = {}

    selected_columns = req.columns[:] if req.columns else ["*"]
    select_part = ", ".join(selected_columns)

    if req.aggregations:
        agg_sql = [f"{a.function.upper()}({a.field}) AS {a.alias}" for a in req.aggregations]
        if req.group_by:
            select_part = ", ".join(req.group_by + agg_sql)
        else:
            select_part = ", ".join(agg_sql)

    sql = f"SELECT {select_part} FROM ({base}) t"

    if req.filters:
        sql += " WHERE " + _build_filters(req.filters, params)

    if req.group_by:
        sql += " GROUP BY " + ", ".join(req.group_by)

    if req.sort_by:
        sql += f" ORDER BY {req.sort_by} {req.sort_direction.upper()}"

    offset = (req.page - 1) * req.page_size
    sql += " LIMIT :limit OFFSET :offset"
    params["limit"] = req.page_size
    params["offset"] = offset

    count_sql = f"SELECT COUNT(*) FROM ({DATASET_SQL[req.dataset]}) t"
    total_rows = db.execute(text(count_sql)).scalar() or 0

    rows = db.execute(text(sql), params).mappings().all()
    return {
        "columns": list(rows[0].keys()) if rows else req.columns,
        "rows": [dict(r) for r in rows],
        "total_rows": total_rows,
        "page": req.page,
        "page_size": req.page_size,
    }

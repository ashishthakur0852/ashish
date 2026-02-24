# MarineOps Insight - Dynamic Marine Reporting Platform

Enterprise-grade marine operations web application focused on **dynamic report generation** across high-volume operational datasets.

## Highlights
- Normalized PostgreSQL schema with seed generation for large maritime datasets.
- FastAPI backend with configurable dynamic reporting API.
- React frontend featuring report builder, live preview, KPI cards, and role-aware UI.
- Prebuilt report datasets: fleet performance, fuel efficiency, compliance, maintenance, delays, incidents, emissions, cargo throughput.
- Export-ready report outputs (JSON API currently; CSV/Excel/PDF extensible through background jobs).

## Architecture
### Backend
- `FastAPI` API layer.
- `SQLAlchemy` data model.
- Dynamic SQL report engine with columns, filters, grouping, aggregation, sorting, and pagination.
- Template save/list endpoints for reusable reporting definitions.

### Frontend
- `React + Vite + TypeScript`.
- Modular components:
  - Dashboard with KPI cards and chart widgets.
  - Dynamic Report Builder with field selection and live preview.
- Zustand state store for role/theme/report preferences.
- Maritime design system with light/dark mode and responsive layout.

## Data Scale (seeded)
- Vessels: **60**
- Crew members: **650**
- Voyages: **6,000**
- Fuel/performance logs: **25,000**
- Maintenance/compliance records: **12,000**
- Incident/inspection logs: **3,000**
- Cargo operations: **9,000**

## Run locally
```bash
docker compose up --build
```
- API: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## Dynamic Report API Example
`POST /api/reports/run`
```json
{
  "dataset": "fuel_efficiency",
  "columns": ["vessel_name", "voyage_code", "fuel_consumption_mt", "co2_emissions_mt"],
  "filters": [{"field": "co2_emissions_mt", "operator": ">", "value": 25}],
  "group_by": ["vessel_name"],
  "aggregations": [{"field": "fuel_consumption_mt", "function": "avg", "alias": "avg_fuel"}],
  "sort_by": "avg_fuel",
  "sort_direction": "desc",
  "page": 1,
  "page_size": 20
}
```

## Production hardening checklist
- Add OAuth2/OIDC and tenant-aware RBAC.
- Move template storage to DB and schedule engine to Celery/Redis.
- Add PDF/XLSX/CSV exports and signed download URLs.
- Add query guardrails (field allowlists + SQL safety parser).
- Add materialized views for heavy recurring reports.
- Add observability stack (Prometheus/Grafana/OpenTelemetry).

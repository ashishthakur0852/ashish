from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .report_engine import run_dynamic_report
from .schemas import DynamicReportRequest, ReportResponse, SavedTemplate

app = FastAPI(title="Marine Ops Dynamic Reporting API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

TEMPLATES = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/reports/run", response_model=ReportResponse)
def run_report(req: DynamicReportRequest, db: Session = Depends(get_db)):
    return run_dynamic_report(db, req)


@app.get("/api/reports/templates")
def list_templates():
    return TEMPLATES


@app.post("/api/reports/templates")
def save_template(template: SavedTemplate):
    TEMPLATES.append(template.model_dump())
    return {"saved": True, "count": len(TEMPLATES)}

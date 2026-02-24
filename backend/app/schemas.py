from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Any


class FilterClause(BaseModel):
    field: str
    operator: Literal["=", "!=", ">", "<", ">=", "<=", "contains", "in", "between"]
    value: Any


class AggregationClause(BaseModel):
    field: str
    function: Literal["sum", "avg", "min", "max", "count"]
    alias: str


class DynamicReportRequest(BaseModel):
    dataset: Literal[
        "fleet_performance",
        "fuel_efficiency",
        "crew_compliance",
        "maintenance_due",
        "voyage_delay_analysis",
        "incident_safety",
        "emissions_compliance",
        "cargo_throughput",
    ]
    columns: List[str] = Field(default_factory=list)
    filters: List[FilterClause] = Field(default_factory=list)
    group_by: List[str] = Field(default_factory=list)
    aggregations: List[AggregationClause] = Field(default_factory=list)
    sort_by: Optional[str] = None
    sort_direction: Literal["asc", "desc"] = "asc"
    page: int = 1
    page_size: int = 50


class SavedTemplate(BaseModel):
    name: str
    description: Optional[str] = None
    config: DynamicReportRequest
    access_role: Literal["operations", "compliance", "executive", "ship_officer"]


class ReportResponse(BaseModel):
    columns: List[str]
    rows: List[dict]
    total_rows: int
    page: int
    page_size: int

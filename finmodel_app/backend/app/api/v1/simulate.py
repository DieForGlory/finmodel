from fastapi import APIRouter
from app.schemas.project import ProjectCreate
from app.services.simulator import generate_cash_flow

router = APIRouter()

@router.post("/calculate-cashflow")
def calculate_project_cashflow(project: ProjectCreate):
    project_data = project.model_dump()
    report = generate_cash_flow(project_data)
    return {"status": "success", "data": report}
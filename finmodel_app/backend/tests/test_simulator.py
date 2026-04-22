import pytest
from datetime import date
from app.services.simulator import generate_cash_flow


def test_generate_cash_flow_full_payment():
    project_data = {
        "construction_period_months": 12,
        "sales_period_months": 12,
        "seasonalities": [],
        "payment_methods": [
            {"method_type": "100_percent", "share_percentage": 100, "installment_months": None}
        ],
        "properties": [{
            "property_type": "residential",
            "total_area": 1000,
            "price_per_sqm": 1500,
            "sales_start_date": date(2026, 5, 1)
        }]
    }

    report = generate_cash_flow(project_data)

    assert len(report) == 12
    total_revenue = sum(item['amount'] for item in report)
    assert total_revenue == 1500000
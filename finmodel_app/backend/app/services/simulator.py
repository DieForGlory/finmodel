import pandas as pd
from dateutil.relativedelta import relativedelta


def generate_cash_flow(project_data: dict) -> list[dict]:
    results = []
    sales_period = project_data['construction_period_months']  # В данном контексте приравниваем цикл к сроку проекта
    seasonality_map = {item['month_number']: item['coefficient'] for item in project_data['seasonalities']}
    payment_methods = project_data['payment_methods']

    for prop in project_data['properties']:
        total_revenue = prop['total_area'] * prop['price_per_sqm']
        base_monthly_revenue = total_revenue / project_data['sales_period_months']

        current_date = prop['sales_start_date']
        remaining_revenue = total_revenue

        for month_index in range(project_data['sales_period_months']):
            current_month_num = current_date.month
            season_coef = seasonality_map.get(current_month_num, 1.0)

            adjusted_revenue = base_monthly_revenue * season_coef

            if adjusted_revenue > remaining_revenue or month_index == project_data['sales_period_months'] - 1:
                adjusted_revenue = remaining_revenue

            remaining_revenue -= adjusted_revenue

            for pm in payment_methods:
                allocated_revenue = adjusted_revenue * (pm['share_percentage'] / 100)

                if pm['method_type'] == 'installment' and pm['installment_months']:
                    installment_chunk = allocated_revenue / pm['installment_months']
                    for i in range(pm['installment_months']):
                        cash_flow_date = current_date + relativedelta(months=i)
                        results.append({
                            'property_type': prop['property_type'],
                            'cash_flow_date': cash_flow_date.strftime('%Y-%m'),
                            'amount': installment_chunk
                        })
                else:
                    results.append({
                        'property_type': prop['property_type'],
                        'cash_flow_date': current_date.strftime('%Y-%m'),
                        'amount': allocated_revenue
                    })

            current_date += relativedelta(months=1)

    df = pd.DataFrame(results)
    if df.empty:
        return []

    cash_flow_report = df.groupby(['cash_flow_date', 'property_type'])['amount'].sum().reset_index()
    return cash_flow_report.to_dict(orient='records')
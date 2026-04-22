import pandas as pd
from dateutil.relativedelta import relativedelta

INSTALLMENT_ANNUAL_RATE = 0.165
MORTGAGE_DOWN_PAYMENT_RATE = 0.30
INSTALLMENT_DOWN_PAYMENT_RATE = 0.30


def generate_cash_flow(project_data: dict) -> list[dict]:
    results = []
    seasonality_map = {item['month_number']: item['coefficient'] for item in project_data.get('seasonalities', [])}
    payment_methods = project_data.get('payment_methods', [])
    sales_period = project_data.get('sales_period_months', 24)

    for prop in project_data.get('properties', []):
        if prop['total_area'] <= 0 or prop['price_per_sqm'] <= 0:
            continue

        total_revenue = prop['total_area'] * prop['price_per_sqm']
        current_date = prop['sales_start_date']

        # Нормализация темпов продаж
        yearly_paces = prop.get('yearly_sales_paces', [])
        if sum(yearly_paces) <= 0:
            years_count = (sales_period + 11) // 12
            yearly_paces = [1.0 / years_count] * years_count
        else:
            total_pace = sum(yearly_paces)
            yearly_paces = [p / total_pace for p in yearly_paces]

        remaining_revenue = total_revenue

        for month_index in range(sales_period):
            year_index = month_index // 12
            pace_for_year = yearly_paces[year_index] if year_index < len(yearly_paces) else 0.0

            # Расчет суммы сезонных коэффициентов для текущего года проекта
            start_month_of_year = year_index * 12
            end_month_of_year = min(start_month_of_year + 12, sales_period)

            sum_season_this_year = 0
            temp_date = prop['sales_start_date'] + relativedelta(months=start_month_of_year)
            for _ in range(start_month_of_year, end_month_of_year):
                sum_season_this_year += seasonality_map.get(temp_date.month, 1.0)
                temp_date += relativedelta(months=1)

            current_month_num = current_date.month
            season_coef = seasonality_map.get(current_month_num, 1.0)

            # Взвешенное распределение годового объема на конкретный месяц
            if sum_season_this_year > 0:
                revenue_for_year = total_revenue * pace_for_year
                adjusted_revenue = (revenue_for_year / sum_season_this_year) * season_coef
            else:
                adjusted_revenue = 0

            if adjusted_revenue > remaining_revenue or month_index == sales_period - 1:
                adjusted_revenue = remaining_revenue

            remaining_revenue -= adjusted_revenue

            if adjusted_revenue <= 0:
                current_date += relativedelta(months=1)
                continue

            for pm in payment_methods:
                share = pm.get('share_percentage', 0)
                if share <= 0:
                    continue

                allocated_revenue = adjusted_revenue * (share / 100)

                if pm['method_type'] == '100_percent':
                    results.append({
                        'cash_flow_date': current_date.strftime('%Y-%m'),
                        'type': f"{prop['property_type']} (100%)",
                        'amount': allocated_revenue
                    })

                elif pm['method_type'] == 'mortgage':
                    dp = allocated_revenue * MORTGAGE_DOWN_PAYMENT_RATE
                    bank = allocated_revenue - dp
                    results.append({
                        'cash_flow_date': current_date.strftime('%Y-%m'),
                        'type': f"{prop['property_type']} (Ипотека ПВ)",
                        'amount': dp
                    })
                    results.append({
                        'cash_flow_date': (current_date + relativedelta(months=1)).strftime('%Y-%m'),
                        'type': f"{prop['property_type']} (Ипотека Банк)",
                        'amount': bank
                    })

                elif pm['method_type'] == 'installment':
                    if pm.get('installment_type') == 'until_end':
                        n_months = sales_period - month_index
                        n_months = max(1, n_months)
                    else:
                        n_months = pm.get('installment_months', 18)

                    interest = 1 + (INSTALLMENT_ANNUAL_RATE * (n_months / 12))
                    total_v = allocated_revenue * interest
                    dp = total_v * INSTALLMENT_DOWN_PAYMENT_RATE
                    monthly = (total_v - dp) / n_months

                    results.append({
                        'cash_flow_date': current_date.strftime('%Y-%m'),
                        'type': f"{prop['property_type']} (Рассрочка ПВ)",
                        'amount': dp
                    })
                    for i in range(1, n_months + 1):
                        results.append({
                            'cash_flow_date': (current_date + relativedelta(months=i)).strftime('%Y-%m'),
                            'type': f"{prop['property_type']} (Рассрочка платеж)",
                            'amount': monthly
                        })

            current_date += relativedelta(months=1)

    if not results: return []
    df = pd.DataFrame(results)
    return df.groupby(['cash_flow_date', 'type'])['amount'].sum().reset_index().to_dict(orient='records')
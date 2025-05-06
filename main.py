from datetime import datetime
from collections import defaultdict
import calendar
import json

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def get_month_date_range(month_str):
    year, month = map(int, month_str.split("-"))
    start = datetime(year, month, 1).date()
    end_day = calendar.monthrange(year, month)[1]
    end = datetime(year, month, end_day).date()
    return start, end

def calculate_active_days(item_start, item_end, month_start, month_end):
    active_start = max(item_start, month_start)
    active_end = min(item_end, month_end)
    if active_start > active_end:
        return 0, None, None
    delta = (active_end - active_start).days + 1
    return delta, active_start, active_end

def to_float(val):
    try:
        return float(val)
    except:
        return 0.0

def to_int(val):
    try:
        return int(val)
    except:
        return 0

def generate_monthly_bill(item_list: list, target_month: str) -> dict:
    month_start, month_end = get_month_date_range(target_month)
    days_in_month = (month_end - month_start).days + 1
    grouped_items = defaultdict(lambda: {"qty": 0, "amount": 0.0})

    for item in item_list:
        start_date = parse_date(item["start_date"])
        stop_date = parse_date(item["stop_date"])
        active_days, active_start, active_end = calculate_active_days(start_date, stop_date, month_start, month_end)
        if active_days == 0:
            continue
        qty = to_int(item.get("qty", 0))
        rate = to_float(item.get("rate", 0))
        prorated_amount = (active_days / days_in_month) * rate * qty
        billing_period_str = f"{active_start} to {active_end}"
        group_key = (item["item_code"], rate, billing_period_str)
        grouped_items[group_key]["qty"] += qty
        grouped_items[group_key]["amount"] += round(prorated_amount, 2)

    line_items = []
    total_revenue = 0.0

    for (item_code, rate, billing_period), values in grouped_items.items():
        amount = round(values["amount"], 2)
        total_revenue += amount
        line_items.append({
            "item_code": item_code,
            "rate": rate,
            "qty": values["qty"],
            "amount": amount,
            "billing_period": billing_period
        })

    return {
        "line_items": line_items,
        "total_revenue": round(total_revenue, 2)
    }

item_list = [
    {
        "idx": 1,
        "item_code": "Executive Desk (4*2)",
        "sales_description": "Dedicated Executive Desk",
        "qty": 10,
        "rate": "1000",
        "amount": "10000",
        "start_date": "2023-11-01",
        "stop_date": "2024-10-17",
    },
    {
        "idx": 2,
        "item_code": "Executive Desk (4*2)",
        "qty": "10",
        "rate": "1080",
        "amount": "10800",
        "start_date": "2024-10-18",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 3,
        "item_code": "Executive Desk (4*2)",
        "qty": 15,
        "rate": "1080",
        "amount": "16200",
        "start_date": "2024-11-01",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 4,
        "item_code": "Executive Desk (4*2)",
        "qty": 5,
        "rate": "1000",
        "amount": "5000",
        "start_date": "2024-11-01",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 5,
        "item_code": "Manager Cabin",
        "qty": 5,
        "rate": 5000,
        "amount": 25000,
        "start_date": "2024-11-01",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 6,
        "item_code": "Manager Cabin",
        "qty": 7,
        "rate": "5000",
        "amount": 35000,
        "start_date": "2024-12-15",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 7,
        "item_code": "Manager Cabin",
        "qty": 10,
        "rate": 4600,
        "amount": 46000,
        "start_date": "2023-11-01",
        "stop_date": "2024-10-17",
    },
    {
        "idx": 8,
        "item_code": "Parking (2S)",
        "qty": 10,
        "rate": 1000,
        "amount": 10000,
        "start_date": "2024-11-01",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 9,
        "item_code": "Parking (2S)",
        "qty": 10,
        "rate": 0,
        "amount": 0,
        "start_date": "2024-11-01",
        "stop_date": "2025-10-31",
    },
    {
        "idx": 10,
        "item_code": "Executive Desk (4*2)",
        "qty": "8",
        "rate": "1100",
        "amount": "8800",
        "start_date": "2024-11-15",
        "stop_date": "2025-01-31",
    },
    {
        "idx": 11,
        "item_code": "Manager Cabin",
        "qty": "3",
        "rate": "5200",
        "amount": "15600",
        "start_date": "2024-10-10",
        "stop_date": "2024-11-10",
    },
    {
        "idx": 12,
        "item_code": "Conference Table",
        "qty": 1,
        "rate": "20000",
        "amount": "20000",
        "start_date": "2024-11-05",
        "stop_date": "2024-11-20",
    },
    {
        "idx": 13,
        "item_code": "Parking (2S)",
        "qty": 5,
        "rate": "1000",
        "amount": "5000",
        "start_date": "2024-11-15",
        "stop_date": "2025-02-28",
    },
    {
        "idx": 14,
        "item_code": "Reception Desk",
        "qty": 2,
        "rate": "7000",
        "amount": "14000",
        "start_date": "2024-11-01",
        "stop_date": "2025-03-31",
    },
    {
        "idx": 15,
        "item_code": "Reception Desk",
        "qty": 1,
        "rate": "7000",
        "amount": "7000",
        "start_date": "2024-11-10",
        "stop_date": "2024-11-25",
    },
    {
        "idx": 16,
        "item_code": "Breakout Area",
        "qty": 3,
        "rate": "3000",
        "amount": "9000",
        "start_date": "2024-01-01",
        "stop_date": "2024-01-31",
    }
]

result = generate_monthly_bill(item_list, "2024-11")

print(json.dumps(result, indent=2))


from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent
ORDERS_CSV = DATA_DIR / "orders.csv"
ORDERS_XLSX = DATA_DIR / "orders.xlsx"


def _flatten_items(items: List[Dict[str, Any]]) -> str:
    parts = []
    for item in items:
        parts.append(f"{item['name']} x{item['qty']}")
    return " | ".join(parts)


def append_order(order: Dict[str, Any]) -> None:
    row = {
        "order_id": order["order_id"],
        "created_at": order["created_at"],
        "client_name": order["client_name"],
        "whatsapp": order["whatsapp"],
        "email": order.get("email", ""),
        "delivery_type": order["delivery_type"],
        "delivery_date": order["delivery_date"],
        "delivery_time": order["delivery_time"],
        "address": order.get("address", ""),
        "notes": order.get("notes", ""),
        "subtotal": order["subtotal"],
        "delivery_fee": order["delivery_fee"],
        "total": order["total"],
        "items": _flatten_items(order["items"]),
    }

    df = pd.DataFrame([row])

    if ORDERS_CSV.exists():
        df.to_csv(ORDERS_CSV, mode="a", header=False, index=False)
    else:
        df.to_csv(ORDERS_CSV, index=False)

    if ORDERS_XLSX.exists():
        with pd.ExcelWriter(ORDERS_XLSX, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            sheet = writer.book["Orders"] if "Orders" in writer.book.sheetnames else writer.book.create_sheet("Orders")
            start_row = sheet.max_row
            df.to_excel(writer, sheet_name="Orders", index=False, header=start_row == 1, startrow=start_row)
    else:
        with pd.ExcelWriter(ORDERS_XLSX, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Orders", index=False)

from __future__ import annotations

import json
import datetime as dt
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from data.orders_store import append_order
from email_utils import send_order_email
from git_utils import commit_and_push

APP_ROOT = Path(__file__).resolve().parent
CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "catalog.json"

app = FastAPI(title="Castelie Cookie Shop")
app.mount("/static", StaticFiles(directory=str(APP_ROOT / "static")), name="static")

templates = Jinja2Templates(directory=str(APP_ROOT / "templates"))


def load_catalog() -> List[Dict[str, Any]]:
    if not CATALOG_PATH.exists():
        return []
    text = CATALOG_PATH.read_text(encoding="utf-8-sig")
    return json.loads(text)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    products = load_catalog()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "products_json": json.dumps(products, ensure_ascii=False),
        },
    )


@app.post("/api/order")
async def create_order(payload: Dict[str, Any]):
    items = payload.get("items", [])
    if not items:
        return JSONResponse({"ok": False, "message": "Carrinho vazio."}, status_code=400)

    name = (payload.get("client_name") or "").strip()
    whatsapp = (payload.get("whatsapp") or "").strip()
    if not name or not whatsapp:
        return JSONResponse({"ok": False, "message": "Nome e WhatsApp sao obrigatorios."}, status_code=400)

    delivery_type = payload.get("delivery_type") or "Entrega"
    address = (payload.get("address") or "").strip()
    if delivery_type == "Entrega" and not address:
        return JSONResponse({"ok": False, "message": "Endereco de entrega obrigatorio."}, status_code=400)

    subtotal = float(payload.get("subtotal") or 0)
    delivery_fee = 8.0 if delivery_type == "Entrega" else 0.0
    total = subtotal + delivery_fee

    now = dt.datetime.now()
    order = {
        "order_id": now.strftime("PED-%Y%m%d-%H%M%S"),
        "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "client_name": name,
        "whatsapp": whatsapp,
        "email": (payload.get("email") or "").strip(),
        "delivery_type": delivery_type,
        "delivery_date": (payload.get("delivery_date") or ""),
        "delivery_time": (payload.get("delivery_time") or ""),
        "address": address,
        "notes": (payload.get("notes") or "").strip(),
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "items": items,
    }

    append_order(order)
    email_ok, email_msg = send_order_email(order)
    git_ok, git_msg = commit_and_push(["data/orders.csv", "data/orders.xlsx"], f"Novo pedido {order['order_id']}")

    return {
        "ok": True,
        "order_id": order["order_id"],
        "email_ok": email_ok,
        "email_msg": email_msg,
        "git_ok": git_ok,
        "git_msg": git_msg,
        "total": total,
    }

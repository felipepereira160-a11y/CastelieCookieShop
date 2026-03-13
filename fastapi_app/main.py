from __future__ import annotations

import csv
import json
import datetime as dt
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from data.orders_store import append_order
from email_utils import send_order_email
from git_utils import commit_and_push

APP_ROOT = Path(__file__).resolve().parent


def _resolve_data_dir() -> Path:
    candidates = [
        APP_ROOT.parents[1] / "data",
        APP_ROOT.parents[2] / "data",
        APP_ROOT.parents[1] / "src" / "data",
        APP_ROOT.parents[2] / "src" / "data",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return APP_ROOT.parents[1] / "data"


def _resolve_assets_dir() -> Path | None:
    candidates = [
        APP_ROOT.parents[1] / "assets",
        APP_ROOT.parents[2] / "assets",
        APP_ROOT.parents[1] / "src" / "assets",
        APP_ROOT.parents[2] / "src" / "assets",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


DATA_DIR = _resolve_data_dir()
CATALOG_PATH = DATA_DIR / "catalog.json"
PAYMENTS_PATH = DATA_DIR / "pagamentos.csv"
ASSETS_DIR = _resolve_assets_dir()
STATIC_DIR = APP_ROOT / "static"
STATIC_PRODUCTS_DIR = STATIC_DIR / "products"
STATIC_PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CATALOG = [
    {
        "id": "ck_classic",
        "name": "Cookie Classico",
        "category": "Cookies",
        "price": 7.5,
        "size": "120g",
        "description": "Massa amanteigada com gotas de chocolate ao leite e toque de baunilha.",
        "highlight": "Mais vendido",
        "available": False,
        "stock": 0,
    },
    {
        "id": "ck_double",
        "name": "Cookie Double Choc",
        "category": "Cookies",
        "price": 8.5,
        "size": "130g",
        "description": "Chocolate intenso com pedacos de chocolate meio amargo.",
        "highlight": "Intenso",
        "available": False,
        "stock": 0,
    },
    {
        "id": "ck_nut",
        "name": "Cookie Castanhas",
        "category": "Cookies",
        "price": 9.0,
        "size": "125g",
        "description": "Mix de castanhas, caramelo salgado e base de chocolate.",
        "highlight": "Crocante",
        "available": False,
        "stock": 0,
    },
    {
        "id": "ck_recheado_tradicional",
        "name": "Cookie recheado tradicional com gotas de chocolate",
        "category": "Cookies",
        "price": 8.5,
        "size": "130g",
        "description": "Cookie recheado tradicional com gotas de chocolate.",
        "highlight": "Disponivel",
        "available": True,
        "stock": 5,
    },
    {
        "id": "bp_brigadeiro",
        "name": "Bolo de Pote Brigadeiro",
        "category": "Bolo de Pote",
        "price": 12.0,
        "size": "240ml",
        "description": "Camadas de bolo de chocolate com brigadeiro cremoso.",
        "highlight": "Classico",
        "available": True,
        "stock": 999,
    },
    {
        "id": "bp_ninho",
        "name": "Bolo de Pote Ninho",
        "category": "Bolo de Pote",
        "price": 12.5,
        "size": "240ml",
        "description": "Bolo branco, creme de leite em po e toque de morango.",
        "highlight": "Suave",
        "available": True,
        "stock": 999,
    },
    {
        "id": "bp_red",
        "name": "Bolo de Pote Red",
        "category": "Bolo de Pote",
        "price": 13.0,
        "size": "240ml",
        "description": "Red velvet com creme de cream cheese e ganache.",
        "highlight": "Premium",
        "available": True,
        "stock": 999,
    },
    {
        "id": "kit_party",
        "name": "Kit Festa Mini",
        "category": "Kits",
        "price": 65.0,
        "size": "6 unidades",
        "description": "3 cookies + 3 bolos de pote. Ideal para compartilhar.",
        "highlight": "Combo",
        "available": True,
        "stock": 999,
    },
    {
        "id": "kit_family",
        "name": "Kit Familia",
        "category": "Kits",
        "price": 120.0,
        "size": "12 unidades",
        "description": "6 cookies + 6 bolos de pote com sabores variados.",
        "highlight": "Melhor custo",
        "available": True,
        "stock": 999,
    },
]

PAYMENT_FIELDS = [
    "cliente",
    "produto_id",
    "produto_nome",
    "quantidade",
    "situacao",
    "valor",
    "valor_pago",
    "observacao",
    "sem_recheio",
    "com_recheio",
]

app = FastAPI(title="Castelie Cookie Shop")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("ADMIN_SESSION_SECRET", "castelie-secret"))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
if ASSETS_DIR is not None:
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

templates = Jinja2Templates(directory=str(APP_ROOT / "templates"))


def load_catalog() -> List[Dict[str, Any]]:
    if not CATALOG_PATH.exists():
        print(f"Catalogo nao encontrado: {CATALOG_PATH}")
        return DEFAULT_CATALOG
    try:
        text = CATALOG_PATH.read_text(encoding="utf-8-sig")
        data = json.loads(text)
        if not data:
            print("Catalogo vazio. Usando default.")
            return DEFAULT_CATALOG
        return data
    except Exception as exc:
        print(f"Falha ao ler catalogo: {exc}. Usando default.")
        return DEFAULT_CATALOG


def save_catalog(items: List[Dict[str, Any]]) -> None:
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def load_payments() -> List[Dict[str, Any]]:
    if not PAYMENTS_PATH.exists():
        return []
    with PAYMENTS_PATH.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            for field in PAYMENT_FIELDS:
                row.setdefault(field, "")
            cliente = (row.get("cliente") or "").strip()
            if not cliente or cliente.lower() == "cookie":
                continue
            rows.append(row)
        return rows


def save_payments(rows: List[Dict[str, Any]]) -> None:
    PAYMENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PAYMENTS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PAYMENT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in PAYMENT_FIELDS})


def _admin_creds() -> tuple[str, str]:
    user = os.getenv("ADMIN_USER", "admin")
    pw = os.getenv("ADMIN_PASS", "C34bs###2028")
    return user, pw


def _is_admin_session(request: Request) -> bool:
    admin_user, _ = _admin_creds()
    return request.session.get("admin_user") == admin_user


def _commit_with_notice(paths: List[str], message: str) -> Dict[str, Any]:
    ok, msg = commit_and_push(paths, message)
    return {"ok": ok, "message": msg}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request, msg: str | None = None, git: str | None = None):
    if not _is_admin_session(request):
        return templates.TemplateResponse("admin_login.html", {"request": request, "message": msg or ""})
    catalog = load_catalog()
    payments = load_payments()
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "catalog_json": json.dumps(catalog, ensure_ascii=False, indent=2),
            "payments_preview": payments[:8],
            "message": msg or "",
            "git_message": git or "",
        },
    )


@app.get("/admin/git-status")
def admin_git_status():
    required = ["GIT_USERNAME", "GIT_REPO", "GIT_TOKEN", "GIT_BRANCH"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        return {"ok": False, "message": f"Faltam variaveis: {', '.join(missing)}"}
    return {"ok": True, "message": "Git configurado."}


@app.post("/admin/login")
def admin_login(request: Request, username: str = Form(""), password: str = Form("")):
    admin_user, admin_pass = _admin_creds()
    if username != admin_user or password != admin_pass:
        return templates.TemplateResponse(
            "admin_login.html",
            {"request": request, "message": "Usuario ou senha incorretos."},
        )
    request.session["admin_user"] = username
    return RedirectResponse("/admin", status_code=303)


@app.get("/admin/logout")
def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin", status_code=303)


@app.get("/admin/pagamentos", response_class=HTMLResponse)
def admin_payments(request: Request, msg: str | None = None, git: str | None = None):
    if not _is_admin_session(request):
        return templates.TemplateResponse("admin_login.html", {"request": request, "message": msg or ""})
    rows = load_payments()
    catalog = load_catalog()
    return templates.TemplateResponse(
        "payments.html",
        {
            "request": request,
            "payments_json": json.dumps(rows, ensure_ascii=False, indent=2),
            "catalog_json": json.dumps(catalog, ensure_ascii=False, indent=2),
            "message": msg or "",
            "git_message": git or "",
        },
    )


@app.post("/admin", response_class=HTMLResponse)
def admin_save(request: Request, catalog_json: str = Form("")):
    if not _is_admin_session(request):
        return templates.TemplateResponse("admin_login.html", {"request": request, "message": "Login necessario."})
    try:
        items = json.loads(catalog_json)
        if not isinstance(items, list):
            raise ValueError("JSON invalido")
        save_catalog(items)
        git = _commit_with_notice(["data/catalog.json"], "Atualizar catalogo")
        msg = "Catalogo atualizado."
        return admin(request, msg=msg, git=git["message"])
    except Exception as exc:
        return admin(request, msg=f"Erro ao salvar: {exc}")


@app.post("/admin/pagamentos", response_class=HTMLResponse)
def admin_payments_save(request: Request, payments_json: str = Form("")):
    if not _is_admin_session(request):
        return templates.TemplateResponse("admin_login.html", {"request": request, "message": "Login necessario."})
    try:
        rows = json.loads(payments_json)
        if not isinstance(rows, list):
            raise ValueError("JSON invalido")
        save_payments(rows)
        git = _commit_with_notice(["data/pagamentos.csv"], "Atualizar pagamentos")
        msg = "Pagamentos atualizados."
        return admin_payments(request, msg=msg, git=git["message"])
    except Exception as exc:
        return admin_payments(request, msg=f"Erro ao salvar: {exc}")


@app.post("/admin/upload")
async def admin_upload(request: Request, product_id: str = Form(""), image: UploadFile = File(...)):
    if not _is_admin_session(request):
        return JSONResponse({"ok": False, "message": "Login necessario."}, status_code=401)

    if not product_id:
        return JSONResponse({"ok": False, "message": "Produto invalido."}, status_code=400)

    ext = Path(image.filename or "").suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        return JSONResponse({"ok": False, "message": "Formato invalido."}, status_code=400)

    target = STATIC_PRODUCTS_DIR / f"{product_id}{ext}"

    for old_ext in (".jpg", ".jpeg", ".png", ".webp"):
        old = STATIC_PRODUCTS_DIR / f"{product_id}{old_ext}"
        if old.exists() and old != target:
            old.unlink()

    content = await image.read()
    target.write_bytes(content)

    git = _commit_with_notice([str(target.relative_to(APP_ROOT.parents[1]))], f"Atualizar imagem {product_id}")
    return {"ok": True, "message": git["message"] if git["message"] else "Imagem salva."}


@app.get("/api/catalog")
def get_catalog():
    return load_catalog()


@app.get("/api/assets-check")
def assets_check():
    files = sorted([p.name for p in STATIC_PRODUCTS_DIR.glob("*.*")])
    return {"count": len(files), "files": files}


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

    # inventory check
    catalog = load_catalog()
    catalog_map = {item.get("id"): item for item in catalog}
    for item in items:
        pid = item.get("id")
        qty = int(item.get("qty") or 0)
        record = catalog_map.get(pid)
        if record is None:
            return JSONResponse({"ok": False, "message": f"Produto {pid} nao encontrado."}, status_code=400)
        if not record.get("available", True):
            return JSONResponse({"ok": False, "message": f"{record.get('name', 'Produto')} indisponivel."}, status_code=400)
        stock = int(record.get("stock") or 0)
        if stock < qty:
            return JSONResponse({"ok": False, "message": f"Estoque insuficiente para {record.get('name', 'produto')}"}, status_code=400)

    # decrement stock
    for item in items:
        pid = item.get("id")
        qty = int(item.get("qty") or 0)
        catalog_map[pid]["stock"] = int(catalog_map[pid].get("stock") or 0) - qty

    save_catalog(list(catalog_map.values()))
    _commit_with_notice(["data/catalog.json"], "Atualizar estoque")

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
    git_ok, git_msg = _commit_with_notice(["data/orders.csv", "data/orders.xlsx"], f"Novo pedido {order['order_id']}").values()

    return {
        "ok": True,
        "order_id": order["order_id"],
        "email_ok": email_ok,
        "email_msg": email_msg,
        "git_ok": git_ok,
        "git_msg": git_msg,
        "total": total,
    }

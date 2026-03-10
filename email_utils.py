import os
import smtplib
from email.message import EmailMessage
from typing import Dict, Any, Tuple


def _get_secret(key: str) -> str:
    value = os.getenv(key, "")
    if value:
        return value
    try:
        import streamlit as st

        return st.secrets.get(key, "")
    except Exception:
        return ""


def send_order_email(order: Dict[str, Any]) -> Tuple[bool, str]:
    smtp_host = _get_secret("SMTP_HOST") or "smtp.gmail.com"
    smtp_port = int(_get_secret("SMTP_PORT") or 587)
    smtp_user = _get_secret("SMTP_USER")
    smtp_pass = _get_secret("SMTP_PASS")
    smtp_to = _get_secret("SMTP_TO") or smtp_user

    if not smtp_user or not smtp_pass or not smtp_to:
        return False, "SMTP nao configurado. Defina SMTP_USER, SMTP_PASS e SMTP_TO."

    msg = EmailMessage()
    msg["Subject"] = f"Novo pedido {order['order_id']}"
    msg["From"] = smtp_user
    msg["To"] = smtp_to

    items_text = "\n".join([f"- {item['name']} x{item['qty']}" for item in order["items"]])

    body = (
        f"Pedido: {order['order_id']}\n"
        f"Data: {order['created_at']}\n\n"
        f"Cliente: {order['client_name']}\n"
        f"WhatsApp: {order['whatsapp']}\n"
        f"Email: {order.get('email', '')}\n\n"
        f"Entrega: {order['delivery_type']}\n"
        f"Data entrega: {order['delivery_date']}\n"
        f"Horario: {order['delivery_time']}\n"
        f"Endereco: {order.get('address', '')}\n\n"
        f"Observacoes: {order.get('notes', '')}\n\n"
        f"Itens:\n{items_text}\n\n"
        f"Subtotal: R$ {order['subtotal']:.2f}\n"
        f"Taxa entrega: R$ {order['delivery_fee']:.2f}\n"
        f"Total: R$ {order['total']:.2f}\n"
    )

    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True, "Email enviado."
    except Exception as exc:
        return False, f"Falha ao enviar email: {exc}"

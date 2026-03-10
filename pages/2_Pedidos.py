import datetime as dt

import streamlit as st

from data.orders_store import append_order
from email_utils import send_order_email
from git_utils import commit_and_push
from state import cart_items, cart_total, init_state, remove_from_cart
from ui import inject_base_css, format_brl, render_top_nav, section_header


st.set_page_config(page_title="Pedidos | Cookie's Shop", page_icon="O", layout="wide")

inject_base_css()
render_top_nav()
init_state()

section_header("Pedidos", "Finalize sua compra")

items = cart_items()

if not items:
    st.markdown(
        "<div class='summary'>Seu carrinho esta vazio. Volte em Produtos para adicionar itens.</div>",
        unsafe_allow_html=True,
    )
    st.stop()

st.markdown("<div class='card'><strong>Seu carrinho</strong></div>", unsafe_allow_html=True)

for item in items:
    row = st.columns([2.2, 1, 1, 0.8])
    with row[0]:
        st.write(f"{item['name']}")
    with row[1]:
        st.write(format_brl(item["price"]))
    with row[2]:
        new_qty = st.number_input(
            "Qtde",
            min_value=1,
            max_value=50,
            value=item["qty"],
            step=1,
            key=f"qty_order_{item['id']}",
        )
        item["qty"] = new_qty
    with row[3]:
        if st.button("Remover", key=f"rm_{item['id']}"):
            remove_from_cart(item["id"])
            st.rerun()

st.write("")

section_header("Dados", "Informacoes do cliente")

col_a, col_b = st.columns(2)
with col_a:
    client_name = st.text_input("Nome completo", placeholder="Ex: Maria Silva")
    whatsapp = st.text_input("WhatsApp", placeholder="(11) 99999-0000")
    email = st.text_input("Email", placeholder="cliente@email.com")
with col_b:
    delivery_type = st.selectbox("Entrega ou retirada", ["Entrega", "Retirada"])
    delivery_date = st.date_input("Data", value=dt.date.today() + dt.timedelta(days=1))
    delivery_time = st.time_input("Horario", value=dt.time(15, 0))

address = st.text_area(
    "Endereco de entrega",
    placeholder="Rua, numero, bairro e ponto de referencia",
    disabled=delivery_type != "Entrega",
)

note = st.text_area("Observacoes", placeholder="Ex: sem castanhas, embalagem para presente")

subtotal = cart_total()
delivery_fee = 8.0 if delivery_type == "Entrega" else 0.0
total = subtotal + delivery_fee

st.write("")

section_header("Resumo", "Valores")

st.markdown(
    f"""
    <div class="summary">
        Subtotal: {format_brl(subtotal)}<br>
        Taxa de entrega: {format_brl(delivery_fee)}<br>
        <strong>Total: {format_brl(total)}</strong>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("Finalizar pedido"):
    if not client_name or not whatsapp:
        st.warning("Informe nome e WhatsApp para finalizar.")
    elif delivery_type == "Entrega" and not address:
        st.warning("Informe o endereco de entrega.")
    else:
        now = dt.datetime.now()
        order = {
            "order_id": now.strftime("PED-%Y%m%d-%H%M%S"),
            "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            "client_name": client_name,
            "whatsapp": whatsapp,
            "email": email,
            "delivery_type": delivery_type,
            "delivery_date": delivery_date.strftime("%Y-%m-%d"),
            "delivery_time": delivery_time.strftime("%H:%M"),
            "address": address,
            "notes": note,
            "subtotal": float(subtotal),
            "delivery_fee": float(delivery_fee),
            "total": float(total),
            "items": items,
        }

        append_order(order)
        email_ok, email_msg = send_order_email(order)
        git_ok, git_msg = commit_and_push(
            [
                "data/orders.csv",
                "data/orders.xlsx",
            ],
            f"Novo pedido {order['order_id']}",
        )

        if email_ok:
            st.success("Email enviado com sucesso.")
        else:
            st.warning(email_msg)

        if git_ok:
            st.success("Pedido registrado e enviado para o GitHub.")
            st.caption(git_msg)
            st.balloons()
        else:
            st.warning("Pedido registrado localmente, mas nao foi possivel enviar ao GitHub.")
            st.caption(git_msg)

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Confirmacao do pedido</div>
                <div class="card-meta">Pedido {order['order_id']} • {order['created_at']}</div>
                <p>Total: <strong>{format_brl(order['total'])}</strong></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

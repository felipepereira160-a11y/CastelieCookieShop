from __future__ import annotations

import streamlit as st


def init_state():
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "last_action" not in st.session_state:
        st.session_state.last_action = ""


def add_to_cart(product_id: str, name: str, price: float, qty: int = 1):
    init_state()
    cart = st.session_state.cart
    if product_id not in cart:
        cart[product_id] = {"id": product_id, "name": name, "price": price, "qty": 0}
    cart[product_id]["qty"] += qty
    st.session_state.last_action = f"{name} adicionado ao carrinho"


def remove_from_cart(product_id: str):
    init_state()
    st.session_state.cart.pop(product_id, None)


def cart_items():
    init_state()
    return list(st.session_state.cart.values())


def cart_total() -> float:
    init_state()
    return sum(item["price"] * item["qty"] for item in st.session_state.cart.values())

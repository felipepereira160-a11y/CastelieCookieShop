from pathlib import Path

import streamlit as st

from data.catalog_store import load_catalog
from state import add_to_cart, cart_items, cart_total, init_state
from ui import inject_base_css, format_brl, render_top_nav, section_header, find_product_image


st.set_page_config(page_title="Produtos | Cookie's Shop", page_icon="P", layout="wide")

inject_base_css()
render_top_nav()
init_state()

section_header("Produtos", "Escolha seus favoritos")

catalog = load_catalog()

image_items = []
for item in catalog:
    image_path = find_product_image(item["id"])
    if image_path:
        image_items.append((item["name"], image_path))

if image_items:
    st.markdown("<div class='card'><strong>Galeria</strong></div>", unsafe_allow_html=True)
    cols = st.columns(min(4, len(image_items)))
    for idx, (name, path) in enumerate(image_items):
        with cols[idx % len(cols)]:
            st.image(path, caption=name, use_container_width=True)

categories = ["Todos"] + sorted({item["category"] for item in catalog})

col_filter, col_search, col_price = st.columns([1, 1.4, 1])
with col_filter:
    category = st.selectbox("Categoria", categories)
with col_search:
    query = st.text_input("Buscar", placeholder="Ex: brigadeiro, castanhas, kit")
with col_price:
    max_price = st.slider("Preco maximo", 7.0, 130.0, 130.0, step=1.0)

filtered = []
for item in catalog:
    if category != "Todos" and item["category"] != category:
        continue
    if query and query.lower() not in (item["name"] + " " + item["description"]).lower():
        continue
    if item["price"] > max_price:
        continue
    filtered.append(item)

if not filtered:
    st.info("Nenhum produto encontrado com esses filtros.")

cols = st.columns(3)
for idx, item in enumerate(filtered):
    with cols[idx % 3]:
        image_path = find_product_image(item["id"])
        if image_path:
            st.image(image_path, use_container_width=True)
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">{item['name']}</div>
                <div class="card-meta">{item['category']} • {item['size']}</div>
                <p>{item['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        qty = st.number_input(
            "Quantidade",
            min_value=1,
            max_value=30,
            value=1,
            step=1,
            key=f"qty_{item['id']}",
        )
        st.markdown(
            f"""
            <div class="card" style="padding-top: 12px;">
                <div class="divider"></div>
                <span class="price">{format_brl(item['price'])}</span>
                <span class="badge">{item['highlight']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Adicionar ao carrinho", key=f"add_{item['id']}"):
            add_to_cart(item["id"], item["name"], item["price"], qty)
            st.success(st.session_state.last_action)

st.write("")
section_header("Carrinho", "Resumo rapido")

items = cart_items()
if not items:
    st.markdown("<div class='summary'>Seu carrinho esta vazio.</div>", unsafe_allow_html=True)
else:
    st.markdown(
        f"""
        <div class="summary">
            <strong>Total parcial:</strong> {format_brl(cart_total())}
            <br>
            <span style="opacity: 0.8;">Finalize o pedido na pagina Pedidos.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(
        [{"Produto": i["name"], "Qtde": i["qty"], "Preco": format_brl(i["price"])} for i in items],
        use_container_width=True,
        hide_index=True,
    )

import os
import re
from pathlib import Path

import pandas as pd
import streamlit as st

from data.catalog_store import load_catalog, save_catalog
from ui import inject_base_css, render_top_nav, section_header


st.set_page_config(page_title="Admin | Cookie's Shop", page_icon="A", layout="wide")

inject_base_css()
render_top_nav()

admin_pass = os.getenv("ADMIN_PASS", "admin")

section_header("Admin", "Gerenciar catalogo e imagens")

pass_input = st.text_input("Senha admin", type="password")
if pass_input != admin_pass:
    st.info("Informe a senha para acessar o painel.")
    st.stop()

catalog = load_catalog()

st.markdown("<div class='card'><strong>Catalogo</strong></div>", unsafe_allow_html=True)

if catalog:
    df = pd.DataFrame(catalog)
else:
    df = pd.DataFrame(columns=["id", "name", "category", "price", "size", "description", "highlight"])

edited = st.data_editor(
    df,
    width="stretch",
    num_rows="dynamic",
    column_config={
        "price": st.column_config.NumberColumn("price", min_value=0.0, step=0.5, format="%.2f"),
    },
)

if st.button("Salvar catalogo"):
    items = edited.fillna("").to_dict(orient="records")
    save_catalog(items)
    st.success("Catalogo atualizado.")

st.write("")
section_header("Novo produto", "Adicionar ao catalogo")

with st.form("add_product"):
    name = st.text_input("Nome")
    category = st.text_input("Categoria", value="Cookies")
    price = st.number_input("Preco", min_value=0.0, step=0.5, value=0.0)
    size = st.text_input("Tamanho", value="120g")
    description = st.text_area("Descricao")
    highlight = st.text_input("Destaque", value="Novo")
    submitted = st.form_submit_button("Adicionar")

if submitted:
    slug = re.sub(r"[^a-z0-9_]+", "_", name.lower().strip())
    slug = re.sub(r"_+", "_", slug).strip("_")
    new_id = slug or f"prod_{len(catalog) + 1}"
    catalog.append(
        {
            "id": new_id,
            "name": name,
            "category": category,
            "price": float(price),
            "size": size,
            "description": description,
            "highlight": highlight,
        }
    )
    save_catalog(catalog)
    st.success(f"Produto '{name}' adicionado com id {new_id}.")
    st.rerun()

st.write("")
section_header("Imagens", "Upload de fotos")

product_ids = [item["id"] for item in catalog]
if not product_ids:
    st.info("Adicione produtos antes de enviar imagens.")
    st.stop()

selected_id = st.selectbox("Produto", product_ids)
file = st.file_uploader("Imagem do produto", type=["jpg", "jpeg", "png", "webp"])

if file and st.button("Salvar imagem"):
    assets_dir = Path(__file__).resolve().parents[1] / "assets" / "products"
    assets_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.name).suffix.lower()
    target = assets_dir / f"{selected_id}{ext}"

    for old_ext in (".jpg", ".jpeg", ".png", ".webp"):
        old = assets_dir / f"{selected_id}{old_ext}"
        if old.exists() and old != target:
            old.unlink()

    target.write_bytes(file.getbuffer())
    st.success("Imagem salva.")

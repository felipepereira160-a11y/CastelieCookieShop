from pathlib import Path

import streamlit as st


def inject_base_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

            :root {
                --cocoa: #22150F;
                --choco: #362116;
                --caramel: #9B5B2F;
                --latte: #CDB59D;
                --cream: #F0E6DB;
                --sand: #E2D2C4;
                --paper: #FAF5EE;
            }

            html, body, [class*="css"]  {
                font-family: 'Source Sans 3', sans-serif;
                color: var(--cocoa);
            }

            .stApp {
                background: radial-gradient(1200px 600px at 10% -10%, #EBDCCB 0%, rgba(235,220,203,0.6) 50%, rgba(235,220,203,0) 70%),
                            radial-gradient(900px 500px at 90% 0%, #D9C5B3 0%, rgba(217,197,179,0.4) 45%, rgba(217,197,179,0) 70%),
                            var(--cream);
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Playfair Display', serif;
                color: var(--cocoa);
                letter-spacing: 0.2px;
            }

            p, span, label, li, div {
                color: var(--cocoa);
            }

            [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
                display: none;
            }

            .top-nav {
                background: var(--sand);
                padding: 10px 16px;
                border-radius: 16px;
                border: 1px solid rgba(54,33,22,0.12);
                margin-bottom: 16px;
            }

            .brand {
                font-family: 'Playfair Display', serif;
                font-size: 20px;
                color: var(--cocoa);
                letter-spacing: 0.4px;
            }

            .stPageLink a {
                color: #6F3A1D;
                font-weight: 600;
                text-decoration: none;
            }
            .stPageLink a:hover {
                color: #9B5B2F;
                text-decoration: underline;
            }

            .hero {
                padding: 24px 28px;
                border-radius: 18px;
                background: linear-gradient(120deg, #EAD8C7 0%, #D9C2AB 45%, #CBAA8E 100%);
                border: 1px solid rgba(54,33,22,0.14);
                box-shadow: 0 16px 40px rgba(54,33,22,0.08);
            }

            .chip {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 999px;
                background: var(--choco);
                color: var(--paper);
                font-size: 12px;
                letter-spacing: 0.4px;
                text-transform: uppercase;
            }

            .card {
                padding: 16px;
                border-radius: 16px;
                background: var(--paper);
                border: 1px solid rgba(54,33,22,0.12);
                box-shadow: 0 8px 20px rgba(54,33,22,0.07);
            }

            .product-card {
                min-height: 230px;
            }

            .card-title {
                font-family: 'Playfair Display', serif;
                font-size: 20px;
                margin-bottom: 4px;
            }

            .card-meta {
                font-size: 13px;
                color: rgba(34,21,15,0.7);
                margin-bottom: 8px;
            }

            .price {
                font-size: 20px;
                font-weight: 700;
                color: var(--caramel);
            }

            .badge {
                display: inline-block;
                padding: 4px 10px;
                border-radius: 999px;
                background: #E0C8B2;
                color: #362116;
                font-size: 12px;
                margin-left: 8px;
            }

            .summary {
                padding: 16px;
                border-radius: 14px;
                background: var(--choco);
                color: var(--paper);
                box-shadow: 0 12px 30px rgba(54,33,22,0.22);
            }

            .divider {
                height: 1px;
                background: rgba(54,33,22,0.16);
                margin: 10px 0 14px 0;
            }

            .stButton > button {
                border-radius: 12px;
                padding: 10px 18px;
                border: none;
                background: var(--caramel);
                color: var(--paper);
                font-weight: 600;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                box-shadow: 0 8px 18px rgba(155,91,47,0.28);
            }
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 24px rgba(155,91,47,0.40);
            }

            .stTextInput label, .stTextArea label, .stNumberInput label, .stSelectbox label, .stDateInput label, .stTimeInput label {
                color: var(--cocoa) !important;
                font-weight: 600;
            }

            .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox select {
                border-radius: 10px;
                border: 1px solid rgba(54,33,22,0.25);
                background: #FFF;
                color: var(--cocoa);
            }

            .stImage img {
                height: 180px;
                object-fit: cover;
                border-radius: 14px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_nav():
    st.markdown("<div class='top-nav'>", unsafe_allow_html=True)
    nav = st.columns([2.6, 1, 1, 1, 1])
    with nav[0]:
        st.markdown("<div class='brand'>Castelie Cookie Shop</div>", unsafe_allow_html=True)
    with nav[1]:
        st.page_link("app.py", label="Inicio", icon="🏠")
    with nav[2]:
        st.page_link("pages/1_Produtos.py", label="Produtos", icon="🧁")
    with nav[3]:
        st.page_link("pages/2_Pedidos.py", label="Pedidos", icon="🧾")
    with nav[4]:
        st.page_link("pages/3_Admin.py", label="Admin", icon="⚙")
    st.markdown("</div>", unsafe_allow_html=True)


def section_header(title: str, subtitle: str | None = None):
    st.markdown(f"<div class='chip'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<h2>{subtitle}</h2>", unsafe_allow_html=True)


def format_brl(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def find_product_image(product_id: str) -> str:
    base = f"assets/products/{product_id}"
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        path = Path(f"{base}{ext}")
        if path.exists():
            return str(path)
    return ""

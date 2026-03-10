from pathlib import Path

import streamlit as st


def inject_base_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;700&family=Manrope:wght@300;400;600&display=swap');

            :root {
                --cocoa: #2A1A12;
                --choco: #3B2519;
                --caramel: #9A5A2A;
                --latte: #D6C1A9;
                --cream: #F2ECE4;
                --sand: #E9DED1;
            }

            html, body, [class*="css"]  {
                font-family: 'Manrope', sans-serif;
                color: var(--cocoa);
            }

            .stApp {
                background: radial-gradient(1200px 600px at 10% -10%, #F3E8DA 0%, rgba(243,232,218,0.6) 50%, rgba(243,232,218,0) 70%),
                            radial-gradient(900px 500px at 90% 0%, #E5D2BC 0%, rgba(229,210,188,0.4) 45%, rgba(229,210,188,0) 70%),
                            var(--cream);
            }

            h1, h2, h3 {
                font-family: 'Fraunces', serif;
                color: var(--cocoa);
                letter-spacing: 0.2px;
            }

            /* Esconde a sidebar */
            [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
                display: none;
            }

            .hero {
                padding: 24px 28px;
                border-radius: 18px;
                background: linear-gradient(120deg, #EFE2D3 0%, #E2CBB1 45%, #D2B293 100%);
                border: 1px solid rgba(59,37,25,0.18);
                box-shadow: 0 16px 40px rgba(59,35,23,0.08);
            }

            .brand {
                font-family: 'Fraunces', serif;
                font-size: 20px;
                color: var(--cocoa);
                letter-spacing: 0.4px;
            }

            .chip {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 999px;
                background: var(--cocoa);
                color: var(--cream);
                font-size: 12px;
                letter-spacing: 0.4px;
                text-transform: uppercase;
            }

            .card {
                padding: 18px 18px 16px 18px;
                border-radius: 16px;
                background: #F7EFE6;
                border: 1px solid rgba(59,37,25,0.12);
                box-shadow: 0 10px 26px rgba(59,35,23,0.08);
                height: 100%;
            }

            .card-title {
                font-family: 'Fraunces', serif;
                font-size: 20px;
                margin-bottom: 4px;
            }

            .card-meta {
                font-size: 13px;
                color: rgba(59,35,23,0.7);
                margin-bottom: 10px;
            }

            .price {
                font-size: 22px;
                font-weight: 700;
                color: var(--caramel);
            }

            .badge {
                display: inline-block;
                padding: 4px 10px;
                border-radius: 999px;
                background: #E0CBB6;
                color: #3B2519;
                font-size: 12px;
                margin-left: 8px;
            }

            .summary {
                padding: 16px;
                border-radius: 14px;
                background: #3B2519;
                color: #F6EFE7;
                box-shadow: 0 12px 30px rgba(59,35,23,0.22);
            }

            .divider {
                height: 1px;
                background: rgba(59,35,23,0.12);
                margin: 12px 0 18px 0;
            }

            .stButton > button {
                border-radius: 12px;
                padding: 10px 18px;
                border: none;
                background: var(--caramel);
                color: #F6EFE7;
                font-weight: 600;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                box-shadow: 0 8px 18px rgba(184,107,58,0.35);
            }
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 24px rgba(184,107,58,0.45);
            }

            .top-nav {
                background: var(--sand);
                padding: 10px 16px;
                border-radius: 16px;
                border: 1px solid rgba(59,37,25,0.12);
                margin-bottom: 14px;
            }

            .stPageLink a {
                color: #7A3F21;
                font-weight: 600;
                text-decoration: none;
            }
            .stPageLink a:hover {
                color: #9A5A2A;
                text-decoration: underline;
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

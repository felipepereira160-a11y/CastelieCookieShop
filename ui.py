from pathlib import Path

import streamlit as st


def inject_base_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;700&family=Manrope:wght@300;400;600&display=swap');

            :root {
                --cocoa: #3B2317;
                --choco: #4B2E1E;
                --caramel: #A55A2A;
                --latte: #E2C7A9;
                --cream: #F2E3D2;
                --strawberry: #B65C5C;
            }

            html, body, [class*="css"]  {
                font-family: 'Manrope', sans-serif;
                color: var(--cocoa);
            }

            .stApp {
                background: radial-gradient(1200px 600px at 10% -10%, #F7E5D4 0%, rgba(247,229,212,0.6) 50%, rgba(247,229,212,0) 70%),
                            radial-gradient(900px 500px at 90% 0%, #E9CDB0 0%, rgba(233,205,176,0.4) 45%, rgba(233,205,176,0) 70%),
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
                background: linear-gradient(120deg, #F7E1CC 0%, #E9C3A3 45%, #DDB18F 100%);
                border: 1px solid rgba(90,55,38,0.15);
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
                background: #FFFFFF;
                border: 1px solid rgba(59,35,23,0.08);
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
                background: var(--latte);
                color: var(--choco);
                font-size: 12px;
                margin-left: 8px;
            }

            .summary {
                padding: 16px;
                border-radius: 14px;
                background: var(--choco);
                color: var(--cream);
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
                color: var(--cream);
                font-weight: 600;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                box-shadow: 0 8px 18px rgba(184,107,58,0.35);
            }
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 24px rgba(184,107,58,0.45);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_nav():
    nav = st.columns([2.4, 1, 1, 1, 1])
    with nav[0]:
        st.markdown("<div class='brand'>Castelie Cookie Shop</div>", unsafe_allow_html=True)
    with nav[1]:
        if st.button("🏠 Inicio", key="nav_home"):
            st.switch_page("app.py")
    with nav[2]:
        if st.button("🧁 Produtos", key="nav_produtos"):
            st.switch_page("pages/1_Produtos.py")
    with nav[3]:
        if st.button("🧾 Pedidos", key="nav_pedidos"):
            st.switch_page("pages/2_Pedidos.py")
    with nav[4]:
        if st.button("⚙ Admin", key="nav_admin"):
            st.switch_page("pages/3_Admin.py")


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

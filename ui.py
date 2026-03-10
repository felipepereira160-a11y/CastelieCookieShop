import streamlit as st
from pathlib import Path


def inject_base_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;700&family=Manrope:wght@300;400;600&display=swap');

            html, body, [class*="css"]  {
                font-family: 'Manrope', sans-serif;
            }

            .stApp {
                background: radial-gradient(1200px 600px at 10% -10%, #FFF0E0 0%, rgba(255,240,224,0.4) 50%, rgba(255,240,224,0) 70%),
                            radial-gradient(900px 500px at 90% 0%, #FFE1C2 0%, rgba(255,225,194,0.4) 45%, rgba(255,225,194,0) 70%),
                            #FFF7EE;
            }

            h1, h2, h3 {
                font-family: 'Fraunces', serif;
                color: #2B1B12;
                letter-spacing: 0.2px;
            }

            .hero {
                padding: 24px 28px;
                border-radius: 18px;
                background: linear-gradient(120deg, #FFF1E1 0%, #FFE0C2 45%, #FFD3B1 100%);
                border: 1px solid rgba(214,90,49,0.18);
                box-shadow: 0 16px 40px rgba(43,27,18,0.08);
            }

            .chip {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 999px;
                background: #2B1B12;
                color: #FFF7EE;
                font-size: 12px;
                letter-spacing: 0.4px;
                text-transform: uppercase;
            }

            .card {
                padding: 18px 18px 16px 18px;
                border-radius: 16px;
                background: #FFFFFF;
                border: 1px solid rgba(43,27,18,0.08);
                box-shadow: 0 10px 26px rgba(43,27,18,0.08);
                height: 100%;
            }

            .card-title {
                font-family: 'Fraunces', serif;
                font-size: 20px;
                margin-bottom: 4px;
            }

            .card-meta {
                font-size: 13px;
                color: rgba(43,27,18,0.7);
                margin-bottom: 10px;
            }

            .price {
                font-size: 22px;
                font-weight: 700;
                color: #D65A31;
            }

            .badge {
                display: inline-block;
                padding: 4px 10px;
                border-radius: 999px;
                background: #FFE7D1;
                color: #7A2F16;
                font-size: 12px;
                margin-left: 8px;
            }

            .summary {
                padding: 16px;
                border-radius: 14px;
                background: #2B1B12;
                color: #FFF7EE;
                box-shadow: 0 12px 30px rgba(43,27,18,0.22);
            }

            .divider {
                height: 1px;
                background: rgba(43,27,18,0.12);
                margin: 12px 0 18px 0;
            }

            .stButton > button {
                border-radius: 12px;
                padding: 10px 18px;
                border: none;
                background: #D65A31;
                color: #FFF7EE;
                font-weight: 600;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                box-shadow: 0 8px 18px rgba(214,90,49,0.35);
            }
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 24px rgba(214,90,49,0.45);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


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

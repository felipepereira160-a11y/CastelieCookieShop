import streamlit as st

from ui import inject_base_css, section_header


st.set_page_config(
    page_title="Cookie's Shop",
    page_icon="C",
    layout="wide",
)

inject_base_css()

st.markdown(
    """
    <div class="hero">
        <div class="chip">Cookie's Shop</div>
        <h1>Cookies e bolo de pote feitos para impressionar.</h1>
        <p style="font-size: 17px; max-width: 720px; color: rgba(43,27,18,0.78);">
            Sabores artesanais, textura perfeita e combinacoes pensadas para festas, presentes e aquele momento especial.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

section_header("Destaques", "O que voce encontra aqui")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">Produtos artesanais</div>
            <div class="card-meta">Ingredientes selecionados e preparos diarios.</div>
            <div class="divider"></div>
            <p>Cookies macios por dentro e bolos de pote cremosos com camadas equilibradas.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">Pedidos sob medida</div>
            <div class="card-meta">Monte combos, escolha quantidades e sabores.</div>
            <div class="divider"></div>
            <p>Perfeito para eventos, empresas e aniversarios. Personalizamos kits.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">Entrega programada</div>
            <div class="card-meta">Agendamento por data e horario.</div>
            <div class="divider"></div>
            <p>Receba fresquinho. Se preferir, retire no balcao com horario marcado.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

section_header("Como usar", "Navegue pelas paginas")

st.markdown(
    """
    <div class="card">
        <ol>
            <li>Acesse a pagina Produtos para escolher os sabores.</li>
            <li>Adicione ao carrinho e ajuste quantidades.</li>
            <li>Finalize seu pedido na pagina Pedidos.</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True,
)

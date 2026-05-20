import streamlit as st
import pandas as pd
import json
import plotly.express as px

JSON_FILE = "data/opportunities.json"

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="AI Opportunity Miner",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS RESPONSIVO
# =========================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }

    div[data-testid="stMetric"] {
        background-color: #111827;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
    }

    @media (max-width: 768px) {

        .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }

        h1 {
            font-size: 28px !important;
        }

        h2 {
            font-size: 22px !important;
        }

        h3 {
            font-size: 18px !important;
        }

        p, div {
            font-size: 15px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HEADER
# =========================

st.title("🚀 AI Opportunity Miner")

st.subheader("🏆 Dashboard Inteligente de Oportunidades")

# =========================
# LOAD DATA
# =========================

try:

    with open(
        JSON_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

except Exception:

    data = []

# =========================
# EMPTY
# =========================

if not data:

    st.warning("Nenhuma oportunidade encontrada.")

else:

    df = pd.DataFrame(data)

    # =========================
    # AJUSTES
    # =========================

    df["score"] = pd.to_numeric(
        df["score"],
        errors="coerce"
    ).fillna(0)

    df = df.sort_values(
        by="score",
        ascending=False
    )

    # =========================
    # SIDEBAR
    # =========================

    st.sidebar.title("⚙ Painel")

    score_min = st.sidebar.slider(
        "🔥 Score mínimo",
        min_value=0,
        max_value=10,
        value=5
    )

    search = st.sidebar.text_input(
        "🔎 Buscar palavra-chave"
    )

    categories = ["Todos"] + sorted(
        df["category"].dropna().unique().tolist()
    )

    selected_category = st.sidebar.selectbox(
        "🏷 Categoria",
        categories
    )

    # =========================
    # BOTÃO BUSCAR
    # =========================

    buscar = st.sidebar.button("🚀 Buscar")

    # =========================
    # FILTROS
    # =========================

    filtered_df = df[
        df["score"] >= score_min
    ]

    if selected_category != "Todos":

        filtered_df = filtered_df[
            filtered_df["category"] == selected_category
        ]

    if search:

        filtered_df = filtered_df[
            filtered_df[
                "idea"
            ].str.lower().str.contains(
                search.lower(),
                na=False
            )
        ]

    # =========================
    # EXECUTAR FILTROS
    # =========================

    if buscar or True:

        df = filtered_df

        # =========================
        # MÉTRICAS
        # =========================

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "📊 Total",
            len(df)
        )

        col2.metric(
            "🔥 Maior Score",
            int(df["score"].max())
            if not df.empty else 0
        )

        col3.metric(
            "📈 Média",
            round(df["score"].mean(), 1)
            if not df.empty else 0
        )

        st.markdown("---")

        # =========================
        # TABELA RESPONSIVA
        # =========================

        st.subheader("📋 Oportunidades")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # =========================
        # GRÁFICO BARRAS
        # =========================

        st.subheader("📊 Ranking de Oportunidades")

        fig_bar = px.bar(
            df,
            x="idea",
            y="score",
            color="category",
            hover_data=["saas"],
            title="Ranking por Score"
        )

        fig_bar.update_layout(
            xaxis_title="Ideia",
            yaxis_title="Score",
            height=500,
            autosize=True
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

        st.markdown("---")

        # =========================
        # GRÁFICO PIZZA
        # =========================

        st.subheader("🥧 Distribuição por Categoria")

        category_count = (
            df["category"]
            .value_counts()
            .reset_index()
        )

        category_count.columns = [
            "category",
            "count"
        ]

        fig_pie = px.pie(
            category_count,
            names="category",
            values="count",
            title="Categorias"
        )

        fig_pie.update_layout(
            height=500,
            autosize=True
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

        st.markdown("---")

        # =========================
        # CARDS RESPONSIVOS
        # =========================

        st.subheader("🔥 Melhores Oportunidades")

        for _, row in df.iterrows():

            with st.container():

                st.markdown(
                    f"""
                    <div style='background:#111827;
                                padding:20px;
                                border-radius:15px;
                                margin-bottom:20px;'>

                    <h3>💡 {row['idea']}</h3>

                    <p><b>🏷 Categoria:</b> {row['category']}</p>

                    <p><b>🔥 Score:</b> {row['score']}</p>

                    <p><b>🧠 Motivo:</b><br>
                    {row['reason']}</p>

                    <p><b>🖥 SaaS:</b><br>
                    {row['saas']}</p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )
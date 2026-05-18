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
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("🚀 AI Opportunity Miner")

st.subheader("🏆 Dashboard de Oportunidades")

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
# EMPTY DATA
# =========================

if not data:

    st.warning("Nenhuma oportunidade encontrada.")

else:

    # dataframe
    df = pd.DataFrame(data)

    # ordena score
    df = df.sort_values(
        by="score",
        ascending=False
    )

    # =========================
    # SIDEBAR FILTROS
    # =========================

    st.sidebar.header("🔎 Filtros")

    score_min = st.sidebar.slider(
        "Score mínimo",
        min_value=0,
        max_value=10,
        value=5
    )

    search = st.sidebar.text_input(
        "Buscar palavra-chave"
    )

    categories = ["Todos"] + sorted(
        df["category"].unique().tolist()
    )

    selected_category = st.sidebar.selectbox(
        "Categoria",
        categories
    )

    # =========================
    # FILTRO SCORE
    # =========================

    filtered_df = df[
        df["score"] >= score_min
    ]

    # =========================
    # FILTRO CATEGORIA
    # =========================

    if selected_category != "Todos":

        filtered_df = filtered_df[
            filtered_df["category"] == selected_category
        ]

    # =========================
    # FILTRO BUSCA
    # =========================

    if search:

        filtered_df = filtered_df[
            filtered_df["idea"]
            .str.lower()
            .str.contains(search.lower())
        ]

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
        df["score"].max()
    )

    col3.metric(
        "📈 Média",
        round(df["score"].mean(), 1)
    )

    # =========================
    # TABELA
    # =========================

    st.subheader("📋 Tabela")

    st.dataframe(
        df,
        use_container_width=True
    )

    # =========================
    # BARRAS
    # =========================

    st.subheader("📊 Ranking por Score")

    fig_bar = px.bar(
        df,
        x="idea",
        y="score",
        color="category",
        hover_data=["saas"],
        title="Ranking de Oportunidades"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

    # =========================
    # PIZZA
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

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

    # =========================
    # CARDS
    # =========================

    st.subheader("🔥 Melhores Oportunidades")

    for _, row in df.iterrows():

        with st.container():

            st.markdown("---")

            st.markdown(
                f"## 💡 {row['idea']}"
            )

            st.markdown(
                f"### 🏷 {row['category']}"
            )

            st.markdown(
                f"### 🔥 Score: {row['score']}"
            )

            st.markdown(
                f"**🧠 Motivo:** {row['reason']}"
            )

            st.markdown(
                f"**🖥 SaaS:** {row['saas']}"
            )
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(

    page_title="AI Opportunity Miner",

    page_icon="🚀",

    layout="wide",

    initial_sidebar_state="expanded"

)

# =========================
# BASE DIRECTORY
# =========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# =========================
# DATABASE CONFIG
# =========================

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "database.db"
)

# =========================
# LOAD CSS
# =========================

CSS_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "style.css"
)

try:

    with open(CSS_PATH, "r", encoding="utf-8") as css:

        st.markdown(

            f"<style>{css.read()}</style>",

            unsafe_allow_html=True

        )

except Exception as error:

    st.warning(
        f"CSS não carregado: {error}"
    )

# =========================
# TITLE
# =========================

st.title("🚀 AI Opportunity Miner")

st.subheader(
    "Dashboard Inteligente de Oportunidades"
)

# =========================
# LOAD DATABASE
# =========================

def load_opportunities():

    try:

        conn = sqlite3.connect(
            DATABASE_PATH
        )

        query = """

        SELECT

            id,
            problem,
            category,
            idea,
            score,
            reason,
            saas,
            created_at

        FROM opportunities

        ORDER BY score DESC

        """

        dataframe = pd.read_sql_query(
            query,
            conn
        )

        conn.close()

        return dataframe

    except Exception as error:

        st.error(
            f"Erro ao carregar banco: {error}"
        )

        return pd.DataFrame()

# =========================
# LOAD DATA
# =========================

df = load_opportunities()

# =========================
# EMPTY DATABASE
# =========================

if df.empty:

    st.warning(
        "Nenhuma oportunidade encontrada."
    )

else:

    # =========================
    # DATA TREATMENT
    # =========================

    df["score"] = pd.to_numeric(
        df["score"],
        errors="coerce"
    ).fillna(0)

    # =========================
    # SIDEBAR
    # =========================

    st.sidebar.title("⚙ Filtros")

    score_min = st.sidebar.slider(

        "🔥 Score mínimo",

        min_value=0,

        max_value=10,

        value=5

    )

    search = st.sidebar.text_input(
        "🔎 Buscar"
    )

    categories = ["Todos"] + sorted(
        df["category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.sidebar.selectbox(

        "🏷 Categoria",

        categories

    )

    # =========================
    # SEARCH BUTTON
    # =========================

    buscar = st.sidebar.button(
        "🚀 Buscar"
    )

    # =========================
    # FILTERS
    # =========================

    filtered_df = df[
        df["score"] >= score_min
    ]

    if selected_category != "Todos":

        filtered_df = filtered_df[
            filtered_df["category"]
            == selected_category
        ]

    if search:

        filtered_df = filtered_df[

            filtered_df["idea"]

            .str.lower()

            .str.contains(
                search.lower(),
                na=False
            )

        ]

    # =========================
    # EXECUTE FILTERS
    # =========================

    if buscar or True:

        df = filtered_df

        # =========================
        # METRICS
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
        # TABLE
        # =========================

        st.subheader(
            "📋 Oportunidades"
        )

        st.dataframe(

            df,

            use_container_width=True,

            hide_index=True

        )

        st.markdown("---")

        # =========================
        # BAR CHART
        # =========================

        st.subheader(
            "📊 Ranking de Oportunidades"
        )

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

            height=500

        )

        st.plotly_chart(

            fig_bar,

            use_container_width=True

        )

        st.markdown("---")

        # =========================
        # PIE CHART
        # =========================

        st.subheader(
            "🥧 Distribuição por Categoria"
        )

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
            height=500
        )

        st.plotly_chart(

            fig_pie,

            use_container_width=True

        )

        st.markdown("---")

        # =========================
        # TIMELINE
        # =========================

        st.subheader(
            "📈 Evolução das Oportunidades"
        )

        timeline_df = df.copy()

        timeline_df["created_at"] = pd.to_datetime(
            timeline_df["created_at"]
        )

        timeline_group = (

            timeline_df

            .groupby(
                timeline_df["created_at"].dt.date
            )

            .size()

            .reset_index(name="total")

        )

        fig_line = px.line(

            timeline_group,

            x="created_at",

            y="total",

            markers=True,

            title="Oportunidades por Data"

        )

        fig_line.update_layout(
            height=500
        )

        st.plotly_chart(

            fig_line,

            use_container_width=True

        )

        st.markdown("---")

        # =========================
        # OPPORTUNITY CARDS
        # =========================

        st.subheader(
            "🔥 Melhores Oportunidades"
        )

        for _, row in df.iterrows():

            st.markdown(

                f"""

                ### 💡 {row['idea']}

                **🏷 Categoria:** {row['category']}

                **🔥 Score:** {row['score']}

                **🧠 Motivo:**  
                {row['reason']}

                **🖥 SaaS:**  
                {row['saas']}

                **📅 Criado em:**  
                {row['created_at']}

                ---

                """

            )
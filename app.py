import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
st.set_page_config(
    page_title="Análisis Salarial por Categoría Semántica",
    layout="wide"
)

# ===============================
# FUNCIONES AUXILIARES
# ===============================
def format_crc(value):
    return f"₡{int(value):,}"

# ===============================
# CARGA DE DATOS
# ===============================
@st.cache_data
def load_data():
    df_cluster = pd.read_csv("dataset_salarios_con_cluster.csv")
    df_categoria = pd.read_csv("resumen_salarios_por_categoria.csv")
    return df_cluster, df_categoria

df, df_cat = load_data()

# ===============================
# MÉTRICAS PRINCIPALES
# ===============================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Registros analizados", len(df))

with col2:
    st.metric(
        "Salario promedio general",
        format_crc(df["salario_limpio_colones"].mean())
    )

with col3:
    st.metric(
        "Salario mediano general",
        format_crc(df["salario_limpio_colones"].median())
    )

with col4:
    st.metric("Categorías analizadas", 17)

st.divider()

# ===============================
# DISTRIBUCIÓN SALARIAL
# ===============================
fig_hist = px.histogram(
    df,
    x="salario_limpio_colones",
    color="cluster_salario",
    nbins=20,
    title="Distribución de salarios mensuales por cluster",
    labels={
        "salario_limpio_colones": "Salario mensual (CRC)",
        "cluster_salario": "Cluster salarial"
    }
)

fig_hist.update_layout(
    bargap=0.1,
    xaxis_tickformat=","
)

st.plotly_chart(fig_hist, use_container_width=True)

# ===============================
# SALARIO PROMEDIO POR CATEGORÍA
# ===============================
df_cat_sorted = df_cat.sort_values("salario_promedio", ascending=True)

fig_bar = px.bar(
    df_cat_sorted,
    x="salario_promedio",
    y="categoria_semantica_final",
    orientation="h",
    title="Salario promedio mensual por categoría semántica",
    labels={
        "salario_promedio": "Salario promedio mensual (CRC)",
        "categoria_semantica_final": "Categoría semántica"
    },
    text=df_cat_sorted["salario_promedio"].apply(format_crc)
)

fig_bar.update_layout(
    xaxis_tickformat=",",
    yaxis=dict(title=""),
    uniformtext_minsize=10,
    uniformtext_mode="hide"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ===============================
# BOXPLOT SALARIAL
# ===============================
fig_box = px.box(
    df,
    x="categoria_semantica_final",
    y="salario_limpio_colones",
    color="cluster_salario",
    title="Distribución salarial por categoría semántica",
    labels={
        "salario_limpio_colones": "Salario mensual (CRC)",
        "categoria_semantica_final": "Categoría semántica",
        "cluster_salario": "Cluster salarial"
    }
)

fig_box.update_layout(
    xaxis_tickangle=-40,
    yaxis_tickformat=","
)

st.plotly_chart(fig_box, use_container_width=True)

# ===============================
# TABLA RESUMEN FINAL
# ===============================
st.divider()
st.subheader("Resumen salarial por categoría semántica")

df_table = df_cat[[
    "categoria_semantica_final",
    "cantidad_puestos",
    "salario_promedio",
    "salario_mediana",
    "salario_min",
    "salario_max",
    "cluster_dominante"
]].copy()

for col in [
    "salario_promedio",
    "salario_mediana",
    "salario_min",
    "salario_max"
]:
    df_table[col] = df_table[col].apply(format_crc)

st.dataframe(
    df_table.sort_values("salario_promedio", ascending=False),
    use_container_width=True,
    hide_index=True
)

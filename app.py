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
col1, col2, col4 = st.columns(3)

with col1:
      st.metric("Registros analizados", "720 (deduplicados)")

with col2:
    st.metric(
        "Salario promedio general",
        format_crc(df["salario_limpio_colones"].mean())
    )

with col4:
    st.metric("Cluster Semanticos analizados", 18)

st.divider()

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
# SALARIO PROMEDIO POR CATEGORÍA Y CLUSTER
# ===============================
# ===============================
# SALARIO PROMEDIO POR CATEGORÍA Y CLUSTER (VERSIÓN MEJORADA)
# ===============================
df_cat_cluster = (
    df.groupby(["categoria_semantica_final", "cluster_salario"])
    .agg(
        salario_promedio=("salario_limpio_colones", "mean"),
        cantidad=("salario_limpio_colones", "count")
    )
    .reset_index()
)

# TRUCO 1: Convertimos el cluster a texto para que los colores sean discretos y no una escala
df_cat_cluster["cluster_salario"] = df_cat_cluster["cluster_salario"].astype(str)

fig_cluster_cat = px.bar(
    df_cat_cluster,
    x="salario_promedio",
    y="categoria_semantica_final",
    color="cluster_salario",
    orientation="h",
    # TRUCO 2: barmode="group" pone las barras una al lado de la otra en lugar de encimadas
    barmode="group", 
    title="Comparativa Salarial: Salarios bajos  vs Salarios altos por Categoría",
    labels={
        "salario_promedio": "Salario promedio mensual (CRC)",
        "categoria_semantica_final": "Área de Trabajo",
        "cluster_salario": "Nivel de Cluster"
    },
    # TRUCO 3: Colores específicos para que contrasten bien
    color_discrete_map={"0": "#1f77b4", "1": "#ff7f0e"} 
)

fig_cluster_cat.update_layout(
    xaxis_tickformat=",",
    yaxis={'categoryorder':'total ascending'}, # Ordena por salario para mejor lectura
    legend_title_text="Segmento Salarial",
    height=600 # Ajusta el tamaño para que no se vea apretado
)

st.plotly_chart(fig_cluster_cat, use_container_width=True)

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

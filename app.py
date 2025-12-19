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
    
    # Convertir cluster 0 y 1 a bajo y alto
    df_cluster['cluster_salario'] = df_cluster['cluster_salario'].replace({0: 'bajo', 1: 'alto'})
    df_categoria['cluster_dominante'] = df_categoria['cluster_dominante'].replace({0: 'bajo', 1: 'alto'})
    
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
# SALARIO PROMEDIO POR CATEGORÍA Y CLUSTER
# ===============================
df_cat_cluster = (

    df.groupby(["categoria_semantica_final", "cluster_salario"])

    .agg(

        salario_promedio=("salario_limpio_colones", "mean"),

        cantidad=("salario_limpio_colones", "count")

    )

    .reset_index()

)

# Crear paleta de colores personalizada - blanco y azul como estaba
color_discrete_map = {'bajo': '#FFFFFF', 'alto': '#1f77b4'}

fig_cluster_cat = px.bar(

    df_cat_cluster,

    x="salario_promedio",

    y="categoria_semantica_final",

    color="cluster_salario",

    orientation="h",

    title="Salario promedio por categoría semántica según cluster salarial",

    labels={

        "salario_promedio": "Salario promedio mensual (CRC)",

        "categoria_semantica_final": "Categoría semántica",

        "cluster_salario": "Cluster salarial"

    },

    text=df_cat_cluster["salario_promedio"].round(0),
    
    color_discrete_map=color_discrete_map

)



fig_cluster_cat.update_layout(

    xaxis_tickformat=",",

    yaxis=dict(title=""),

    uniformtext_minsize=10,

    uniformtext_mode="hide"

)



st.plotly_chart(fig_cluster_cat, use_container_width=True)
# ===============================
# TABLA RESUMEN FINAL
# ===============================
st.divider()
st.subheader("Resumen salarial por categoría semántica")

df_table = df_cat[[
    "categoria_semantica_final",
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

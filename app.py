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
df_cat_cluster = (
    df.groupby(["categoria_semantica_final", "cluster_salario"])
    .agg(
        salario_promedio=("salario_limpio_colones", "mean"),
        cantidad=("salario_limpio_colones", "count")
    )
    .reset_index()
)

# Reemplazar 0 y 1 por bajo y alto
df_cat_cluster['cluster_salario'] = df_cat_cluster['cluster_salario'].replace({0: 'bajo', 1: 'alto'})

# Separar los datos por cluster
df_bajo = df_cat_cluster[df_cat_cluster['cluster_salario'] == 'bajo'].copy()
df_alto = df_cat_cluster[df_cat_cluster['cluster_salario'] == 'alto'].copy()

# Ordenar por categoría para consistencia
categorias_ordenadas = df_cat_cluster['categoria_semantica_final'].unique()

# Crear dos gráficos lado a lado
col1, col2 = st.columns(2)

with col1:
    fig_bajo = px.bar(
        df_bajo,
        x="salario_promedio",
        y="categoria_semantica_final",
        orientation="h",
        title="Salario promedio - Cluster BAJO",
        labels={
            "salario_promedio": "Salario promedio (CRC)",
            "categoria_semantica_final": "Categoría semántica"
        },
        text=df_bajo["salario_promedio"].round(0),
        color_discrete_sequence=['lightblue']  # Color claro para bajo
    )
    
    fig_bajo.update_layout(
        xaxis_tickformat=",",
        yaxis=dict(title="", categoryorder='array', categoryarray=categorias_ordenadas),
        uniformtext_minsize=8,
        showlegend=False
    )
    
    fig_bajo.update_traces(texttemplate='%{text:,.0f}', textposition='inside')
    st.plotly_chart(fig_bajo, use_container_width=True)

with col2:
    fig_alto = px.bar(
        df_alto,
        x="salario_promedio",
        y="categoria_semantica_final",
        orientation="h",
        title="Salario promedio - Cluster ALTO",
        labels={
            "salario_promedio": "Salario promedio (CRC)",
            "categoria_semantica_final": "Categoría semántica"
        },
        text=df_alto["salario_promedio"].round(0),
        color_discrete_sequence=['darkblue']  # Color oscuro para alto
    )
    
    fig_alto.update_layout(
        xaxis_tickformat=",",
        yaxis=dict(title="", categoryorder='array', categoryarray=categorias_ordenadas),
        uniformtext_minsize=8,
        showlegend=False
    )
    
    fig_alto.update_traces(texttemplate='%{text:,.0f}', textposition='inside')
    st.plotly_chart(fig_alto, use_container_width=True)
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

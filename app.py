import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# CONFIGURACIÓN
# ===============================
st.set_page_config(
    page_title="Dashboard Salarial",
    layout="wide"
)

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
# MÉTRICAS GENERALES
# ===============================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Registros analizados",
        value=len(df)
    )

with col2:
    st.metric(
        label="Salario promedio (CRC)",
        value=f"₡{int(df['salario_limpio_colones'].mean()):,}"
    )

with col3:
    st.metric(
        label="Categorías semánticas",
        value=df_cat['categoria_semantica_final'].nunique()
    )

st.divider()

# ===============================
# DISTRIBUCIÓN SALARIAL
# ===============================
fig_dist = px.histogram(
    df,
    x="salario_limpio_colones",
    color="cluster_salario",
    nbins=25,
    title="Distribución salarial por cluster",
    labels={"salario_limpio_colones": "Salario mensual (CRC)"}
)

st.plotly_chart(fig_dist, use_container_width=True)

# ===============================
# SALARIO PROMEDIO POR CATEGORÍA
# ===============================
fig_cat = px.bar(
    df_cat.sort_values("salario_promedio", ascending=True),
    x="salario_promedio",
    y="categoria_semantica_final",
    orientation="h",
    title="Salario promedio por categoría semántica (CRC)",
    labels={
        "salario_promedio": "Salario promedio (CRC)",
        "categoria_semantica_final": "Categoría semántica"
    }
)

st.plotly_chart(fig_cat, use_container_width=True)

# ===============================
# BOX PLOT SALARIAL POR CATEGORÍA
# ===============================
fig_box = px.box(
    df,
    x="categoria_semantica_final",
    y="salario_limpio_colones",
    color="cluster_salario",
    title="Distribución salarial por categoría semántica",
    labels={
        "salario_limpio_colones": "Salario mensual (CRC)",
        "categoria_semantica_final": "Categoría semántica"
    }
)

fig_box.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_box, use_container_width=True)

# ===============================
# TABLA RESUMEN
# ===============================
st.divider()
st.subheader("Resumen salarial por categoría")

st.dataframe(
    df_cat[[
        "categoria_semantica_final",
        "cantidad_puestos",
        "salario_promedio",
        "salario_mediana",
        "salario_min",
        "salario_max",
        "cluster_dominante"
    ]],
    use_container_width=True
)

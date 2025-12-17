import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Herramienta Interna", layout="wide")

# --- SELECTOR DE FUENTE DE DATOS ---
st.sidebar.title("Configuración")
modo_datos = st.sidebar.radio("Fuente de datos:", ["Simulación (Prueba)", "MySQL (Real)"])

# --- FUNCIÓN PARA OBTENER DATOS ---
def obtener_datos(modo):
    if modo == "Simulación (Prueba)":
        # Creamos datos parecidos a los que tendrías en tu empresa
        data = {
            'fecha': pd.date_range(start='2024-01-01', periods=100, freq='D'),
            'categoria': np.random.choice(['Electrónica', 'Hogar', 'Oficina', 'Servicios'], 100),
            'monto': np.random.uniform(100, 1500, 100).round(2),
            'vendedor': np.random.choice(['Ana', 'Luis', 'Pedro', 'Marta'], 100)
        }
        return pd.DataFrame(data)
    else:
        # Aquí irá tu conexión real cuando estés listo
        try:
            conn = st.connection('mysql', type='sql')
            return conn.query("SELECT * FROM tus_ventas_reales", ttl=600)
        except Exception as e:
            st.error("No se pudo conectar a MySQL. Revisa tus Secrets.")
            return pd.DataFrame()

# 1. Cargar los datos según el modo seleccionado
df = obtener_datos(modo_datos)

if not df.empty:
    st.title(f"📊 Dashboard de Ventas ({modo_datos})")

    # 2. KPIs rápidos (Métricas tipo Tableau)
    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas Totales", f"${df['monto'].sum():,.2f}")
    col2.metric("Categoría Top", df.groupby('categoria')['monto'].sum().idxmax())
    col3.metric("Ticket Promedio", f"${df['monto'].mean():,.2f}")

    # 3. Gráficos interactivos
    fila2_col1, fila2_col2 = st.columns(2)

    with fila2_col1:
        fig_bar = px.bar(df, x='categoria', y='monto', color='vendedor', title="Ventas por Categoría y Vendedor")
        st.plotly_chart(fig_bar, use_container_width=True)

    with fila2_col2:
        fig_line = px.line(df.groupby('fecha')['monto'].sum().reset_index(), x='fecha', y='monto', title="Tendencia de Ventas")
        st.plotly_chart(fig_line, use_container_width=True)

    # 4. Tabla de datos crudos (con filtro)
    st.write("### Detalle de Transacciones")
    vendedor_filtro = st.multiselect("Filtrar por vendedor:", df['vendedor'].unique(), default=df['vendedor'].unique())
    df_final = df[df['vendedor'].isin(vendedor_filtro)]
    st.dataframe(df_final, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard Corporativo", layout="wide")

# 2. Función para conectar a tu MySQL (usando caché para que sea rápido)
@st.cache_data
def cargar_datos():
    # Aquí usamos la conexión que configuramos antes
    conn = st.connection('mysql', type='sql')
    query = """
        SELECT categoria, SUM(monto) as total_ventas 
        FROM ventas 
        GROUP BY categoria
    """
    return conn.query(query)

# --- INTERFAZ DE LA APP ---
st.title("📊 Mi Reemplazo de Tableau")
st.markdown("Esta herramienta lee directamente de MySQL y muestra los datos en tiempo real.")

try:
    df = cargar_datos()

    # 3. Filtros laterales (Como en Tableau)
    st.sidebar.header("Filtros")
    categorias_seleccionadas = st.sidebar.multiselect(
        "Selecciona Categorías:",
        options=df["categoria"].unique(),
        default=df["categoria"].unique()
    )

    # Filtrar el dataframe basado en la selección
    df_filtrado = df[df["categoria"].isin(categorias_seleccionadas)]

    # 4. Crear el gráfico (El "Visual")
    fig = px.bar(
        df_filtrado, 
        x="categoria", 
        y="total_ventas",
        title="Ventas Totales por Categoría",
        labels={"total_ventas": "Ventas ($)", "categoria": "Categoría"},
        color="total_ventas",
        color_continuous_scale="Viridis"
    )

    # 5. Mostrar el gráfico en la app
    st.plotly_chart(fig, use_container_width=True)

    # 6. Botón para exportar a Excel (Plus que no tiene Tableau Reader fácilmente)
    st.download_button(
        label="📥 Descargar datos en Excel",
        data=df_filtrado.to_csv(index=False),
        file_name="reporte_ventas.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"Hubo un error al conectar con la base de datos: {e}")

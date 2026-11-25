"""MiData - Asistente inteligente para transformar datos en información útil.
Ejecutar:  streamlit run midata_app.py"""
import streamlit as st
from backend.carga import cargar_archivo
from backend import salud, eda, visualizacion, privacidad, asistente

st.set_page_config(page_title="MiData", page_icon="📊", layout="wide")
st.title("📊 MiData")
st.caption("Asistente inteligente para transformar datos en información útil · IES N° 9 «Juana Azurduy»")

with st.sidebar:
    st.header("1. Cargá tu planilla")
    archivo = st.file_uploader("CSV o Excel (hasta 50 MB)", type=["csv", "xlsx", "xls"])
    st.info("🔒 Los datos viven solo en la memoria de esta sesión. A la IA se envía "
            "únicamente un resumen estadístico anonimizado (Ley 25.326).")

if not archivo:
    st.write("Subí un archivo desde la barra lateral para comenzar. "
             "Podés probar con `datos/ventas_ejemplo.csv`.")
    st.stop()

try:
    df = cargar_archivo(archivo.name, archivo.getvalue())
except Exception as e:
    st.error(f"No se pudo leer el archivo: {e}")
    st.stop()

t1, t2, t3, t4 = st.tabs(["🩺 Salud de Datos", "📈 EDA", "🎨 Visualización", "💬 Chat IA"])

with t1:
    r = salud.resumen_estructura(df)
    c = st.columns(4)
    c[0].metric("Filas", r["filas"]); c[1].metric("Columnas", r["columnas"])
    c[2].metric("Duplicados", r["duplicados"]); c[3].metric("Nulos", r["nulos_totales"])
    st.subheader("Detalle por columna"); st.dataframe(salud.tabla_columnas(df), use_container_width=True)
    st.subheader("Valores atípicos (método IQR)"); st.dataframe(salud.outliers_iqr(df), use_container_width=True)
    sens = privacidad.columnas_sensibles(df)
    if sens:
        st.warning(f"Columnas posiblemente sensibles (no se enviarán a la IA): {', '.join(sens)}")

with t2:
    st.subheader("Estadísticas descriptivas"); st.dataframe(eda.estadisticas(df), use_container_width=True)
    cats = eda.columnas_categoricas(df)
    if cats:
        col = st.selectbox("Frecuencias de:", cats); st.dataframe(eda.frecuencias(df, col))
    corr = eda.correlaciones(df)
    if not corr.empty:
        st.subheader("Correlaciones"); st.dataframe(corr)

with t3:
    tipo = st.radio("Tipo de gráfico", ["Barras", "Líneas", "Dispersión", "Histograma"], horizontal=True)
    num = list(df.select_dtypes("number").columns)
    x = st.selectbox("Eje X", list(df.columns))
    y = st.selectbox("Eje Y", num) if tipo != "Histograma" and num else None
    st.plotly_chart(visualizacion.grafico(df, tipo, x, y), use_container_width=True)

with t4:
    st.caption("Preguntá en lenguaje cotidiano. La respuesta se basa solo en tus datos.")
    pregunta = st.text_input("Tu pregunta", placeholder="¿Qué producto tuvo más ventas?")
    if pregunta:
        try:
            with st.spinner("Consultando…"):
                resp, ctx = asistente.responder(df, pregunta)
            st.markdown(resp)
            with st.expander("Ver el resumen anonimizado enviado a la IA (trazabilidad)"):
                st.code(ctx)
        except Exception as e:
            st.error(f"No se pudo consultar la IA ({e}). Verificá la variable ANTHROPIC_API_KEY.")

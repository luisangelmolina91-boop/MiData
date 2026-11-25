# MiData v1.0 (MVP)
Asistente inteligente para transformar datos en información útil. Python 3.12 + Streamlit.

## Instalación
```
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="tu_clave"                # Windows: set ANTHROPIC_API_KEY=tu_clave
streamlit run midata_app.py
```
## Uso (3 pasos)
1. Cargá un CSV/Excel desde la barra lateral.
2. Revisá Salud de Datos, EDA y Visualización.
3. Preguntale a tus datos en la pestaña Chat IA.

## Estructura
- `midata_app.py`: interfaz Streamlit (4 pestañas)
- `backend/`: carga, salud, eda, visualizacion, privacidad, asistente
- `datos/ventas_ejemplo.csv`: dataset de prueba (con nulos, un duplicado y un atípico)

## Privacidad
Sin almacenamiento permanente. A la IA solo se envía un resumen estadístico sin columnas sensibles.
La IA se cambia de proveedor editando únicamente `backend/asistente.py::llamar_llm`.

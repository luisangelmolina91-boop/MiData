"""F1 - Ingestión: lee CSV y Excel con validación de codificación y delimitador."""
import io
import pandas as pd

MAX_MB = 50
CODIFICACIONES = ("utf-8", "utf-8-sig", "latin-1", "cp1252")


def cargar_archivo(nombre: str, contenido: bytes) -> pd.DataFrame:
    if len(contenido) > MAX_MB * 1024 * 1024:
        raise ValueError(f"El archivo supera el límite de {MAX_MB} MB.")
    ext = nombre.lower().rsplit(".", 1)[-1]
    if ext in ("xlsx", "xls"):
        return pd.read_excel(io.BytesIO(contenido))
    if ext == "csv":
        for enc in CODIFICACIONES:
            try:
                # sep=None detecta automáticamente , ; o tab
                return pd.read_csv(io.BytesIO(contenido), sep=None, engine="python", encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError("No se pudo detectar la codificación del CSV.")
    raise ValueError("Formato no soportado. Use .csv, .xlsx o .xls")

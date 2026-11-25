"""Privacidad (Ley 25.326): anonimiza columnas sensibles y construye el contexto que
se envía a la IA. NUNCA se envía la planilla completa, solo resúmenes estadísticos."""
import re
import pandas as pd

PATRON_SENSIBLE = re.compile(r"(dni|cuil|cuit|nombre|apellido|mail|correo|tel|celular|direcc|domicilio)", re.I)


def columnas_sensibles(df: pd.DataFrame):
    return [c for c in df.columns if PATRON_SENSIBLE.search(str(c))]


def anonimizar(df: pd.DataFrame) -> pd.DataFrame:
    sens = columnas_sensibles(df)
    return df.drop(columns=sens), sens


def contexto_para_ia(df: pd.DataFrame) -> str:
    """Resumen anonimizado y compacto: estructura, estadísticas y frecuencias."""
    limpio, ocultas = anonimizar(df)
    partes = [f"Filas: {len(limpio)}. Columnas: {', '.join(map(str, limpio.columns))}."]
    if ocultas:
        partes.append(f"Columnas sensibles omitidas: {len(ocultas)}.")
    num = limpio.select_dtypes("number")
    if not num.empty:
        partes.append("Estadísticas numéricas:\n" + num.describe().T.round(2).to_string())
        if num.shape[1] > 1:
            partes.append("Correlaciones:\n" + num.corr().round(2).to_string())
    for c in limpio.select_dtypes(exclude="number").columns[:5]:
        if limpio[c].nunique() <= 30:
            partes.append(f"Frecuencias de {c}:\n" + limpio[c].value_counts().head(10).to_string())
    return "\n\n".join(partes)

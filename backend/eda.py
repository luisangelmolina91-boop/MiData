"""F2 - Análisis exploratorio automatizado."""
import pandas as pd


def estadisticas(df: pd.DataFrame) -> pd.DataFrame:
    num = df.select_dtypes("number")
    return num.describe().T.round(2) if not num.empty else pd.DataFrame()


def frecuencias(df: pd.DataFrame, col: str, top: int = 10) -> pd.DataFrame:
    return df[col].value_counts().head(top).rename_axis(col).reset_index(name="frecuencia")


def correlaciones(df: pd.DataFrame) -> pd.DataFrame:
    num = df.select_dtypes("number")
    return num.corr().round(2) if num.shape[1] > 1 else pd.DataFrame()


def columnas_categoricas(df: pd.DataFrame):
    return [c for c in df.columns if df[c].dtype == "object" or str(df[c].dtype) in ("category", "string", "str")]

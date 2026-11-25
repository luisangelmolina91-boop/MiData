"""F1 - Salud de datos: estructura, nulos, duplicados y outliers (IQR)."""
import pandas as pd


def resumen_estructura(df: pd.DataFrame) -> dict:
    return {"filas": len(df), "columnas": df.shape[1],
            "duplicados": int(df.duplicated().sum()),
            "nulos_totales": int(df.isna().sum().sum())}


def tabla_columnas(df: pd.DataFrame) -> pd.DataFrame:
    n = max(len(df), 1)
    return pd.DataFrame({
        "columna": df.columns,
        "tipo": [str(t) for t in df.dtypes],
        "nulos": df.isna().sum().values,
        "% nulos": (df.isna().sum().values / n * 100).round(1),
        "únicos": [df[c].nunique() for c in df.columns],
    })


def outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    """Valores atípicos por Rango Intercuartílico: fuera de [Q1-1.5*IQR, Q3+1.5*IQR]."""
    filas = []
    for c in df.select_dtypes("number").columns:
        s = df[c].dropna()
        if s.empty:
            continue
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n = int(((s < lo) | (s > hi)).sum())
        filas.append({"columna": c, "límite inferior": round(lo, 2),
                      "límite superior": round(hi, 2), "atípicos": n})
    return pd.DataFrame(filas)

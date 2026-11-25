"""Gráficos dinámicos con Plotly (barras, líneas, dispersión, histograma)."""
import plotly.express as px

PALETA = ["#0F5C6B", "#C8962E", "#B5482F", "#3C8DAD", "#7A5C1E"]


def grafico(df, tipo: str, x: str, y: str | None = None):
    kw = dict(color_discrete_sequence=PALETA)
    if tipo == "Barras":
        d = df.groupby(x)[y].sum().reset_index() if y else df[x].value_counts().rename_axis(x).reset_index(name="frecuencia")
        return px.bar(d, x=x, y=y or "frecuencia", **kw)
    if tipo == "Líneas":
        return px.line(df.sort_values(x), x=x, y=y, **kw)
    if tipo == "Dispersión":
        return px.scatter(df, x=x, y=y, **kw)
    return px.histogram(df, x=x, **kw)

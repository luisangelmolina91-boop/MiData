"""F3 - Asistente conversacional. La IA responde SOLO con el resumen anonimizado
(RAG sobre métricas locales). Proveedor intercambiable: ver llamar_llm()."""
import os
from .privacidad import contexto_para_ia

SISTEMA = ("Sos el asistente de MiData. Respondé en el idioma del usuario usando EXCLUSIVAMENTE "
           "el resumen de datos provisto. Si la respuesta no está en el resumen, decí que no "
           "se puede determinar con los datos cargados. Indicá de qué estadística proviene cada dato.")


def llamar_llm(system: str, pregunta: str) -> str:
    """Punto único de integración con la API. Por defecto usa Anthropic; para cambiar de
    proveedor solo se reemplaza esta función."""
    import anthropic  # pip install anthropic
    cliente = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    r = cliente.messages.create(model=os.environ.get("MIDATA_MODELO", "claude-sonnet-4-6"),
                                max_tokens=800, system=system,
                                messages=[{"role": "user", "content": pregunta}])
    return r.content[0].text


def responder(df, pregunta: str) -> tuple[str, str]:
    """Devuelve (respuesta, contexto_enviado) para mostrar la trazabilidad."""
    ctx = contexto_para_ia(df)
    return llamar_llm(f"{SISTEMA}\n\nRESUMEN DE DATOS:\n{ctx}", pregunta), ctx

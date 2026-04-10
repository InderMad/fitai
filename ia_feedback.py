# ia_feedback.py
# Este archivo contiene la función que llama a la API de Claude
# para generar feedback personalizado tras cada sesión.

import os
import anthropic


def generar_feedback_sesion(perfil, resultados, fase_actual, info_semana):
    """
    Genera un análisis personalizado de la sesión usando Claude.

    perfil       → datos del usuario (nombre, nivel, objetivo...)
    resultados   → lista de resultados del algoritmo de IA
    fase_actual  → fase del bloque actual (adaptación, acumulación...)
    info_semana  → información sobre la semana del bloque

    Devuelve un string con el feedback en texto, o un mensaje
    de error si la API no está disponible.
    """

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None  # Si no hay API key, no mostramos nada

    # Construir el resumen de la sesión para pasarle a Claude
    resumen_ejercicios = []
    for r in resultados:
        resumen_ejercicios.append(
            f"- {r['ejercicio']}: usó {r['peso_usado']}kg, "
            f"completó {r['pct_reps']:.0f}% de las reps, "
            f"RPE promedio {r['rpe_promedio']:.1f}, "
            f"decisión: {r['decision']} → {r['nuevo_peso']}kg"
        )

    ejercicios_texto = "\n".join(resumen_ejercicios)

    subidas  = sum(1 for r in resultados if r["decision"] == "subir")
    bajadas  = sum(1 for r in resultados if r["decision"] == "bajar")
    mantiene = sum(1 for r in resultados if r["decision"] == "mantener")

    # El prompt que le pasamos a Claude
    # Cuanto más detallado y específico sea el prompt,
    # mejor será el feedback generado
    prompt = f"""Eres un entrenador personal experto y motivador. 
Analiza esta sesión de entrenamiento y da feedback personalizado en español.

DATOS DEL USUARIO:
- Nombre: {perfil.get('nombre', 'Usuario')}
- Nivel: {perfil.get('nivel_texto', 'Intermedio')}
- Objetivo: {perfil.get('objetivo', 'Ganar músculo')}
- Género: {perfil.get('genero', 'No especificado')}

CONTEXTO DEL BLOQUE:
- Bloque número: {info_semana['numero_bloque']}
- Semana del bloque: {info_semana['semana_en_bloque']} de 8
- Fase actual: {fase_actual['nombre']}
- Descripción de la fase: {fase_actual['descripcion']}
- RPE objetivo para esta fase: {fase_actual['rpe_objetivo']}/10

RESULTADOS DE LA SESIÓN:
{ejercicios_texto}

RESUMEN:
- Ejercicios que suben de peso: {subidas}
- Ejercicios que se mantienen: {mantiene}
- Ejercicios que bajan de peso: {bajadas}

INSTRUCCIONES PARA TU RESPUESTA:
1. Empieza con una valoración general de la sesión (1-2 frases)
2. Menciona 1-2 puntos positivos específicos con datos concretos
3. Si hay algo a mejorar, dilo de forma constructiva (máximo 1 punto)
4. Contextualiza en qué fase del bloque están y qué esperar las próximas semanas
5. Termina con una frase motivadora corta y personalizada

FORMATO:
- Máximo 150 palabras en total
- Tono cercano, profesional y motivador
- Usa el nombre del usuario
- No uses bullet points ni listas, escribe en párrafos naturales
- No menciones que eres una IA"""

    try:
        cliente   = anthropic.Anthropic(api_key=api_key)
        respuesta = cliente.messages.create(
            model      = "claude-haiku-4-5-20251001",  # Modelo rápido y económico
            max_tokens = 300,
            messages   = [{"role": "user", "content": prompt}]
        )
        return respuesta.content[0].text

    except Exception as e:
        # Si hay cualquier error (sin créditos, sin conexión, etc.)
        # simplemente no mostramos el feedback en lugar de romper la app
        return None
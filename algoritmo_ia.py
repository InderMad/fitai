# algoritmo_ia.py
# Este archivo contiene el algoritmo que analiza el rendimiento
# del usuario y decide qué hacer con los pesos en la siguiente sesión.
# No tiene nada visual, solo lógica pura.


def calcular_nuevo_peso(peso_actual, porcentaje_cambio, subir=True):
    """
    Calcula el nuevo peso redondeado al múltiplo de 2.5 más cercano.

    peso_actual      → peso que usó el usuario esta sesión
    porcentaje_cambio → cuánto subir o bajar (ej: 0.05 = 5%)
    subir            → True si subimos, False si bajamos
    """
    if subir:
        nuevo_peso = peso_actual * (1 + porcentaje_cambio)
    else:
        nuevo_peso = peso_actual * (1 - porcentaje_cambio)

    # Redondear al múltiplo de 2.5 más cercano
    nuevo_peso_redondeado = round(nuevo_peso / 2.5) * 2.5

    # Nunca devolver menos de 2.5kg
    return max(nuevo_peso_redondeado, 2.5)


def analizar_ejercicio(nombre_ejercicio, series_registradas, reps_objetivo):
    """
    Analiza el rendimiento en un ejercicio y decide qué hacer.

    nombre_ejercicio  → nombre del ejercicio (para el mensaje)
    series_registradas → lista de diccionarios con:
                         {"peso": float, "reps": int, "rpe": int}
    reps_objetivo     → cuántas reps debía hacer por serie

    Devuelve un diccionario con:
        decision      → "subir", "mantener" o "bajar"
        nuevo_peso    → el peso recomendado para la próxima sesión
        mensaje       → explicación en texto para el usuario
        emoji         → ⬆️, ➡️ o ⬇️
        color         → "green", "blue" u "orange" para colorear en la app
    """

    # --- Calcular métricas ---
    total_series = len(series_registradas)

    if total_series == 0:
        return None

    # Peso promedio usado (por si el usuario cambió el peso entre series)
    peso_promedio = sum(s["peso"] for s in series_registradas) / total_series

    # Repeticiones promedio completadas
    reps_promedio = sum(s["reps"] for s in series_registradas) / total_series

    # RPE promedio
    rpe_promedio = sum(s["rpe"] for s in series_registradas) / total_series

    # Porcentaje de repeticiones completadas respecto al objetivo
    pct_reps = (reps_promedio / reps_objetivo) * 100 if reps_objetivo > 0 else 0

    # --- Aplicar la lógica de decisión ---
    if pct_reps >= 100 and rpe_promedio <= 7:
        # Completó todo y le resultó fácil → subir peso
        decision   = "subir"
        nuevo_peso = calcular_nuevo_peso(peso_promedio, 0.05, subir=True)
        emoji      = "⬆️"
        color      = "green"
        razon      = f"completaste todas las reps con esfuerzo bajo (RPE {rpe_promedio:.1f})"

    elif pct_reps >= 100 and rpe_promedio <= 9:
        # Completó todo pero al límite → mantener
        decision   = "mantener"
        nuevo_peso = calcular_nuevo_peso(peso_promedio, 0, subir=True)
        emoji      = "➡️"
        color      = "blue"
        razon      = f"completaste todas las reps pero el esfuerzo fue alto (RPE {rpe_promedio:.1f})"

    elif pct_reps >= 90:
        # Casi completó todo → mantener
        decision   = "mantener"
        nuevo_peso = calcular_nuevo_peso(peso_promedio, 0, subir=True)
        emoji      = "➡️"
        color      = "blue"
        razon      = f"completaste el {pct_reps:.0f}% de las reps — muy cerca del objetivo"

    elif pct_reps < 90 and rpe_promedio >= 8:
        # Falló bastantes reps y le costó mucho → bajar peso
        decision   = "bajar"
        nuevo_peso = calcular_nuevo_peso(peso_promedio, 0.05, subir=False)
        emoji      = "⬇️"
        color      = "orange"
        razon      = f"solo completaste el {pct_reps:.0f}% de las reps con esfuerzo alto (RPE {rpe_promedio:.1f})"

    else:
        # Falló reps pero no por esfuerzo → posible problema de técnica
        decision   = "mantener"
        nuevo_peso = calcular_nuevo_peso(peso_promedio, 0, subir=True)
        emoji      = "➡️"
        color      = "blue"
        razon      = f"completaste el {pct_reps:.0f}% de las reps — revisa la técnica del ejercicio"

    # Construir el mensaje final que verá el usuario
    if decision == "subir":
        mensaje = f"Sube a **{nuevo_peso} kg** la próxima sesión — {razon}."
    elif decision == "bajar":
        mensaje = f"Baja a **{nuevo_peso} kg** la próxima sesión — {razon}."
    else:
        mensaje = f"Mantén **{nuevo_peso} kg** la próxima sesión — {razon}."

    return {
        "ejercicio":   nombre_ejercicio,
        "decision":    decision,
        "nuevo_peso":  nuevo_peso,
        "peso_usado":  peso_promedio,
        "pct_reps":    pct_reps,
        "rpe_promedio":rpe_promedio,
        "mensaje":     mensaje,
        "emoji":       emoji,
        "color":       color
    }


def analizar_sesion_completa(registros_sesion, reps_objetivo):
    """
    Analiza todos los ejercicios de una sesión completa.

    registros_sesion → diccionario donde cada clave es el nombre
                       del ejercicio y el valor es una lista de series:
                       {
                         "Press de banca": [
                             {"peso": 32.5, "reps": 10, "rpe": 7},
                             {"peso": 32.5, "reps": 10, "rpe": 8},
                             ...
                         ],
                         ...
                       }
    reps_objetivo    → número de reps objetivo (igual para todos los ejercicios)

    Devuelve una lista de resultados, uno por ejercicio.
    """
    resultados = []

    for nombre_ejercicio, series in registros_sesion.items():
        resultado = analizar_ejercicio(nombre_ejercicio, series, reps_objetivo)
        if resultado:
            resultados.append(resultado)

    return resultados
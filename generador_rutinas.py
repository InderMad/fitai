# generador_rutinas.py

EJERCICIOS = {

    "gimnasio_completo": {

        "pecho": [
            {"nombre": "Press de banca con barra",        "nivel_min": 2, "peso_inicial_pct": 0.45},
            {"nombre": "Press de banca en máquina",       "nivel_min": 1, "peso_inicial_pct": 0.40},
            {"nombre": "Press inclinado con mancuernas",  "nivel_min": 1, "peso_inicial_pct": 0.14},
            {"nombre": "Aperturas en máquina (pec deck)", "nivel_min": 1, "peso_inicial_pct": 0.25},
            {"nombre": "Press declinado con barra",       "nivel_min": 2, "peso_inicial_pct": 0.50},
        ],
        "espalda": [
            {"nombre": "Jalón al pecho en polea",         "nivel_min": 1, "peso_inicial_pct": 0.45},
            {"nombre": "Remo en polea baja",              "nivel_min": 1, "peso_inicial_pct": 0.40},
            {"nombre": "Remo con mancuerna",              "nivel_min": 1, "peso_inicial_pct": 0.18},
            {"nombre": "Dominadas asistidas",             "nivel_min": 2, "peso_inicial_pct": 0.00},
            {"nombre": "Remo con barra",                  "nivel_min": 2, "peso_inicial_pct": 0.40},
            {"nombre": "Pullover en polea",               "nivel_min": 1, "peso_inicial_pct": 0.25},
        ],
        "hombros": [
            {"nombre": "Press de hombro en máquina",      "nivel_min": 1, "peso_inicial_pct": 0.22},
            {"nombre": "Press militar con barra",         "nivel_min": 2, "peso_inicial_pct": 0.30},
            {"nombre": "Elevaciones laterales",           "nivel_min": 1, "peso_inicial_pct": 0.05},
            {"nombre": "Pájaros con mancuernas",          "nivel_min": 1, "peso_inicial_pct": 0.05},
        ],
        "piernas": [
            {"nombre": "Sentadilla con barra",            "nivel_min": 2, "peso_inicial_pct": 0.65},
            {"nombre": "Sentadilla en máquina",           "nivel_min": 1, "peso_inicial_pct": 0.55},
            {"nombre": "Prensa de piernas",               "nivel_min": 1, "peso_inicial_pct": 0.90},
            {"nombre": "Extensión de cuádriceps",         "nivel_min": 1, "peso_inicial_pct": 0.32},
            {"nombre": "Curl femoral tumbado",            "nivel_min": 1, "peso_inicial_pct": 0.28},
            {"nombre": "Elevación de talones de pie",     "nivel_min": 1, "peso_inicial_pct": 0.40},
        ],
        "gluteos": [
            {"nombre": "Hip thrust con barra",            "nivel_min": 1, "peso_inicial_pct": 0.70},
            {"nombre": "Patada de glúteo en polea",       "nivel_min": 1, "peso_inicial_pct": 0.15},
            {"nombre": "Peso muerto rumano",              "nivel_min": 2, "peso_inicial_pct": 0.55},
            {"nombre": "Abducción de cadera en máquina",  "nivel_min": 1, "peso_inicial_pct": 0.30},
            {"nombre": "Zancada con mancuernas",          "nivel_min": 1, "peso_inicial_pct": 0.14},
            {"nombre": "Sentadilla sumo con mancuerna",   "nivel_min": 1, "peso_inicial_pct": 0.25},
        ],
        "biceps": [
            {"nombre": "Curl con barra recta",            "nivel_min": 1, "peso_inicial_pct": 0.16},
            {"nombre": "Curl con mancuernas alterno",     "nivel_min": 1, "peso_inicial_pct": 0.09},
            {"nombre": "Curl en polea baja",              "nivel_min": 1, "peso_inicial_pct": 0.14},
            {"nombre": "Curl martillo con mancuernas",    "nivel_min": 1, "peso_inicial_pct": 0.10},
        ],
        "triceps": [
            {"nombre": "Extensión de tríceps en polea",   "nivel_min": 1, "peso_inicial_pct": 0.22},
            {"nombre": "Press francés con barra",         "nivel_min": 2, "peso_inicial_pct": 0.20},
            {"nombre": "Fondos en paralelas",             "nivel_min": 2, "peso_inicial_pct": 0.00},
            {"nombre": "Extensión sobre cabeza en polea", "nivel_min": 1, "peso_inicial_pct": 0.18},
        ],
    },

    "mancuernas": {
        "pecho": [
            {"nombre": "Press con mancuernas en suelo",   "nivel_min": 1, "peso_inicial_pct": 0.14},
            {"nombre": "Aperturas con mancuernas",        "nivel_min": 1, "peso_inicial_pct": 0.08},
        ],
        "espalda": [
            {"nombre": "Remo con mancuerna",              "nivel_min": 1, "peso_inicial_pct": 0.18},
            {"nombre": "Pullover con mancuerna",          "nivel_min": 1, "peso_inicial_pct": 0.12},
        ],
        "hombros": [
            {"nombre": "Press de hombro con mancuernas",  "nivel_min": 1, "peso_inicial_pct": 0.10},
            {"nombre": "Elevaciones laterales",           "nivel_min": 1, "peso_inicial_pct": 0.05},
        ],
        "piernas": [
            {"nombre": "Sentadilla con mancuernas",       "nivel_min": 1, "peso_inicial_pct": 0.18},
            {"nombre": "Zancadas con mancuernas",         "nivel_min": 1, "peso_inicial_pct": 0.14},
            {"nombre": "Peso muerto rumano con mancuernas","nivel_min": 1, "peso_inicial_pct": 0.20},
        ],
        "gluteos": [
            {"nombre": "Hip thrust con mancuerna",        "nivel_min": 1, "peso_inicial_pct": 0.25},
            {"nombre": "Sentadilla sumo con mancuerna",   "nivel_min": 1, "peso_inicial_pct": 0.20},
            {"nombre": "Zancada con mancuernas",          "nivel_min": 1, "peso_inicial_pct": 0.14},
        ],
        "biceps": [
            {"nombre": "Curl con mancuernas",             "nivel_min": 1, "peso_inicial_pct": 0.09},
            {"nombre": "Curl martillo",                   "nivel_min": 1, "peso_inicial_pct": 0.10},
        ],
        "triceps": [
            {"nombre": "Extensión de tríceps con mancuerna","nivel_min": 1, "peso_inicial_pct": 0.08},
            {"nombre": "Fondos entre sillas",             "nivel_min": 1, "peso_inicial_pct": 0.00},
        ],
    },

    "sin_equipamiento": {
        "pecho": [
            {"nombre": "Flexiones",                            "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Flexiones declinadas (pies en silla)", "nivel_min": 2, "peso_inicial_pct": 0.00},
        ],
        "espalda": [
            {"nombre": "Superman en suelo",                    "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Remo con toalla en puerta",            "nivel_min": 1, "peso_inicial_pct": 0.00},
        ],
        "hombros": [
            {"nombre": "Flexiones pike",                       "nivel_min": 2, "peso_inicial_pct": 0.00},
        ],
        "piernas": [
            {"nombre": "Sentadilla con peso corporal",         "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Zancadas",                             "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Sentadilla búlgara",                   "nivel_min": 2, "peso_inicial_pct": 0.00},
        ],
        "gluteos": [
            {"nombre": "Puente de glúteos",                    "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Hip thrust con peso corporal",         "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Patada de glúteo en cuadrupedia",      "nivel_min": 1, "peso_inicial_pct": 0.00},
        ],
        "biceps": [
            {"nombre": "Curl con toalla (resistencia manual)", "nivel_min": 1, "peso_inicial_pct": 0.00},
        ],
        "triceps": [
            {"nombre": "Fondos entre sillas",                  "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Flexiones diamante",                   "nivel_min": 2, "peso_inicial_pct": 0.00},
        ],
    },
}


# =====================================================
# TÉCNICAS AVANZADAS (solo nivel 3)
# =====================================================
# Estas técnicas se añaden como nota al ejercicio
# para que el usuario sepa cómo ejecutarlas

TECNICAS_AVANZADAS = {
    "drop_set": {
        "nombre": "Drop Set",
        "descripcion": "Al fallar, reduce el peso un 20% y continúa hasta fallar de nuevo. Sin descanso entre reducciones.",
        "abreviatura": "DS"
    },
    "rest_pause": {
        "nombre": "Rest-Pause",
        "descripcion": "Al fallar, descansa 15 segundos sin soltar la barra y continúa. Repite 2–3 veces.",
        "abreviatura": "RP"
    },
    "series_descendentes": {
        "nombre": "Series Descendentes",
        "descripcion": "Haz la serie principal, descansa 10s, reduce 10% de peso y haz otra serie.",
        "abreviatura": "SD"
    }
}


def calcular_peso_inicial(peso_usuario, porcentaje):
    if porcentaje == 0:
        return None
    peso_raw = peso_usuario * porcentaje
    peso_redondeado = round(peso_raw / 2.5) * 2.5
    return max(peso_redondeado, 2.5)


def seleccionar_ejercicios(banco, grupos, nivel, peso_usuario, num_ejercicios):
    ejercicios_seleccionados = []
    for grupo in grupos:
        disponibles = [
            e for e in banco.get(grupo, [])
            if e["nivel_min"] <= nivel
        ]
        elegidos = disponibles[:num_ejercicios]
        for e in elegidos:
            ejercicios_seleccionados.append({
                "grupo":         grupo,
                "nombre":        e["nombre"],
                "peso_sugerido": calcular_peso_inicial(peso_usuario, e["peso_inicial_pct"]),
                "tecnica":       None   # Se rellena para avanzados
            })
    return ejercicios_seleccionados


def generar_rutina(perfil):
    """
    Genera una rutina completa teniendo en cuenta:
    - género (para priorizar grupos musculares)
    - músculos prioritarios elegidos por el usuario
    - nivel (para añadir técnicas avanzadas)
    """
    nivel        = perfil["nivel_num"]
    dias         = perfil["dias"]
    peso         = perfil["peso"]
    objetivo     = perfil["objetivo"]
    minutos      = perfil["minutos"]
    equip_raw    = perfil["equipamiento"]
    genero       = perfil.get("genero", "Prefiero no decirlo")
    prioritarios = perfil.get("musculos_prioritarios", [])

    # Normalizar equipamiento
    if "gimnasio" in equip_raw.lower():
        equip_key = "gimnasio_completo"
    elif "mancuernas" in equip_raw.lower():
        equip_key = "mancuernas"
    else:
        equip_key = "sin_equipamiento"

    banco = EJERCICIOS[equip_key]

    # --------------------------------------------------
    # Parámetros según objetivo
    # --------------------------------------------------
    if "músculo" in objetivo or "hipertrofia" in objetivo.lower():
        series = 4; reps_min = 8;  reps_max = 12; descanso = 90
    elif "grasa" in objetivo.lower():
        series = 3; reps_min = 12; reps_max = 15; descanso = 60
    elif "fuerza" in objetivo.lower():
        series = 5; reps_min = 4;  reps_max = 6;  descanso = 180
    else:
        series = 3; reps_min = 10; reps_max = 15; descanso = 75

    if nivel == 1:
        series = 3; reps_min = 10; reps_max = 12

    # --------------------------------------------------
    # Estructura según días
    # --------------------------------------------------
    if dias <= 3:
        estructura = "fullbody"
    elif dias == 4:
        estructura = "torso_pierna"
    else:
        estructura = "push_pull_legs"

    ejercicios_por_sesion = minutos // 12

    # --------------------------------------------------
    # Calcular grupos extra por género y prioritarios
    # --------------------------------------------------
    # Los músculos prioritarios reciben el doble de ejercicios
    # Para mujeres, si no ha elegido prioritarios, se añaden glúteos por defecto

    grupos_extra = list(prioritarios)  # copia para no modificar el original

    if genero == "Mujer" and "gluteos" not in grupos_extra and not prioritarios:
        grupos_extra = ["gluteos", "piernas"]

    # --------------------------------------------------
    # Construir días según estructura
    # --------------------------------------------------
    dias_rutina = []

    if estructura == "fullbody":
        nombres_dias = {2: ["Lunes", "Jueves"], 3: ["Lunes", "Miércoles", "Viernes"]}
        grupos_base  = ["piernas", "pecho", "espalda", "hombros", "biceps", "triceps"]

        # Añadir grupos prioritarios si no están ya
        for g in grupos_extra:
            if g not in grupos_base:
                grupos_base.insert(1, g)  # Insertar después de piernas

        sesion = seleccionar_ejercicios(banco, grupos_base, nivel, peso, 1)

        # Dar doble ejercicio a los grupos prioritarios
        for g in grupos_extra:
            extra = seleccionar_ejercicios(banco, [g], nivel, peso, 2)
            if len(extra) > 1:
                sesion.append(extra[1])

        sesion = sesion[:ejercicios_por_sesion]

        for nombre_dia in nombres_dias.get(dias, ["Día 1", "Día 2", "Día 3"]):
            dias_rutina.append({
                "dia":       nombre_dia,
                "enfoque":   "Cuerpo completo",
                "ejercicios": [dict(e) for e in sesion]
            })

    elif estructura == "torso_pierna":
        # En torso/pierna, si hay prioritarios en tren inferior, se añaden al día de pierna
        grupos_pierna = ["piernas"]
        if "gluteos" in grupos_extra or genero == "Mujer":
            grupos_pierna = ["gluteos", "piernas"]

        dias_config = [
            {"dia": "Lunes",   "enfoque": "Torso", "grupos": ["pecho", "espalda", "hombros", "biceps", "triceps"]},
            {"dia": "Martes",  "enfoque": "Pierna + Glúteos" if "gluteos" in grupos_pierna else "Pierna", "grupos": grupos_pierna},
            {"dia": "Jueves",  "enfoque": "Torso", "grupos": ["pecho", "espalda", "hombros", "biceps", "triceps"]},
            {"dia": "Viernes", "enfoque": "Pierna + Glúteos" if "gluteos" in grupos_pierna else "Pierna", "grupos": grupos_pierna},
        ]

        for config in dias_config:
            num_por_grupo = 3 if any(g in grupos_extra for g in config["grupos"]) else 2
            ejercicios    = seleccionar_ejercicios(banco, config["grupos"], nivel, peso, num_por_grupo)
            ejercicios    = ejercicios[:ejercicios_por_sesion]
            dias_rutina.append({
                "dia":        config["dia"],
                "enfoque":    config["enfoque"],
                "ejercicios": ejercicios
            })

    else:  # push_pull_legs
        # En PPL, si hay prioritarios en glúteos o piernas, el día de Legs tiene más volumen
        grupos_legs = ["piernas"]
        if "gluteos" in grupos_extra or genero == "Mujer":
            grupos_legs = ["gluteos", "piernas"]

        enfoque_legs = "Legs + Glúteos" if len(grupos_legs) > 1 else "Legs (Piernas)"

        dias_config = [
            {"dia": "Lunes",     "enfoque": "Push (Pecho, Hombros, Tríceps)", "grupos": ["pecho", "hombros", "triceps"]},
            {"dia": "Martes",    "enfoque": "Pull (Espalda, Bíceps)",          "grupos": ["espalda", "biceps"]},
            {"dia": "Miércoles", "enfoque": enfoque_legs,                      "grupos": grupos_legs},
            {"dia": "Jueves",    "enfoque": "Push (Pecho, Hombros, Tríceps)", "grupos": ["pecho", "hombros", "triceps"]},
            {"dia": "Viernes",   "enfoque": "Pull (Espalda, Bíceps)",          "grupos": ["espalda", "biceps"]},
        ]
        if dias == 6:
            dias_config.append({"dia": "Sábado", "enfoque": enfoque_legs, "grupos": grupos_legs})

        for config in dias_config:
            # Más ejercicios en grupos prioritarios
            num_por_grupo = 3 if any(g in grupos_extra for g in config["grupos"]) else 2
            ejercicios    = seleccionar_ejercicios(banco, config["grupos"], nivel, peso, num_por_grupo)
            ejercicios    = ejercicios[:ejercicios_por_sesion]
            dias_rutina.append({
                "dia":        config["dia"],
                "enfoque":    config["enfoque"],
                "ejercicios": ejercicios
            })

    # --------------------------------------------------
    # Añadir series, reps y técnicas avanzadas
    # --------------------------------------------------
    import random
    tecnicas_disponibles = list(TECNICAS_AVANZADAS.values())

    for dia in dias_rutina:
        for idx, ejercicio in enumerate(dia["ejercicios"]):
            ejercicio["series"]   = series
            ejercicio["reps_min"] = reps_min
            ejercicio["reps_max"] = reps_max
            ejercicio["tecnica"]  = None

            # Solo para avanzados (nivel 3): añadir técnica avanzada
            # en el último ejercicio de cada grupo muscular
            if nivel == 3:
                # Comprobar si es el último ejercicio de su grupo en esta sesión
                mismo_grupo = [e for e in dia["ejercicios"] if e["grupo"] == ejercicio["grupo"]]
                if mismo_grupo and ejercicio == mismo_grupo[-1]:
                    tecnica = random.choice(tecnicas_disponibles)
                    ejercicio["tecnica"] = tecnica

    return {
        "estructura":   estructura,
        "series":       series,
        "reps_min":     reps_min,
        "reps_max":     reps_max,
        "descanso_seg": descanso,
        "dias":         dias_rutina
    }
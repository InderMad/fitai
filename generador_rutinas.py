# generador_rutinas.py
# Este archivo contiene toda la lógica para generar rutinas personalizadas.
# No tiene nada visual, solo cálculos y decisiones.

# =====================================================
# BASE DE DATOS DE EJERCICIOS
# =====================================================
# Estructura de cada ejercicio:
#   "nombre"           → cómo se llama el ejercicio
#   "nivel_min"        → nivel mínimo para hacerlo (1=principiante, 2=intermedio, 3=avanzado)
#   "peso_inicial_pct" → peso inicial sugerido como fracción del peso corporal del usuario
#                        Ejemplo: 0.6 significa 60% del peso corporal
#                        Si es 0, el ejercicio usa peso corporal (sin barra ni mancuernas)

EJERCICIOS = {

    # --------------------------------------------------
    # GIMNASIO COMPLETO
    # --------------------------------------------------
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
            {"nombre": "Hip thrust con barra",            "nivel_min": 2, "peso_inicial_pct": 0.70},
            {"nombre": "Peso muerto rumano",              "nivel_min": 2, "peso_inicial_pct": 0.55},
            {"nombre": "Elevación de talones de pie",     "nivel_min": 1, "peso_inicial_pct": 0.40},
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

    # --------------------------------------------------
    # MANCUERNAS EN CASA
    # --------------------------------------------------
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
        "biceps": [
            {"nombre": "Curl con mancuernas",             "nivel_min": 1, "peso_inicial_pct": 0.09},
            {"nombre": "Curl martillo",                   "nivel_min": 1, "peso_inicial_pct": 0.10},
        ],
        "triceps": [
            {"nombre": "Extensión de tríceps con mancuerna","nivel_min": 1, "peso_inicial_pct": 0.08},
            {"nombre": "Fondos entre sillas",             "nivel_min": 1, "peso_inicial_pct": 0.00},
        ],
    },

    # --------------------------------------------------
    # SIN EQUIPAMIENTO
    # --------------------------------------------------
    "sin_equipamiento": {
        "pecho":   [
            {"nombre": "Flexiones",                       "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Flexiones declinadas (pies en silla)","nivel_min": 2, "peso_inicial_pct": 0.00},
        ],
        "espalda": [
            {"nombre": "Superman en suelo",               "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Remo con toalla en puerta",       "nivel_min": 1, "peso_inicial_pct": 0.00},
        ],
        "hombros": [
            {"nombre": "Flexiones pike",                  "nivel_min": 2, "peso_inicial_pct": 0.00},
        ],
        "piernas": [
            {"nombre": "Sentadilla con peso corporal",    "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Zancadas",                        "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Sentadilla búlgara",              "nivel_min": 2, "peso_inicial_pct": 0.00},
            {"nombre": "Puente de glúteos",               "nivel_min": 1, "peso_inicial_pct": 0.00},
        ],
        "biceps":  [
            {"nombre": "Curl con toalla (resistencia manual)","nivel_min": 1, "peso_inicial_pct": 0.00},
        ],
        "triceps": [
            {"nombre": "Fondos entre sillas",             "nivel_min": 1, "peso_inicial_pct": 0.00},
            {"nombre": "Flexiones diamante",              "nivel_min": 2, "peso_inicial_pct": 0.00},
        ],
    },
}


# =====================================================
# FUNCIÓN AUXILIAR: Calcular peso inicial
# =====================================================
def calcular_peso_inicial(peso_usuario, porcentaje):
    """
    Calcula el peso inicial para un ejercicio y lo redondea
    al múltiplo de 2.5 más cercano (como funcionan los discos del gimnasio).

    Ejemplo:
        peso_usuario = 73kg, porcentaje = 0.45
        73 * 0.45 = 32.85kg → redondeado a 32.5kg
    """
    if porcentaje == 0:
        return None  # Ejercicio de peso corporal, no aplica peso

    peso_raw = peso_usuario * porcentaje
    # Redondear al múltiplo de 2.5 más cercano
    peso_redondeado = round(peso_raw / 2.5) * 2.5
    return max(peso_redondeado, 2.5)  # Nunca devolver menos de 2.5kg


# =====================================================
# FUNCIÓN AUXILIAR: Seleccionar ejercicios
# =====================================================
def seleccionar_ejercicios(banco, grupos, nivel, peso_usuario, num_ejercicios):
    """
    Selecciona ejercicios de los grupos musculares indicados,
    filtrando por nivel y calculando el peso inicial de cada uno.

    banco          → diccionario de ejercicios (gimnasio, mancuernas, etc.)
    grupos         → lista de grupos musculares a incluir (ej: ["pecho", "triceps"])
    nivel          → nivel del usuario (1, 2 o 3)
    peso_usuario   → peso del usuario en kg
    num_ejercicios → cuántos ejercicios incluir por grupo
    """
    ejercicios_seleccionados = []

    for grupo in grupos:
        disponibles = [
            e for e in banco.get(grupo, [])
            if e["nivel_min"] <= nivel
        ]

        # Cogemos los primeros N ejercicios disponibles para ese grupo
        # (en versiones futuras esto rotará para dar variedad)
        elegidos = disponibles[:num_ejercicios]

        for e in elegidos:
            ejercicios_seleccionados.append({
                "grupo": grupo,
                "nombre": e["nombre"],
                "peso_sugerido": calcular_peso_inicial(peso_usuario, e["peso_inicial_pct"])
            })

    return ejercicios_seleccionados


# =====================================================
# FUNCIÓN PRINCIPAL: Generar rutina completa
# =====================================================
def generar_rutina(perfil):
    """
    Recibe el perfil del usuario y devuelve una rutina completa.

    El perfil debe tener estas claves:
        nombre, edad, peso, nivel_num, objetivo, dias, minutos, equipamiento

    Devuelve un diccionario con:
        estructura   → tipo de rutina (fullbody, torso_pierna, ppl)
        series       → número de series por ejercicio
        reps_min     → repeticiones mínimas objetivo
        reps_max     → repeticiones máximas objetivo
        descanso_seg → descanso entre series en segundos
        dias         → lista de días con sus ejercicios
    """

    nivel      = perfil["nivel_num"]
    dias       = perfil["dias"]
    peso       = perfil["peso"]
    objetivo   = perfil["objetivo"]
    minutos    = perfil["minutos"]
    equip_raw  = perfil["equipamiento"]

    # Normalizar el equipamiento al key del diccionario EJERCICIOS
    if "gimnasio" in equip_raw.lower():
        equip_key = "gimnasio_completo"
    elif "mancuernas" in equip_raw.lower():
        equip_key = "mancuernas"
    else:
        equip_key = "sin_equipamiento"

    banco = EJERCICIOS[equip_key]

    # --------------------------------------------------
    # PASO 1: Decidir parámetros según objetivo
    # --------------------------------------------------
    if "músculo" in objetivo or "hipertrofia" in objetivo.lower():
        series      = 4
        reps_min    = 8
        reps_max    = 12
        descanso    = 90   # segundos entre series

    elif "grasa" in objetivo.lower():
        series      = 3
        reps_min    = 12
        reps_max    = 15
        descanso    = 60

    elif "fuerza" in objetivo.lower():
        series      = 5
        reps_min    = 4
        reps_max    = 6
        descanso    = 180

    else:  # condición física general
        series      = 3
        reps_min    = 10
        reps_max    = 15
        descanso    = 75

    # Para principiantes, siempre reducimos el volumen al mínimo
    if nivel == 1:
        series   = 3
        reps_min = 10
        reps_max = 12

    # --------------------------------------------------
    # PASO 2: Decidir estructura según días disponibles
    # --------------------------------------------------
    if dias <= 3:
        estructura = "fullbody"
    elif dias == 4:
        estructura = "torso_pierna"
    else:
        estructura = "push_pull_legs"

    # --------------------------------------------------
    # PASO 3: Limitar ejercicios según tiempo disponible
    # Cada ejercicio ocupa aprox. 10–12 minutos
    # --------------------------------------------------
    ejercicios_por_sesion = minutos // 12

    # --------------------------------------------------
    # PASO 4: Construir los días según la estructura
    # --------------------------------------------------
    dias_rutina = []

    if estructura == "fullbody":
        nombres_dias = {2: ["Lunes", "Jueves"], 3: ["Lunes", "Miércoles", "Viernes"]}
        grupos_fullbody = ["piernas", "pecho", "espalda", "hombros", "biceps", "triceps"]
        ejercicios_por_grupo = 1

        ejercicios_sesion = seleccionar_ejercicios(
            banco, grupos_fullbody, nivel, peso, ejercicios_por_grupo
        )
        # Limitamos al tiempo disponible
        ejercicios_sesion = ejercicios_sesion[:ejercicios_por_sesion]

        for nombre_dia in nombres_dias.get(dias, ["Día 1", "Día 2", "Día 3"]):
            dias_rutina.append({
                "dia": nombre_dia,
                "enfoque": "Cuerpo completo",
                "ejercicios": [dict(e) for e in ejercicios_sesion]
            })

    elif estructura == "torso_pierna":
        # Alterna: Torso (lunes/miércoles) y Pierna (martes/jueves)
        dias_config = [
            {"dia": "Lunes",     "enfoque": "Torso", "grupos": ["pecho", "espalda", "hombros", "biceps", "triceps"]},
            {"dia": "Martes",    "enfoque": "Pierna","grupos": ["piernas"]},
            {"dia": "Jueves",    "enfoque": "Torso", "grupos": ["pecho", "espalda", "hombros", "biceps", "triceps"]},
            {"dia": "Viernes",   "enfoque": "Pierna","grupos": ["piernas"]},
        ]
        ejercicios_por_grupo = 2

        for config in dias_config:
            ejercicios = seleccionar_ejercicios(
                banco, config["grupos"], nivel, peso, ejercicios_por_grupo
            )
            ejercicios = ejercicios[:ejercicios_por_sesion]
            dias_rutina.append({
                "dia": config["dia"],
                "enfoque": config["enfoque"],
                "ejercicios": ejercicios
            })

    else:  # push_pull_legs (5–6 días)
        dias_config = [
            {"dia": "Lunes",     "enfoque": "Push (Pecho, Hombros, Tríceps)", "grupos": ["pecho", "hombros", "triceps"]},
            {"dia": "Martes",    "enfoque": "Pull (Espalda, Bíceps)",          "grupos": ["espalda", "biceps"]},
            {"dia": "Miércoles", "enfoque": "Legs (Piernas)",                  "grupos": ["piernas"]},
            {"dia": "Jueves",    "enfoque": "Push (Pecho, Hombros, Tríceps)", "grupos": ["pecho", "hombros", "triceps"]},
            {"dia": "Viernes",   "enfoque": "Pull (Espalda, Bíceps)",          "grupos": ["espalda", "biceps"]},
        ]
        if dias == 6:
            dias_config.append(
                {"dia": "Sábado", "enfoque": "Legs (Piernas)", "grupos": ["piernas"]}
            )

        ejercicios_por_grupo = 2

        for config in dias_config:
            ejercicios = seleccionar_ejercicios(
                banco, config["grupos"], nivel, peso, ejercicios_por_grupo
            )
            ejercicios = ejercicios[:ejercicios_por_sesion]
            dias_rutina.append({
                "dia": config["dia"],
                "enfoque": config["enfoque"],
                "ejercicios": ejercicios
            })

    # --------------------------------------------------
    # PASO 5: Añadir series y reps a cada ejercicio
    # (se hace aquí para que todos los ejercicios tengan
    #  los mismos parámetros base de la rutina)
    # --------------------------------------------------
    for dia in dias_rutina:
        for ejercicio in dia["ejercicios"]:
            ejercicio["series"]   = series
            ejercicio["reps_min"] = reps_min
            ejercicio["reps_max"] = reps_max

    return {
        "estructura":    estructura,
        "series":        series,
        "reps_min":      reps_min,
        "reps_max":      reps_max,
        "descanso_seg":  descanso,
        "dias":          dias_rutina
    }
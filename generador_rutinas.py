# generador_rutinas.py

import random

# =====================================================
# BASE DE DATOS DE EJERCICIOS
# =====================================================
# Estructura de cada ejercicio:
#   nombre          → nombre del ejercicio
#   nivel_min       → 1=principiante, 2=intermedio, 3=avanzado
#   peso_inicial_pct→ fracción del peso corporal para el peso inicial
#                     0.0 = peso corporal o sin peso externo

EJERCICIOS = {

    # --------------------------------------------------
    # PECHO
    # --------------------------------------------------
    "pecho": [
        {"nombre": "Flexiones",                                         "nivel_min": 1, "peso_inicial_pct": 0.00},
        {"nombre": "Fondos paralelas",                                  "nivel_min": 2, "peso_inicial_pct": 0.00},
        {"nombre": "Press banca mancuernas agarre prono",               "nivel_min": 1, "peso_inicial_pct": 0.14},
        {"nombre": "Press banca mancuernas agarre neutro",              "nivel_min": 1, "peso_inicial_pct": 0.14},
        {"nombre": "Press banca barra",                                 "nivel_min": 2, "peso_inicial_pct": 0.45},
        {"nombre": "Press banca máquina agarre prono",                  "nivel_min": 1, "peso_inicial_pct": 0.40},
        {"nombre": "Press banca máquina agarre neutro",                 "nivel_min": 1, "peso_inicial_pct": 0.40},
        {"nombre": "Press banca polea agarre prono",                    "nivel_min": 1, "peso_inicial_pct": 0.18},
        {"nombre": "Press banca polea agarre neutro",                   "nivel_min": 1, "peso_inicial_pct": 0.18},
        {"nombre": "Press banca inclinado mancuerna agarre prono",      "nivel_min": 1, "peso_inicial_pct": 0.12},
        {"nombre": "Press banca inclinado mancuerna agarre neutro",     "nivel_min": 1, "peso_inicial_pct": 0.12},
        {"nombre": "Press banca inclinado barra",                       "nivel_min": 2, "peso_inicial_pct": 0.40},
        {"nombre": "Press banca inclinado máquina agarre prono",        "nivel_min": 1, "peso_inicial_pct": 0.35},
        {"nombre": "Press banca inclinado máquina agarre neutro",       "nivel_min": 1, "peso_inicial_pct": 0.35},
        {"nombre": "Press banca inclinado polea agarre neutro",         "nivel_min": 1, "peso_inicial_pct": 0.15},
        {"nombre": "Press banca inclinado polea agarre prono",          "nivel_min": 1, "peso_inicial_pct": 0.15},
        {"nombre": "Aperturas pecho polea alta agarre neutro",          "nivel_min": 1, "peso_inicial_pct": 0.12},
        {"nombre": "Aperturas pecho polea media agarre neutro",         "nivel_min": 1, "peso_inicial_pct": 0.12},
        {"nombre": "Aperturas agarre supino polea baja",                "nivel_min": 1, "peso_inicial_pct": 0.10},
        {"nombre": "Apertura unilateral polea media agarre neutro",     "nivel_min": 1, "peso_inicial_pct": 0.08},
        {"nombre": "Apertura máquina plana agarre neutro",              "nivel_min": 1, "peso_inicial_pct": 0.25},
    ],

    # --------------------------------------------------
    # ESPALDA
    # --------------------------------------------------
    "espalda": [
        {"nombre": "Jalón agarre prono polea",                          "nivel_min": 1, "peso_inicial_pct": 0.45},
        {"nombre": "Jalón agarre neutro polea",                         "nivel_min": 1, "peso_inicial_pct": 0.45},
        {"nombre": "Jalón agarre supino polea",                         "nivel_min": 1, "peso_inicial_pct": 0.45},
        {"nombre": "Jalón agarre prono máquina",                        "nivel_min": 1, "peso_inicial_pct": 0.42},
        {"nombre": "Jalón agarre neutro máquina",                       "nivel_min": 1, "peso_inicial_pct": 0.42},
        {"nombre": "Jalón agarre supino máquina",                       "nivel_min": 1, "peso_inicial_pct": 0.42},
        {"nombre": "Jalón agarre prono polea unilateral",               "nivel_min": 1, "peso_inicial_pct": 0.22},
        {"nombre": "Jalón agarre neutro polea unilateral",              "nivel_min": 1, "peso_inicial_pct": 0.22},
        {"nombre": "Jalón agarre supino polea unilateral",              "nivel_min": 1, "peso_inicial_pct": 0.22},
        {"nombre": "Jalón agarre prono máquina unilateral",             "nivel_min": 1, "peso_inicial_pct": 0.20},
        {"nombre": "Jalón agarre neutro máquina unilateral",            "nivel_min": 1, "peso_inicial_pct": 0.20},
        {"nombre": "Jalón agarre supino máquina unilateral",            "nivel_min": 1, "peso_inicial_pct": 0.20},
        {"nombre": "Remo agarre prono polea",                           "nivel_min": 1, "peso_inicial_pct": 0.40},
        {"nombre": "Remo agarre neutro polea",                          "nivel_min": 1, "peso_inicial_pct": 0.40},
        {"nombre": "Remo agarre supino polea",                          "nivel_min": 1, "peso_inicial_pct": 0.40},
        {"nombre": "Remo agarre prono máquina",                         "nivel_min": 1, "peso_inicial_pct": 0.38},
        {"nombre": "Remo agarre neutro máquina",                        "nivel_min": 1, "peso_inicial_pct": 0.38},
        {"nombre": "Remo agarre supino máquina",                        "nivel_min": 1, "peso_inicial_pct": 0.38},
        {"nombre": "Remo agarre neutro mancuerna",                      "nivel_min": 1, "peso_inicial_pct": 0.18},
        {"nombre": "Peso muerto convencional",                          "nivel_min": 2, "peso_inicial_pct": 0.70},
        {"nombre": "Remo agarre prono polea unilateral",                "nivel_min": 1, "peso_inicial_pct": 0.20},
        {"nombre": "Remo agarre neutro polea unilateral",               "nivel_min": 1, "peso_inicial_pct": 0.20},
        {"nombre": "Remo agarre supino polea unilateral",               "nivel_min": 1, "peso_inicial_pct": 0.20},
        {"nombre": "Remo agarre prono máquina unilateral",              "nivel_min": 1, "peso_inicial_pct": 0.18},
        {"nombre": "Remo agarre neutro máquina unilateral",             "nivel_min": 1, "peso_inicial_pct": 0.18},
        {"nombre": "Remo agarre supino máquina unilateral",             "nivel_min": 1, "peso_inicial_pct": 0.18},
        {"nombre": "Remo agarre neutro mancuerna unilateral",           "nivel_min": 1, "peso_inicial_pct": 0.18},
        {"nombre": "Remo agarre prono barra",                           "nivel_min": 2, "peso_inicial_pct": 0.40},
        {"nombre": "Remo agarre supino barra",                          "nivel_min": 2, "peso_inicial_pct": 0.40},
        {"nombre": "Pull over agarre neutro",                           "nivel_min": 1, "peso_inicial_pct": 0.14},
        {"nombre": "Pull over agarre prono",                            "nivel_min": 1, "peso_inicial_pct": 0.14},
        {"nombre": "Dominadas agarre prono",                            "nivel_min": 2, "peso_inicial_pct": 0.00},
        {"nombre": "Dominadas agarre neutro",                           "nivel_min": 2, "peso_inicial_pct": 0.00},
        {"nombre": "Dominadas agarre supino",                           "nivel_min": 2, "peso_inicial_pct": 0.00},
        {"nombre": "Dominadas australianas",                            "nivel_min": 1, "peso_inicial_pct": 0.00},
    ],

    # --------------------------------------------------
    # HOMBROS (press)
    # --------------------------------------------------
    "hombros": [
        {"nombre": "Press militar mancuerna agarre prono",              "nivel_min": 1, "peso_inicial_pct": 0.10},
        {"nombre": "Press militar mancuerna agarre neutro",             "nivel_min": 1, "peso_inicial_pct": 0.10},
        {"nombre": "Press militar barra agarre prono",                  "nivel_min": 2, "peso_inicial_pct": 0.30},
        {"nombre": "Press militar máquina agarre prono",                "nivel_min": 1, "peso_inicial_pct": 0.22},
        {"nombre": "Press militar máquina agarre neutro",               "nivel_min": 1, "peso_inicial_pct": 0.22},
        {"nombre": "Press militar polea agarre prono",                  "nivel_min": 1, "peso_inicial_pct": 0.12},
        {"nombre": "Press militar polea agarre neutro",                 "nivel_min": 1, "peso_inicial_pct": 0.12},
        {"nombre": "Press Arnold mancuerna",                            "nivel_min": 2, "peso_inicial_pct": 0.10},
    ],

    # --------------------------------------------------
    # DELTOIDES ANTERIOR
    # --------------------------------------------------
    "deltoides_anterior": [
        {"nombre": "Elevación frontal disco",                           "nivel_min": 1, "peso_inicial_pct": 0.06},
        {"nombre": "Elevación frontal mancuerna agarre prono",          "nivel_min": 1, "peso_inicial_pct": 0.05},
        {"nombre": "Elevación frontal mancuerna agarre neutro",         "nivel_min": 1, "peso_inicial_pct": 0.05},
        {"nombre": "Elevación frontal polea agarre prono",              "nivel_min": 1, "peso_inicial_pct": 0.06},
        {"nombre": "Elevación frontal polea agarre neutro",             "nivel_min": 1, "peso_inicial_pct": 0.06},
        {"nombre": "Elevación frontal barra agarre prono",              "nivel_min": 1, "peso_inicial_pct": 0.10},
        {"nombre": "Elevación frontal tumbado polea agarre prono",      "nivel_min": 1, "peso_inicial_pct": 0.05},
        {"nombre": "Elevación frontal tumbado polea agarre neutro",     "nivel_min": 1, "peso_inicial_pct": 0.05},
    ],

    # --------------------------------------------------
    # DELTOIDES MEDIO
    # --------------------------------------------------
    "deltoides_medio": [
        {"nombre": "Elevación lateral mancuerna agarre neutro",                     "nivel_min": 1, "peso_inicial_pct": 0.05},
        {"nombre": "Elevación lateral mancuerna neutro cuerpo inclinado",           "nivel_min": 1, "peso_inicial_pct": 0.04},
        {"nombre": "Elevación lateral polea agarre neutro",                         "nivel_min": 1, "peso_inicial_pct": 0.06},
        {"nombre": "Elevación lateral polea agarre neutro cuerpo inclinado",        "nivel_min": 1, "peso_inicial_pct": 0.05},
        {"nombre": "Elevación lateral máquina",                                     "nivel_min": 1, "peso_inicial_pct": 0.08},
        {"nombre": "Elevación lateral mancuerna hasta arriba",                      "nivel_min": 1, "peso_inicial_pct": 0.04},
        {"nombre": "Elevación lateral polea por detrás",                            "nivel_min": 1, "peso_inicial_pct": 0.05},
        {"nombre": "Elevación lateral mancuerna de lado banco inclinado",           "nivel_min": 1, "peso_inicial_pct": 0.04},
    ],

    # --------------------------------------------------
    # DELTOIDES POSTERIOR
    # --------------------------------------------------
    "deltoides_posterior": [
        {"nombre": "Pájaros mancuerna agarre prono",                    "nivel_min": 1, "peso_inicial_pct": 0.05},
        {"nombre": "Pájaros mancuerna agarre neutro",                   "nivel_min": 1, "peso_inicial_pct": 0.05},
        {"nombre": "Pájaros polea agarre prono",                        "nivel_min": 1, "peso_inicial_pct": 0.06},
        {"nombre": "Pájaros polea agarre neutro",                       "nivel_min": 1, "peso_inicial_pct": 0.06},
        {"nombre": "Face pull",                                         "nivel_min": 1, "peso_inicial_pct": 0.10},
        {"nombre": "Pájaros máquina",                                   "nivel_min": 1, "peso_inicial_pct": 0.08},
    ],

    # --------------------------------------------------
    # GLÚTEO
    # --------------------------------------------------
    "gluteos": [
        {"nombre": "Hip thrust con barra",                              "nivel_min": 1, "peso_inicial_pct": 0.70},
        {"nombre": "Hip thrust mancuerna",                              "nivel_min": 1, "peso_inicial_pct": 0.20},
        {"nombre": "Hip thrust máquina",                                "nivel_min": 1, "peso_inicial_pct": 0.55},
        {"nombre": "Sentadilla barra espalda",                          "nivel_min": 2, "peso_inicial_pct": 0.65},
        {"nombre": "Sentadilla unilateral",                             "nivel_min": 2, "peso_inicial_pct": 0.00},
        {"nombre": "Peso muerto sumo",                                  "nivel_min": 2, "peso_inicial_pct": 0.60},
        {"nombre": "Zancadas hacia detrás",                             "nivel_min": 1, "peso_inicial_pct": 0.14},
        {"nombre": "Zancada cruzada hacia detrás",                      "nivel_min": 2, "peso_inicial_pct": 0.10},
        {"nombre": "Búlgara zancada glúteo",                            "nivel_min": 2, "peso_inicial_pct": 0.12},
        {"nombre": "Step up glúteo",                                    "nivel_min": 1, "peso_inicial_pct": 0.10},
        {"nombre": "Patada de glúteo en polea",                         "nivel_min": 1, "peso_inicial_pct": 0.08},
        {"nombre": "Abducción en máquina",                              "nivel_min": 1, "peso_inicial_pct": 0.30},
        {"nombre": "Abducción con banda",                               "nivel_min": 1, "peso_inicial_pct": 0.00},
        {"nombre": "Cuadrupedia patada glúteo con banda",               "nivel_min": 1, "peso_inicial_pct": 0.00},
        {"nombre": "Puente Fitball pies contrapuestos",                 "nivel_min": 1, "peso_inicial_pct": 0.00},
        {"nombre": "Máquina contractora glúteo",                        "nivel_min": 1, "peso_inicial_pct": 0.25},
    ],

    # --------------------------------------------------
    # CUÁDRICEPS
    # --------------------------------------------------
    "cuadriceps": [
        {"nombre": "Sentadilla frontal barra",                          "nivel_min": 2, "peso_inicial_pct": 0.55},
        {"nombre": "Sentadilla talones levantados",                     "nivel_min": 1, "peso_inicial_pct": 0.40},
        {"nombre": "Sentadilla goblet",                                 "nivel_min": 1, "peso_inicial_pct": 0.20},
        {"nombre": "Sentadilla isométrica",                             "nivel_min": 1, "peso_inicial_pct": 0.00},
        {"nombre": "Prensa inclinada pies bajos",                       "nivel_min": 1, "peso_inicial_pct": 0.90},
        {"nombre": "Hack squat",                                        "nivel_min": 2, "peso_inicial_pct": 0.70},
        {"nombre": "Zancada búlgara cuádriceps",                        "nivel_min": 2, "peso_inicial_pct": 0.12},
        {"nombre": "Zancadas paso corto",                               "nivel_min": 1, "peso_inicial_pct": 0.10},
        {"nombre": "Zancadas paso hacia delante",                       "nivel_min": 1, "peso_inicial_pct": 0.10},
        {"nombre": "Extensión de cuádriceps en máquina",                "nivel_min": 1, "peso_inicial_pct": 0.32},
        {"nombre": "Sissy squat",                                       "nivel_min": 2, "peso_inicial_pct": 0.00},
        {"nombre": "Step-up cuádriceps",                                "nivel_min": 1, "peso_inicial_pct": 0.10},
    ],

    # --------------------------------------------------
    # FEMORAL
    # --------------------------------------------------
    "femoral": [
        {"nombre": "Peso muerto rumano",                                "nivel_min": 2, "peso_inicial_pct": 0.55},
        {"nombre": "Curl femoral tumbado",                              "nivel_min": 1, "peso_inicial_pct": 0.28},
        {"nombre": "Curl femoral sentado",                              "nivel_min": 1, "peso_inicial_pct": 0.28},
        {"nombre": "Curl femoral unilateral",                           "nivel_min": 1, "peso_inicial_pct": 0.14},
        {"nombre": "Nordic curl",                                       "nivel_min": 3, "peso_inicial_pct": 0.00},
        {"nombre": "Elevación cadera Fitball",                          "nivel_min": 1, "peso_inicial_pct": 0.00},
    ],

    # --------------------------------------------------
    # ABS
    # --------------------------------------------------
    "abs": [
        {"nombre": "Crunch Fitball",                                    "nivel_min": 1, "peso_inicial_pct": 0.00},
        {"nombre": "Plancha isométrica",                                "nivel_min": 1, "peso_inicial_pct": 0.00},
        {"nombre": "Plancha isométrica Fitball",                        "nivel_min": 2, "peso_inicial_pct": 0.00},
        {"nombre": "Plancha lateral isométrica",                        "nivel_min": 1, "peso_inicial_pct": 0.00},
        {"nombre": "Dragon flag adaptación",                            "nivel_min": 3, "peso_inicial_pct": 0.00},
        {"nombre": "Elevación de piernas",                              "nivel_min": 2, "peso_inicial_pct": 0.00},
    ],

    # --------------------------------------------------
    # BÍCEPS
    # --------------------------------------------------
    "biceps": [
        {"nombre": "Curl bíceps mancuerna prono",                       "nivel_min": 1, "peso_inicial_pct": 0.08},
        {"nombre": "Curl bíceps mancuerna supino",                      "nivel_min": 1, "peso_inicial_pct": 0.09},
        {"nombre": "Curl bíceps barra prono",                           "nivel_min": 1, "peso_inicial_pct": 0.14},
        {"nombre": "Curl bíceps barra supino",                          "nivel_min": 1, "peso_inicial_pct": 0.16},
        {"nombre": "Bíceps martillo mancuerna",                         "nivel_min": 1, "peso_inicial_pct": 0.10},
        {"nombre": "Bíceps martillo máquina",                           "nivel_min": 1, "peso_inicial_pct": 0.12},
        {"nombre": "Curl bíceps máquina",                               "nivel_min": 1, "peso_inicial_pct": 0.12},
        {"nombre": "Curl bíceps banco inclinado mancuerna supino",      "nivel_min": 1, "peso_inicial_pct": 0.08},
        {"nombre": "Curl bíceps banco declinado mancuerna supino",      "nivel_min": 2, "peso_inicial_pct": 0.08},
    ],

    # --------------------------------------------------
    # TRÍCEPS
    # --------------------------------------------------
    "triceps": [
        {"nombre": "Tríceps cuerda polea",                              "nivel_min": 1, "peso_inicial_pct": 0.18},
        {"nombre": "Tríceps prono polea",                               "nivel_min": 1, "peso_inicial_pct": 0.16},
        {"nombre": "Tríceps supino polea",                              "nivel_min": 1, "peso_inicial_pct": 0.16},
        {"nombre": "Skull crushers mancuerna",                          "nivel_min": 2, "peso_inicial_pct": 0.10},
        {"nombre": "Skull crushers barra",                              "nivel_min": 2, "peso_inicial_pct": 0.18},
        {"nombre": "Press francés barra",                               "nivel_min": 2, "peso_inicial_pct": 0.20},
        {"nombre": "Press francés mancuerna",                           "nivel_min": 1, "peso_inicial_pct": 0.10},
        {"nombre": "Tríceps cruzado polea",                             "nivel_min": 1, "peso_inicial_pct": 0.14},
        {"nombre": "Fondos paralelas tríceps",                          "nivel_min": 2, "peso_inicial_pct": 0.00},
    ],
}

# Alias para compatibilidad con código anterior
EJERCICIOS["piernas"]  = EJERCICIOS["cuadriceps"]
EJERCICIOS["hombro"]   = EJERCICIOS["hombros"]


# =====================================================
# TÉCNICAS AVANZADAS (solo nivel 3)
# =====================================================
TECNICAS_AVANZADAS = {
    "drop_set": {
        "nombre":      "Drop Set",
        "descripcion": "Al fallar, reduce el peso un 20% y continúa hasta fallar de nuevo. Sin descanso.",
        "abreviatura": "DS"
    },
    "rest_pause": {
        "nombre":      "Rest-Pause",
        "descripcion": "Al fallar, descansa 15 segundos y continúa. Repite 2–3 veces.",
        "abreviatura": "RP"
    },
    "series_descendentes": {
        "nombre":      "Series Descendentes",
        "descripcion": "Haz la serie principal, descansa 10s, reduce 10% y haz otra serie.",
        "abreviatura": "SD"
    }
}


# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def calcular_peso_inicial(peso_usuario, porcentaje):
    if porcentaje == 0:
        return None
    peso_raw = peso_usuario * porcentaje
    return max(round(peso_raw / 2.5) * 2.5, 2.5)


def _elegir_ejercicios(grupo, nivel, peso_usuario, cantidad, usados=None):
    """
    Selecciona 'cantidad' ejercicios del grupo indicado,
    filtrando por nivel y evitando repetir los ya usados.
    Rota aleatoriamente para dar variedad entre sesiones.
    """
    if usados is None:
        usados = set()

    disponibles = [
        e for e in EJERCICIOS.get(grupo, [])
        if e["nivel_min"] <= nivel and e["nombre"] not in usados
    ]

    # Si no hay suficientes sin usar, permitir repetición
    if len(disponibles) < cantidad:
        disponibles = [e for e in EJERCICIOS.get(grupo, []) if e["nivel_min"] <= nivel]

    elegidos = random.sample(disponibles, min(cantidad, len(disponibles)))

    resultado = []
    for e in elegidos:
        resultado.append({
            "grupo":         grupo,
            "nombre":        e["nombre"],
            "peso_sugerido": calcular_peso_inicial(peso_usuario, e["peso_inicial_pct"]),
            "tecnica":       None
        })
        usados.add(e["nombre"])

    return resultado, usados


def _construir_dia(nombre_dia, enfoque, spec, nivel, peso_usuario, usados_global):
    """
    Construye un día de entrenamiento según la especificación.

    spec → lista de tuplas (grupo, cantidad)
           Ejemplo: [("pecho", 2), ("espalda", 2), ("deltoides_medio", 1)]
    """
    ejercicios = []
    for grupo, cantidad in spec:
        nuevos, usados_global = _elegir_ejercicios(
            grupo, nivel, peso_usuario, cantidad, usados_global
        )
        ejercicios.extend(nuevos)

    return {
        "dia":        nombre_dia,
        "enfoque":    enfoque,
        "ejercicios": ejercicios
    }, usados_global


def _aplicar_parametros(dias_rutina, series, reps_min, reps_max, nivel):
    """Añade series, reps y técnicas avanzadas a cada ejercicio."""
    import random as _random
    tecnicas = list(TECNICAS_AVANZADAS.values())

    for dia in dias_rutina:
        grupos_vistos = {}
        for ejercicio in dia["ejercicios"]:
            ejercicio["series"]   = series
            ejercicio["reps_min"] = reps_min
            ejercicio["reps_max"] = reps_max
            ejercicio["tecnica"]  = None

            grupo = ejercicio["grupo"]
            grupos_vistos[grupo] = grupos_vistos.get(grupo, 0) + 1

        # Técnicas avanzadas: último ejercicio de cada grupo para nivel 3
        if nivel == 3:
            grupos_contados = {}
            for ejercicio in dia["ejercicios"]:
                grupo = ejercicio["grupo"]
                grupos_contados[grupo] = grupos_contados.get(grupo, 0) + 1

            contador_actual = {}
            for ejercicio in dia["ejercicios"]:
                grupo = ejercicio["grupo"]
                contador_actual[grupo] = contador_actual.get(grupo, 0) + 1
                if contador_actual[grupo] == grupos_contados[grupo]:
                    ejercicio["tecnica"] = _random.choice(tecnicas)


# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def generar_rutina(perfil):
    """
    Genera una rutina completa personalizada según:
    - Género (Hombre / Mujer / Prefiero no decirlo)
    - Objetivo (músculo / grasa / fuerza / condición)
    - Días disponibles (1–6)
    - Nivel (1=principiante, 2=intermedio, 3=avanzado)
    - Músculos prioritarios
    """

    nivel        = perfil["nivel_num"]
    dias         = perfil["dias"]
    peso         = perfil["peso"]
    objetivo     = perfil["objetivo"].lower()
    genero       = perfil.get("genero", "Prefiero no decirlo")
    prioritarios = perfil.get("musculos_prioritarios", [])

    # --------------------------------------------------
    # Parámetros según objetivo
    # --------------------------------------------------
    if "músculo" in objetivo or "hipertrofia" in objetivo:
        series = 4; reps_min = 8;  reps_max = 12; descanso = 90
    elif "grasa" in objetivo:
        series = 3; reps_min = 12; reps_max = 15; descanso = 60
    elif "fuerza" in objetivo:
        series = 5; reps_min = 4;  reps_max = 6;  descanso = 180
    else:
        series = 3; reps_min = 10; reps_max = 15; descanso = 75

    if nivel == 1:
        series = 3; reps_min = 10; reps_max = 12

    # --------------------------------------------------
    # Determinar si es perfil "chica" o "chico"
    # Para "Prefiero no decirlo" usamos la lógica de chico
    # salvo que tenga prioritarios de tren inferior
    # --------------------------------------------------
    es_mujer = (genero == "Mujer")
    tiene_foco_inferior = any(g in prioritarios for g in ["gluteos", "piernas", "cuadriceps", "femoral"])

    if genero == "Prefiero no decirlo" and tiene_foco_inferior:
        es_mujer = True

    # --------------------------------------------------
    # Función interna para foco de glúteo:
    # si glúteos está en prioritarios, pone más glúteo que cuádriceps
    # --------------------------------------------------
    def spec_pierna_con_foco(base_gluteo, base_cuad, base_femoral, abs_count=1):
        if "gluteos" in prioritarios:
            return [
                ("gluteos",    base_gluteo + 1),
                ("cuadriceps", max(base_cuad - 1, 1)),
                ("femoral",    base_femoral),
                ("abs",        abs_count)
            ]
        elif "cuadriceps" in prioritarios:
            return [
                ("gluteos",    max(base_gluteo - 1, 1)),
                ("cuadriceps", base_cuad + 1),
                ("femoral",    base_femoral),
                ("abs",        abs_count)
            ]
        else:
            return [
                ("gluteos",    base_gluteo),
                ("cuadriceps", base_cuad),
                ("femoral",    base_femoral),
                ("abs",        abs_count)
            ]

    def spec_brazo(tri_count=1, bi_count=1):
        """Devuelve spec de brazo según prioritarios."""
        if "triceps" in prioritarios:
            return [("triceps", tri_count + 1), ("biceps", bi_count)]
        elif "biceps" in prioritarios:
            return [("triceps", tri_count), ("biceps", bi_count + 1)]
        else:
            return [("triceps", tri_count), ("biceps", bi_count)]

    # --------------------------------------------------
    # Usados globales para rotar ejercicios
    # --------------------------------------------------
    usados = set()
    dias_rutina = []

    # ══════════════════════════════════════════════════
    # 1 DÍA — FULLBODY (igual para todos)
    # ══════════════════════════════════════════════════
    if dias == 1:
        estructura = "fullbody_1dia"
        spec = [
            ("pecho", 1), ("espalda", 1), ("deltoides_medio", 1),
            ("gluteos", 1), ("cuadriceps", 1), ("femoral", 1),
            ("abs", 1), ("biceps", 1), ("triceps", 1)
        ]
        dia, usados = _construir_dia("Día 1", "Full Body", spec, nivel, peso, usados)
        dias_rutina.append(dia)

    # ══════════════════════════════════════════════════
    # 2 DÍAS — Tren Superior / Tren Inferior
    # ══════════════════════════════════════════════════
    elif dias == 2:
        estructura = "superior_inferior"

        spec_sup = [
            ("pecho", 2), ("espalda", 2), ("deltoides_medio", 1),
            *spec_brazo(1, 1)
        ]
        spec_inf = spec_pierna_con_foco(2, 2, 2, 1)

        dia1, usados = _construir_dia("Lunes",   "Tren Superior", spec_sup, nivel, peso, usados)
        dia2, usados = _construir_dia("Jueves",  "Tren Inferior", spec_inf, nivel, peso, usados)
        dias_rutina = [dia1, dia2]

    # ══════════════════════════════════════════════════
    # 3 DÍAS
    # ══════════════════════════════════════════════════
    elif dias == 3:
        if es_mujer or "grasa" in objetivo:
            # Chica o pérdida de grasa:
            # Día 1 Superior, Día 2 Inferior, Día 3 Fullbody
            estructura = "superior_inferior_fullbody"

            spec_sup = [
                ("pecho", 2), ("espalda", 2), ("deltoides_medio", 1),
                *spec_brazo(1, 1)
            ]
            spec_inf = spec_pierna_con_foco(2, 2, 2, 1)
            spec_fb  = [
                ("pecho", 1), ("espalda", 1), ("deltoides_medio", 1),
                ("gluteos", 1), ("cuadriceps", 1), ("femoral", 1),
                ("abs", 1), ("biceps", 1), ("triceps", 1)
            ]

            usados2 = set()
            dia1, usados  = _construir_dia("Lunes",    "Tren Superior",  spec_sup, nivel, peso, usados)
            dia2, usados  = _construir_dia("Miércoles","Tren Inferior",  spec_inf, nivel, peso, usados)
            dia3, usados2 = _construir_dia("Viernes",  "Full Body",      spec_fb,  nivel, peso, usados2)
            dias_rutina = [dia1, dia2, dia3]

        else:
            # Chico o ganancia muscular:
            # Empuje / Tirón / Pierna
            estructura = "empuje_tiron_pierna"

            spec_emp = [("pecho", 3), ("deltoides_medio", 2), *spec_brazo(2, 0)]
            spec_tir = [("espalda", 3), ("deltoides_posterior", 2), *spec_brazo(0, 2)]
            spec_pie = spec_pierna_con_foco(2, 2, 1, 1)

            dia1, usados = _construir_dia("Lunes",    "Empuje (Pecho, Hombro, Tríceps)", spec_emp, nivel, peso, usados)
            dia2, usados = _construir_dia("Miércoles","Tirón (Espalda, Bíceps)",          spec_tir, nivel, peso, usados)
            dia3, usados = _construir_dia("Viernes",  "Pierna",                           spec_pie, nivel, peso, usados)
            dias_rutina = [dia1, dia2, dia3]

    # ══════════════════════════════════════════════════
    # 4 DÍAS
    # ══════════════════════════════════════════════════
    elif dias == 4:
        if es_mujer and "músculo" in objetivo:
            # Chica aumento masa:
            # Cuád+Glút / Superior Espalda / Femoral+Glút / Superior Hombro
            estructura = "4dias_chica_masa"

            spec_d1 = spec_pierna_con_foco(3, 2, 0, 1)
            spec_d2 = [
                ("espalda", 2), ("pecho", 1),
                ("deltoides_posterior", 2), *spec_brazo(1, 0)
            ]
            spec_d3 = [
                ("gluteos", 3 if "gluteos" in prioritarios else 2),
                ("femoral",  2 if "gluteos" not in prioritarios else 2),
                ("abs", 1)
            ]
            spec_d4 = [
                ("hombros", 1), ("deltoides_medio", 2), ("deltoides_posterior", 1),
                *spec_brazo(1, 1)
            ]

            usados_b = set()
            dia1, usados   = _construir_dia("Lunes",    "Cuádriceps y Glúteo",       spec_d1, nivel, peso, usados)
            dia2, usados   = _construir_dia("Martes",   "Tren Superior — Espalda",   spec_d2, nivel, peso, usados)
            dia3, usados_b = _construir_dia("Jueves",   "Femoral y Glúteo",          spec_d3, nivel, peso, usados_b)
            dia4, usados_b = _construir_dia("Viernes",  "Tren Superior — Hombro",    spec_d4, nivel, peso, usados_b)
            dias_rutina = [dia1, dia2, dia3, dia4]

        elif "grasa" in objetivo:
            # 4 días pérdida de grasa: 2 sup + 2 inf (variados)
            estructura = "4dias_grasa"

            spec_sup1 = [("pecho", 2), ("espalda", 2), ("deltoides_medio", 1), *spec_brazo(1, 1)]
            spec_inf1 = spec_pierna_con_foco(2, 2, 2, 1)
            usados2 = set()
            spec_sup2 = [("pecho", 2), ("espalda", 2), ("deltoides_medio", 1), *spec_brazo(1, 1)]
            spec_inf2 = spec_pierna_con_foco(2, 2, 2, 1)

            dia1, usados  = _construir_dia("Lunes",    "Tren Superior A",  spec_sup1, nivel, peso, usados)
            dia2, usados  = _construir_dia("Martes",   "Tren Inferior A",  spec_inf1, nivel, peso, usados)
            dia3, usados2 = _construir_dia("Jueves",   "Tren Superior B",  spec_sup2, nivel, peso, usados2)
            dia4, usados2 = _construir_dia("Viernes",  "Tren Inferior B",  spec_inf2, nivel, peso, usados2)
            dias_rutina = [dia1, dia2, dia3, dia4]

        else:
            # Chico aumento masa: Empuje / Tirón / Pierna / Hombro+Brazo
            estructura = "4dias_chico_masa"

            spec_emp = [("pecho", 3), ("deltoides_medio", 2), *spec_brazo(2, 0)]
            spec_tir = [("espalda", 3), ("deltoides_posterior", 2), *spec_brazo(0, 2)]
            spec_pie = spec_pierna_con_foco(2, 2, 1, 1)
            spec_hom = [
                ("hombros", 1), ("deltoides_medio", 2),
                ("deltoides_posterior", 1), *spec_brazo(1, 1)
            ]

            dia1, usados = _construir_dia("Lunes",   "Empuje (Pecho, Hombro, Tríceps)",     spec_emp, nivel, peso, usados)
            dia2, usados = _construir_dia("Martes",  "Tirón (Espalda, Bíceps)",              spec_tir, nivel, peso, usados)
            dia3, usados = _construir_dia("Jueves",  "Pierna",                               spec_pie, nivel, peso, usados)
            dia4, usados = _construir_dia("Viernes", "Hombro y Brazo",                       spec_hom, nivel, peso, usados)
            dias_rutina = [dia1, dia2, dia3, dia4]

    # ══════════════════════════════════════════════════
    # 5 DÍAS
    # ══════════════════════════════════════════════════
    elif dias == 5:
        if es_mujer and "músculo" in objetivo:
            # Chica masa: Cuád+Glút / Superior Esp / Fem+Glút / Superior Hom / Pierna entera
            estructura = "5dias_chica_masa"

            spec_d1 = spec_pierna_con_foco(3, 2, 0, 1)
            spec_d2 = [("espalda", 2), ("pecho", 1), ("deltoides_posterior", 2), *spec_brazo(1, 0)]
            spec_d3 = [("gluteos", 3), ("femoral", 2), ("abs", 1)]
            spec_d4 = [("hombros", 1), ("deltoides_medio", 2), ("deltoides_posterior", 1), *spec_brazo(1, 1)]
            spec_d5 = [("cuadriceps", 2), ("femoral", 2), ("gluteos", 1), ("abs", 1)]

            usados_b = set()
            dia1, usados   = _construir_dia("Lunes",    "Cuádriceps y Glúteo",     spec_d1, nivel, peso, usados)
            dia2, usados   = _construir_dia("Martes",   "Superior — Espalda",      spec_d2, nivel, peso, usados)
            dia3, usados_b = _construir_dia("Miércoles","Femoral y Glúteo",         spec_d3, nivel, peso, usados_b)
            dia4, usados_b = _construir_dia("Jueves",   "Superior — Hombro",       spec_d4, nivel, peso, usados_b)
            dia5, usados_b = _construir_dia("Viernes",  "Pierna Completa",         spec_d5, nivel, peso, usados_b)
            dias_rutina = [dia1, dia2, dia3, dia4, dia5]

        elif "grasa" in objetivo:
            # 5 días grasa: 2 sup + 2 inf + 1 fullbody
            estructura = "5dias_grasa"

            spec_sup1 = [("pecho", 2), ("espalda", 2), ("deltoides_medio", 1), *spec_brazo(1, 1)]
            spec_inf1 = spec_pierna_con_foco(2, 2, 2, 1)
            usados_b  = set()
            spec_sup2 = [("pecho", 2), ("espalda", 2), ("deltoides_medio", 1), *spec_brazo(1, 1)]
            spec_inf2 = spec_pierna_con_foco(2, 2, 2, 1)
            spec_fb   = [
                ("pecho", 1), ("espalda", 1), ("deltoides_medio", 1),
                ("gluteos", 1), ("cuadriceps", 1), ("femoral", 1),
                ("abs", 1), ("biceps", 1), ("triceps", 1)
            ]

            dia1, usados   = _construir_dia("Lunes",    "Tren Superior A",   spec_sup1, nivel, peso, usados)
            dia2, usados   = _construir_dia("Martes",   "Tren Inferior A",   spec_inf1, nivel, peso, usados)
            dia3, usados_b = _construir_dia("Miércoles","Tren Superior B",   spec_sup2, nivel, peso, usados_b)
            dia4, usados_b = _construir_dia("Jueves",   "Tren Inferior B",   spec_inf2, nivel, peso, usados_b)
            dia5, _        = _construir_dia("Viernes",  "Full Body",         spec_fb,   nivel, peso, set())
            dias_rutina = [dia1, dia2, dia3, dia4, dia5]

        else:
            # Chico masa: Emp1 / Tir1 / Pierna / Emp2 / Tir2 (diferente al 1 y 2)
            estructura = "5dias_chico_masa"

            spec_emp1 = [("pecho", 3), ("deltoides_medio", 2), *spec_brazo(2, 0)]
            spec_tir1 = [("espalda", 3), ("deltoides_posterior", 2), *spec_brazo(0, 2)]
            spec_pie  = spec_pierna_con_foco(2, 2, 1, 1)
            usados_b  = set()
            spec_emp2 = [("pecho", 3), ("deltoides_medio", 2), *spec_brazo(2, 0)]
            spec_tir2 = [("espalda", 3), ("deltoides_posterior", 2), *spec_brazo(0, 2)]

            dia1, usados   = _construir_dia("Lunes",    "Empuje 1 (Pecho, Hombro, Tríceps)", spec_emp1, nivel, peso, usados)
            dia2, usados   = _construir_dia("Martes",   "Tirón 1 (Espalda, Bíceps)",          spec_tir1, nivel, peso, usados)
            dia3, usados   = _construir_dia("Miércoles","Pierna",                              spec_pie,  nivel, peso, usados)
            dia4, usados_b = _construir_dia("Jueves",   "Empuje 2 (Pecho, Hombro, Tríceps)", spec_emp2, nivel, peso, usados_b)
            dia5, usados_b = _construir_dia("Viernes",  "Tirón 2 (Espalda, Bíceps)",          spec_tir2, nivel, peso, usados_b)
            dias_rutina = [dia1, dia2, dia3, dia4, dia5]

    # ══════════════════════════════════════════════════
    # 6 DÍAS
    # ══════════════════════════════════════════════════
    else:  # dias == 6
        if es_mujer and "músculo" in objetivo:
            # Chica masa 6 días
            estructura = "6dias_chica_masa"

            spec_d1 = spec_pierna_con_foco(3, 2, 0, 1)
            spec_d2 = [("espalda", 2), ("pecho", 1), ("deltoides_posterior", 2), *spec_brazo(1, 0)]
            spec_d3 = [("gluteos", 3), ("femoral", 2), ("abs", 1)]
            spec_d4 = [("hombros", 1), ("deltoides_medio", 2), ("deltoides_posterior", 1), *spec_brazo(1, 1)]
            spec_d5 = [("cuadriceps", 2), ("femoral", 2), ("gluteos", 1), ("abs", 1)]
            spec_d6 = [("pecho", 2), ("espalda", 2), ("deltoides_medio", 1), *spec_brazo(1, 1)]

            usados_b = set()
            dia1, usados   = _construir_dia("Lunes",    "Cuádriceps y Glúteo",    spec_d1, nivel, peso, usados)
            dia2, usados   = _construir_dia("Martes",   "Superior — Espalda",     spec_d2, nivel, peso, usados)
            dia3, usados_b = _construir_dia("Miércoles","Femoral y Glúteo",        spec_d3, nivel, peso, usados_b)
            dia4, usados_b = _construir_dia("Jueves",   "Superior — Hombro",      spec_d4, nivel, peso, usados_b)
            dia5, usados_b = _construir_dia("Viernes",  "Pierna Completa",        spec_d5, nivel, peso, usados_b)
            dia6, _        = _construir_dia("Sábado",   "Tren Superior Completo", spec_d6, nivel, peso, set())
            dias_rutina = [dia1, dia2, dia3, dia4, dia5, dia6]

        elif "grasa" in objetivo:
            # 6 días grasa: sup+inf+fb x2
            estructura = "6dias_grasa"

            spec_sup1 = [("pecho", 2), ("espalda", 2), ("deltoides_medio", 1), *spec_brazo(1, 1)]
            spec_inf1 = spec_pierna_con_foco(2, 2, 2, 1)
            spec_fb1  = [("pecho",1),("espalda",1),("deltoides_medio",1),("gluteos",1),
                         ("cuadriceps",1),("femoral",1),("abs",1),("biceps",1),("triceps",1)]
            usados_b  = set()
            spec_sup2 = [("pecho", 2), ("espalda", 2), ("deltoides_medio", 1), *spec_brazo(1, 1)]
            spec_inf2 = spec_pierna_con_foco(2, 2, 2, 1)
            spec_fb2  = [("pecho",1),("espalda",1),("deltoides_medio",1),("gluteos",1),
                         ("cuadriceps",1),("femoral",1),("abs",1),("biceps",1),("triceps",1)]

            dia1, usados   = _construir_dia("Lunes",    "Tren Superior A",  spec_sup1, nivel, peso, usados)
            dia2, usados   = _construir_dia("Martes",   "Tren Inferior A",  spec_inf1, nivel, peso, usados)
            dia3, _        = _construir_dia("Miércoles","Full Body A",       spec_fb1,  nivel, peso, set())
            dia4, usados_b = _construir_dia("Jueves",   "Tren Superior B",  spec_sup2, nivel, peso, usados_b)
            dia5, usados_b = _construir_dia("Viernes",  "Tren Inferior B",  spec_inf2, nivel, peso, usados_b)
            dia6, _        = _construir_dia("Sábado",   "Full Body B",      spec_fb2,  nivel, peso, set())
            dias_rutina = [dia1, dia2, dia3, dia4, dia5, dia6]

        else:
            # Chico masa 6 días: Emp1/Tir1/Pier1/Emp2/Tir2/Pier2
            estructura = "6dias_chico_masa"

            spec_emp1 = [("pecho", 3), ("deltoides_medio", 2), *spec_brazo(2, 0)]
            spec_tir1 = [("espalda", 3), ("deltoides_posterior", 2), *spec_brazo(0, 2)]
            spec_pie1 = spec_pierna_con_foco(2, 2, 1, 1)
            usados_b  = set()
            spec_emp2 = [("pecho", 3), ("deltoides_medio", 2), *spec_brazo(2, 0)]
            spec_tir2 = [("espalda", 3), ("deltoides_posterior", 2), *spec_brazo(0, 2)]
            spec_pie2 = [("cuadriceps", 2), ("femoral", 2), ("gluteos", 1), ("abs", 1)]

            dia1, usados   = _construir_dia("Lunes",    "Empuje 1",  spec_emp1, nivel, peso, usados)
            dia2, usados   = _construir_dia("Martes",   "Tirón 1",   spec_tir1, nivel, peso, usados)
            dia3, usados   = _construir_dia("Miércoles","Pierna 1",  spec_pie1, nivel, peso, usados)
            dia4, usados_b = _construir_dia("Jueves",   "Empuje 2",  spec_emp2, nivel, peso, usados_b)
            dia5, usados_b = _construir_dia("Viernes",  "Tirón 2",   spec_tir2, nivel, peso, usados_b)
            dia6, usados_b = _construir_dia("Sábado",   "Pierna 2",  spec_pie2, nivel, peso, usados_b)
            dias_rutina = [dia1, dia2, dia3, dia4, dia5, dia6]

    # Añadir parámetros a todos los ejercicios
    _aplicar_parametros(dias_rutina, series, reps_min, reps_max, nivel)

    return {
        "estructura":   estructura,
        "series":       series,
        "reps_min":     reps_min,
        "reps_max":     reps_max,
        "descanso_seg": descanso,
        "dias":         dias_rutina
    }
# strength_standards.py
# Estándares de fuerza basados en datos de Strength Level (strengthlevel.com)
# Los valores son el peso levantado en 1 repetición máxima (1RM) estimada
# ajustados por peso corporal del usuario.
#
# Los multiplicadores representan cuántas veces el peso corporal
# debe levantar el usuario para alcanzar cada nivel.
#
# Fuente de referencia: strengthlevel.com (datos públicos)

# =====================================================
# ESTÁNDARES POR EJERCICIO Y GÉNERO
# =====================================================
# Estructura:
# ejercicio → género → [principiante, novato, intermedio, avanzado, elite]
# Los valores son multiplicadores del peso corporal (ratio)
# Ejemplo: 0.5 significa que debes levantar el 50% de tu peso corporal

STANDARDS = {
    "Press de banca con barra": {
        "Hombre": {
            "ratios": [0.35, 0.55, 0.80, 1.10, 1.40],
        },
        "Mujer": {
            "ratios": [0.20, 0.35, 0.50, 0.70, 0.95],
        },
        "Prefiero no decirlo": {
            "ratios": [0.25, 0.45, 0.65, 0.90, 1.20],
        }
    },
    "Press de banca en máquina": {
        "Hombre": {
            "ratios": [0.40, 0.60, 0.85, 1.15, 1.45],
        },
        "Mujer": {
            "ratios": [0.25, 0.40, 0.55, 0.75, 1.00],
        },
        "Prefiero no decirlo": {
            "ratios": [0.30, 0.50, 0.70, 0.95, 1.25],
        }
    },
    "Sentadilla con barra": {
        "Hombre": {
            "ratios": [0.50, 0.75, 1.10, 1.50, 1.90],
        },
        "Mujer": {
            "ratios": [0.30, 0.50, 0.75, 1.05, 1.40],
        },
        "Prefiero no decirlo": {
            "ratios": [0.40, 0.62, 0.92, 1.27, 1.65],
        }
    },
    "Peso muerto rumano": {
        "Hombre": {
            "ratios": [0.50, 0.80, 1.15, 1.55, 2.00],
        },
        "Mujer": {
            "ratios": [0.35, 0.55, 0.80, 1.10, 1.50],
        },
        "Prefiero no decirlo": {
            "ratios": [0.42, 0.67, 0.97, 1.32, 1.75],
        }
    },
    "Press militar con barra": {
        "Hombre": {
            "ratios": [0.25, 0.40, 0.60, 0.80, 1.05],
        },
        "Mujer": {
            "ratios": [0.15, 0.25, 0.38, 0.53, 0.72],
        },
        "Prefiero no decirlo": {
            "ratios": [0.20, 0.32, 0.49, 0.66, 0.88],
        }
    },
    "Press de hombro en máquina": {
        "Hombre": {
            "ratios": [0.28, 0.45, 0.65, 0.88, 1.15],
        },
        "Mujer": {
            "ratios": [0.18, 0.28, 0.42, 0.58, 0.80],
        },
        "Prefiero no decirlo": {
            "ratios": [0.23, 0.36, 0.53, 0.73, 0.97],
        }
    },
    "Jalón al pecho en polea": {
        "Hombre": {
            "ratios": [0.40, 0.60, 0.85, 1.10, 1.40],
        },
        "Mujer": {
            "ratios": [0.25, 0.40, 0.58, 0.78, 1.02],
        },
        "Prefiero no decirlo": {
            "ratios": [0.32, 0.50, 0.71, 0.94, 1.21],
        }
    },
    "Remo en polea baja": {
        "Hombre": {
            "ratios": [0.40, 0.62, 0.88, 1.18, 1.50],
        },
        "Mujer": {
            "ratios": [0.25, 0.40, 0.60, 0.82, 1.08],
        },
        "Prefiero no decirlo": {
            "ratios": [0.32, 0.51, 0.74, 1.00, 1.29],
        }
    },
    "Remo con barra": {
        "Hombre": {
            "ratios": [0.40, 0.65, 0.92, 1.25, 1.60],
        },
        "Mujer": {
            "ratios": [0.25, 0.42, 0.62, 0.86, 1.14],
        },
        "Prefiero no decirlo": {
            "ratios": [0.32, 0.53, 0.77, 1.05, 1.37],
        }
    },
    "Hip thrust con barra": {
        "Hombre": {
            "ratios": [0.55, 0.90, 1.30, 1.75, 2.20],
        },
        "Mujer": {
            "ratios": [0.45, 0.75, 1.10, 1.50, 1.95],
        },
        "Prefiero no decirlo": {
            "ratios": [0.50, 0.82, 1.20, 1.62, 2.07],
        }
    },
    "Curl con barra recta": {
        "Hombre": {
            "ratios": [0.18, 0.30, 0.44, 0.60, 0.78],
        },
        "Mujer": {
            "ratios": [0.10, 0.18, 0.27, 0.38, 0.52],
        },
        "Prefiero no decirlo": {
            "ratios": [0.14, 0.24, 0.35, 0.49, 0.65],
        }
    },
    "Extensión de tríceps en polea": {
        "Hombre": {
            "ratios": [0.20, 0.32, 0.47, 0.64, 0.84],
        },
        "Mujer": {
            "ratios": [0.12, 0.20, 0.30, 0.42, 0.57],
        },
        "Prefiero no decirlo": {
            "ratios": [0.16, 0.26, 0.38, 0.53, 0.70],
        }
    },
    "Prensa de piernas": {
        "Hombre": {
            "ratios": [0.80, 1.30, 1.90, 2.55, 3.25],
        },
        "Mujer": {
            "ratios": [0.55, 0.90, 1.35, 1.85, 2.40],
        },
        "Prefiero no decirlo": {
            "ratios": [0.67, 1.10, 1.62, 2.20, 2.82],
        }
    },
}

NIVELES = ["Principiante", "Novato", "Intermedio", "Avanzado", "Elite"]

# Percentiles aproximados por nivel
# Qué % de la población está POR DEBAJO de cada nivel
PERCENTILES = {
    "Principiante": 20,
    "Novato":       40,
    "Intermedio":   60,
    "Avanzado":     82,
    "Elite":        97
}


def estimar_1rm(peso_kg, reps):
    """
    Estima el 1RM (peso máximo para 1 repetición) usando la fórmula de Epley.
    Es la fórmula más usada en la industria del fitness.

    peso_kg → peso usado en la serie
    reps    → repeticiones completadas

    Ejemplo: 60kg × 10 reps → 1RM estimado ≈ 80kg
    """
    if reps == 1:
        return peso_kg
    return peso_kg * (1 + reps / 30)


def calcular_nivel_fuerza(nombre_ejercicio, peso_usuario, genero, peso_levantado, reps):
    """
    Calcula el nivel de fuerza del usuario en un ejercicio específico.

    nombre_ejercicio → nombre exacto del ejercicio
    peso_usuario     → peso corporal en kg
    genero           → "Hombre", "Mujer" o "Prefiero no decirlo"
    peso_levantado   → kg usados en la serie
    reps             → repeticiones completadas

    Devuelve un diccionario con:
        nivel        → nombre del nivel (Principiante, Novato, etc.)
        nivel_idx    → índice del nivel (0–4)
        percentil    → % aproximado de personas superadas
        ratio_actual → relación peso_levantado/peso_corporal
        umbrales_kg  → pesos de referencia para cada nivel
        siguiente_nivel → info sobre el siguiente nivel
    """
    if nombre_ejercicio not in STANDARDS:
        return None

    standards = STANDARDS[nombre_ejercicio]
    genero_key = genero if genero in standards else "Prefiero no decirlo"
    ratios = standards[genero_key]["ratios"]

    # Calcular 1RM estimado
    rm1 = estimar_1rm(peso_levantado, reps)

    # Calcular el ratio actual (1RM / peso corporal)
    ratio_actual = rm1 / peso_usuario if peso_usuario > 0 else 0

    # Calcular los umbrales en kg para este usuario
    umbrales_kg = [round(r * peso_usuario, 1) for r in ratios]

    # Determinar el nivel actual
    nivel_idx = 0
    for i, umbral in enumerate(ratios):
        if ratio_actual >= umbral:
            nivel_idx = i

    nivel_actual = NIVELES[nivel_idx]
    percentil    = PERCENTILES[nivel_actual]

    # Calcular info del siguiente nivel
    siguiente_nivel = None
    if nivel_idx < len(NIVELES) - 1:
        siguiente_nivel = {
            "nombre":    NIVELES[nivel_idx + 1],
            "umbral_kg": umbrales_kg[nivel_idx + 1],
            "faltan_kg": round(umbrales_kg[nivel_idx + 1] - rm1, 1)
        }

    return {
        "ejercicio":       nombre_ejercicio,
        "nivel":           nivel_actual,
        "nivel_idx":       nivel_idx,
        "percentil":       percentil,
        "rm1_estimado":    round(rm1, 1),
        "ratio_actual":    round(ratio_actual, 2),
        "umbrales_kg":     umbrales_kg,
        "siguiente_nivel": siguiente_nivel
    }


def ejercicios_con_standard():
    """Devuelve la lista de ejercicios que tienen estándares definidos."""
    return list(STANDARDS.keys())
# bloques.py
# Este archivo contiene toda la lógica de planificación
# de bloques de entrenamiento de 6-8 semanas.

from datetime import datetime, timedelta
import json


# =====================================================
# DEFINICIÓN DE FASES
# =====================================================
# Cada bloque de 8 semanas tiene 4 fases.
# Cada fase define cuántas series hacer y el RPE objetivo.

FASES_BLOQUE = [
    {
        "nombre":      "Adaptación",
        "semanas":     [1, 2],
        "series":      3,
        "rpe_objetivo": 7,
        "descripcion": "Semanas de adaptación. Aprende los movimientos y establece tu base.",
        "color":       "blue"
    },
    {
        "nombre":      "Acumulación",
        "semanas":     [3, 4, 5],
        "series":      4,
        "rpe_objetivo": 8,
        "descripcion": "Fase principal. Máximo volumen del bloque. Aquí se construye el músculo.",
        "color":       "green"
    },
    {
        "nombre":      "Intensificación",
        "semanas":     [6, 7],
        "series":      4,
        "rpe_objetivo": 9,
        "descripcion": "Semanas de alta intensidad. Menos volumen, más peso. El cuerpo da lo máximo.",
        "color":       "orange"
    },
    {
        "nombre":      "Deload",
        "semanas":     [8],
        "series":      2,
        "rpe_objetivo": 6,
        "descripcion": "Semana de descarga. El cuerpo recupera y asimila las ganancias del bloque.",
        "color":       "blue"
    }
]


def obtener_fase_actual(semana_del_bloque):
    """
    Dado el número de semana dentro del bloque (1–8),
    devuelve la fase correspondiente.

    Ejemplo:
        semana 1 → Adaptación
        semana 3 → Acumulación
        semana 8 → Deload
    """
    for fase in FASES_BLOQUE:
        if semana_del_bloque in fase["semanas"]:
            return fase

    # Si la semana es mayor que 8, estamos en un nuevo bloque
    return FASES_BLOQUE[0]


def calcular_semana_del_bloque(fecha_inicio_bloque):
    """
    Calcula en qué semana del bloque estamos hoy.

    fecha_inicio_bloque → string con la fecha de inicio "YYYY-MM-DD"

    Devuelve un número del 1 al 8.
    Si han pasado más de 8 semanas, devuelve el número
    correspondiente dentro del bloque actual.
    """
    fecha_inicio = datetime.strptime(fecha_inicio_bloque, "%Y-%m-%d")
    hoy          = datetime.now()
    dias_pasados = (hoy - fecha_inicio).days
    semana_total = (dias_pasados // 7) + 1

    # Calcular semana dentro del bloque actual (ciclos de 8 semanas)
    semana_en_bloque = ((semana_total - 1) % 8) + 1
    numero_bloque    = ((semana_total - 1) // 8) + 1

    return {
        "semana_total":      semana_total,
        "semana_en_bloque":  semana_en_bloque,
        "numero_bloque":     numero_bloque,
        "dias_pasados":      dias_pasados
    }


def crear_bloque_inicial():
    """
    Crea la estructura inicial de un bloque de entrenamiento.
    Se llama cuando el usuario crea su perfil por primera vez.

    Devuelve un diccionario con la información del bloque.
    """
    hoy = datetime.now().strftime("%Y-%m-%d")

    return {
        "numero_bloque":   1,
        "fecha_inicio":    hoy,
        "duracion_semanas": 8,
        "completado":      False
    }


def ajustar_rutina_por_fase(rutina, fase):
    """
    Ajusta el número de series de todos los ejercicios
    según la fase actual del bloque.

    rutina → el diccionario de la rutina
    fase   → el diccionario de la fase actual

    Devuelve la rutina con las series ajustadas.
    """
    import copy
    rutina_ajustada = copy.deepcopy(rutina)

    for dia in rutina_ajustada["dias"]:
        for ejercicio in dia["ejercicios"]:
            ejercicio["series"] = fase["series"]

    # Actualizar también el valor global de series en la rutina
    rutina_ajustada["series"] = fase["series"]

    return rutina_ajustada


def generar_resumen_bloque(historial_sesiones, numero_bloque):
    """
    Genera un resumen del bloque completado.

    historial_sesiones → lista de sesiones del bloque
    numero_bloque      → número del bloque que terminó

    Devuelve un diccionario con estadísticas del bloque.
    """
    if not historial_sesiones:
        return None

    total_sesiones    = len(historial_sesiones)
    ejercicios_subidos = 0
    ejercicios_bajados = 0
    ejercicios_totales = 0

    for sesion in historial_sesiones:
        for resultado in sesion["resultados"]:
            ejercicios_totales += 1
            if resultado.get("decision") == "subir":
                ejercicios_subidos += 1
            elif resultado.get("decision") == "bajar":
                ejercicios_bajados += 1

    pct_progreso = (ejercicios_subidos / ejercicios_totales * 100) if ejercicios_totales > 0 else 0

    return {
        "numero_bloque":       numero_bloque,
        "total_sesiones":      total_sesiones,
        "ejercicios_subidos":  ejercicios_subidos,
        "ejercicios_bajados":  ejercicios_bajados,
        "pct_progreso":        pct_progreso
    }
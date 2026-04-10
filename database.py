# database.py
import os
import json
from supabase import create_client


def get_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise Exception(
            "❌ No se encontraron las variables SUPABASE_URL y SUPABASE_KEY. "
            "Configúralas en Railway → Variables."
        )
    return create_client(url, key)


# =====================================================
# FUNCIONES DE USUARIOS
# =====================================================

def guardar_usuario(perfil):
    supabase = get_supabase_client()
    datos = {
        "nombre":       perfil["nombre"],
        "edad":         perfil["edad"],
        "peso":         perfil["peso"],
        "nivel_texto":  perfil["nivel_texto"],
        "nivel_num":    perfil["nivel_num"],
        "objetivo":     perfil["objetivo"],
        "dias":         perfil["dias"],
        "minutos":      perfil["minutos"],
        "equipamiento": perfil["equipamiento"],
        "lesiones":     perfil.get("lesiones", "")
    }
    respuesta = supabase.table("usuarios").insert(datos).execute()
    return respuesta.data[0]["id"]


def buscar_usuario_por_nombre(nombre):
    supabase = get_supabase_client()
    respuesta = (
        supabase.table("usuarios")
        .select("*")
        .eq("nombre", nombre)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if respuesta.data:
        return respuesta.data[0]
    return None


# =====================================================
# FUNCIONES DE RUTINAS
# =====================================================

def guardar_rutina(usuario_id, rutina):
    supabase = get_supabase_client()
    datos = {
        "usuario_id":  usuario_id,
        "rutina_json": json.dumps(rutina, ensure_ascii=False)
    }
    supabase.table("rutinas").insert(datos).execute()


def obtener_rutina(usuario_id):
    supabase = get_supabase_client()
    respuesta = (
        supabase.table("rutinas")
        .select("*")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if respuesta.data:
        return json.loads(respuesta.data[0]["rutina_json"])
    return None


# =====================================================
# FUNCIONES DE SESIONES
# =====================================================

def guardar_sesion(usuario_id, dia_nombre, resultados):
    supabase = get_supabase_client()
    datos = {
        "usuario_id":      usuario_id,
        "dia_nombre":      dia_nombre,
        "resultados_json": json.dumps(resultados, ensure_ascii=False)
    }
    supabase.table("sesiones").insert(datos).execute()


def obtener_historial_sesiones(usuario_id, limite=10):
    supabase = get_supabase_client()
    respuesta = (
        supabase.table("sesiones")
        .select("*")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=True)
        .limit(limite)
        .execute()
    )
    sesiones = []
    for fila in respuesta.data:
        sesiones.append({
            "fecha":      fila["created_at"][:10],
            "dia":        fila["dia_nombre"],
            "resultados": json.loads(fila["resultados_json"])
        })
    return sesiones


def obtener_progreso_por_ejercicio(usuario_id):
    """
    Extrae el historial de pesos de TODOS los ejercicios del usuario,
    ordenado cronológicamente (del más antiguo al más reciente).

    Devuelve un diccionario donde cada clave es el nombre de un ejercicio
    y el valor es una lista de puntos de datos:

    {
        "Press de banca con barra": [
            {"sesion": 1, "fecha": "2026-04-01", "peso_usado": 32.5, "nuevo_peso": 35.0},
            {"sesion": 2, "fecha": "2026-04-03", "peso_usado": 35.0, "nuevo_peso": 35.0},
            ...
        ],
        "Jalón al pecho en polea": [...],
        ...
    }
    """
    supabase = get_supabase_client()

    # Obtenemos TODAS las sesiones del usuario, ordenadas de más antigua a más reciente
    respuesta = (
        supabase.table("sesiones")
        .select("*")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=False)  # False = cronológico (más antigua primero)
        .execute()
    )

    # Diccionario que iremos llenando
    progreso = {}

    for numero_sesion, fila in enumerate(respuesta.data, 1):
        fecha      = fila["created_at"][:10]
        resultados = json.loads(fila["resultados_json"])

        for resultado in resultados:
            nombre_ejercicio = resultado["ejercicio"]
            peso_usado       = resultado["peso_usado"]
            nuevo_peso       = resultado["nuevo_peso"]

            # Si es la primera vez que vemos este ejercicio, creamos su lista
            if nombre_ejercicio not in progreso:
                progreso[nombre_ejercicio] = []

            progreso[nombre_ejercicio].append({
                "sesion":      numero_sesion,
                "fecha":       fecha,
                "peso_usado":  peso_usado,
                "nuevo_peso":  nuevo_peso
            })

    return progreso
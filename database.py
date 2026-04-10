# database.py
# Este archivo maneja toda la comunicación con Supabase.
# El resto de la app solo llama a estas funciones,
# sin necesitar saber cómo funciona la base de datos por dentro.

import os
import json
from supabase import create_client

# =====================================================
# CONEXIÓN CON SUPABASE
# =====================================================
# os.environ.get() lee las variables de entorno que configuramos
# en Railway. Si no las encuentra (por ejemplo en local),
# devuelve None y la app mostrará un error claro.

def get_supabase_client():
    """
    Crea y devuelve el cliente de conexión a Supabase.
    Se llama cada vez que necesitamos hacer algo con la base de datos.
    """
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
    """
    Guarda el perfil del usuario en Supabase.
    Devuelve el ID único asignado al usuario.

    perfil → el diccionario con todos los datos del formulario
    """
    supabase = get_supabase_client()

    datos = {
        "nombre":      perfil["nombre"],
        "edad":        perfil["edad"],
        "peso":        perfil["peso"],
        "nivel_texto": perfil["nivel_texto"],
        "nivel_num":   perfil["nivel_num"],
        "objetivo":    perfil["objetivo"],
        "dias":        perfil["dias"],
        "minutos":     perfil["minutos"],
        "equipamiento":perfil["equipamiento"],
        "lesiones":    perfil.get("lesiones", "")
    }

    respuesta = supabase.table("usuarios").insert(datos).execute()

    # La respuesta contiene los datos insertados, incluyendo el ID generado
    usuario_id = respuesta.data[0]["id"]
    return usuario_id


def buscar_usuario_por_nombre(nombre):
    """
    Busca un usuario por nombre.
    Devuelve el usuario encontrado o None si no existe.

    Nota: en el futuro esto se reemplazará por login con email.
    Por ahora usamos el nombre como identificador simple.
    """
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
    """
    Guarda la rutina generada para un usuario.
    La rutina se convierte a texto JSON para guardarla en la base de datos.

    usuario_id → el ID del usuario al que pertenece esta rutina
    rutina     → el diccionario con la rutina completa
    """
    supabase = get_supabase_client()

    datos = {
        "usuario_id":  usuario_id,
        "rutina_json": json.dumps(rutina, ensure_ascii=False)
        # json.dumps convierte el diccionario Python a texto JSON
        # ensure_ascii=False permite guardar caracteres como tildes y ñ
    }

    supabase.table("rutinas").insert(datos).execute()


def obtener_rutina(usuario_id):
    """
    Obtiene la rutina más reciente de un usuario.
    Devuelve el diccionario de la rutina o None si no tiene ninguna.
    """
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
        # json.loads convierte el texto JSON de vuelta a diccionario Python
        return json.loads(respuesta.data[0]["rutina_json"])
    return None


# =====================================================
# FUNCIONES DE SESIONES
# =====================================================

def guardar_sesion(usuario_id, dia_nombre, resultados):
    """
    Guarda los resultados de una sesión de entrenamiento.

    usuario_id  → ID del usuario
    dia_nombre  → ej: "Lunes"
    resultados  → lista de resultados del algoritmo de IA
    """
    supabase = get_supabase_client()

    datos = {
        "usuario_id":       usuario_id,
        "dia_nombre":       dia_nombre,
        "resultados_json":  json.dumps(resultados, ensure_ascii=False)
    }

    supabase.table("sesiones").insert(datos).execute()


def obtener_historial_sesiones(usuario_id, limite=10):
    """
    Obtiene las últimas N sesiones de un usuario.
    Devuelve una lista de sesiones ordenadas de más reciente a más antigua.

    usuario_id → ID del usuario
    limite     → cuántas sesiones devolver (por defecto las últimas 10)
    """
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
            "fecha":      fila["created_at"][:10],  # Solo la fecha, sin la hora
            "dia":        fila["dia_nombre"],
            "resultados": json.loads(fila["resultados_json"])
        })

    return sesiones
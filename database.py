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
# AUTENTICACIÓN
# =====================================================

def registrar_usuario(email, password):
    """
    Crea una nueva cuenta con email y contraseña.
    Devuelve el objeto de sesión si funciona, o un mensaje de error.

    Supabase se encarga de:
    - Verificar que el email no está ya registrado
    - Cifrar la contraseña (nunca se guarda en texto plano)
    - Generar un ID único para el usuario
    """
    supabase = get_supabase_client()
    try:
        respuesta = supabase.auth.sign_up({
            "email":    email,
            "password": password
        })
        if respuesta.user:
            return {"ok": True, "user": respuesta.user, "session": respuesta.session}
        return {"ok": False, "error": "No se pudo crear la cuenta."}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def login_usuario(email, password):
    """
    Inicia sesión con email y contraseña.
    Devuelve la sesión si las credenciales son correctas, o un error.
    """
    supabase = get_supabase_client()
    try:
        respuesta = supabase.auth.sign_in_with_password({
            "email":    email,
            "password": password
        })
        if respuesta.user:
            return {"ok": True, "user": respuesta.user, "session": respuesta.session}
        return {"ok": False, "error": "Email o contraseña incorrectos."}
    except Exception as e:
        return {"ok": False, "error": "Email o contraseña incorrectos."}


def logout_usuario():
    """
    Cierra la sesión del usuario actual.
    """
    supabase = get_supabase_client()
    try:
        supabase.auth.sign_out()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# =====================================================
# FUNCIONES DE PERFIL DE USUARIO
# =====================================================

def guardar_perfil(auth_user_id, perfil):
    """
    Guarda el perfil del usuario vinculado a su cuenta de login.
    Usa auth_user_id para conectar el perfil con la cuenta de autenticación.
    """
    supabase = get_supabase_client()
    datos = {
        "auth_user_id":  auth_user_id,
        "nombre":        perfil["nombre"],
        "edad":          perfil["edad"],
        "peso":          perfil["peso"],
        "nivel_texto":   perfil["nivel_texto"],
        "nivel_num":     perfil["nivel_num"],
        "objetivo":      perfil["objetivo"],
        "dias":          perfil["dias"],
        "minutos":       perfil["minutos"],
        "equipamiento":  perfil["equipamiento"],
        "lesiones":      perfil.get("lesiones", "")
    }
    respuesta = supabase.table("usuarios").insert(datos).execute()
    return respuesta.data[0]["id"]


def obtener_perfil(auth_user_id):
    """
    Obtiene el perfil de un usuario por su auth_user_id.
    Devuelve el perfil o None si no tiene perfil creado todavía.
    """
    supabase = get_supabase_client()
    respuesta = (
        supabase.table("usuarios")
        .select("*")
        .eq("auth_user_id", auth_user_id)
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
    supabase = get_supabase_client()
    respuesta = (
        supabase.table("sesiones")
        .select("*")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=False)
        .execute()
    )
    progreso = {}
    for numero_sesion, fila in enumerate(respuesta.data, 1):
        fecha      = fila["created_at"][:10]
        resultados = json.loads(fila["resultados_json"])
        for resultado in resultados:
            nombre_ejercicio = resultado["ejercicio"]
            if nombre_ejercicio not in progreso:
                progreso[nombre_ejercicio] = []
            progreso[nombre_ejercicio].append({
                "sesion":     numero_sesion,
                "fecha":      fecha,
                "peso_usado": resultado["peso_usado"],
                "nuevo_peso": resultado["nuevo_peso"]
            })
    return progreso
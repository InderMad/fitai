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
    supabase = get_supabase_client()
    try:
        supabase.auth.sign_out()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# =====================================================
# FUNCIONES DE PERFIL
# =====================================================

def guardar_perfil(auth_user_id, perfil):
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


def actualizar_pesos_rutina(usuario_id, resultados_ia):
    rutina_actual = obtener_rutina(usuario_id)
    if not rutina_actual:
        return None

    nuevos_pesos = {
        r["ejercicio"]: r["nuevo_peso"]
        for r in resultados_ia
    }

    for dia in rutina_actual["dias"]:
        for ejercicio in dia["ejercicios"]:
            nombre = ejercicio["nombre"]
            if nombre in nuevos_pesos:
                ejercicio["peso_sugerido"] = nuevos_pesos[nombre]

    supabase = get_supabase_client()
    respuesta = (
        supabase.table("rutinas")
        .select("id")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if respuesta.data:
        rutina_id = respuesta.data[0]["id"]
        supabase.table("rutinas").update({
            "rutina_json": json.dumps(rutina_actual, ensure_ascii=False)
        }).eq("id", rutina_id).execute()

    return rutina_actual


# =====================================================
# FUNCIONES DE BLOQUES ← NUEVAS
# =====================================================

def guardar_bloque(usuario_id, bloque):
    """
    Guarda el bloque de entrenamiento del usuario.
    bloque → diccionario con numero_bloque, fecha_inicio, etc.
    """
    supabase = get_supabase_client()
    datos = {
        "usuario_id":  usuario_id,
        "bloque_json": json.dumps(bloque, ensure_ascii=False)
    }
    supabase.table("bloques").insert(datos).execute()


def obtener_bloque_actual(usuario_id):
    """
    Obtiene el bloque activo más reciente del usuario.
    Devuelve el bloque o None si no tiene ninguno.
    """
    supabase = get_supabase_client()
    respuesta = (
        supabase.table("bloques")
        .select("*")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if respuesta.data:
        return json.loads(respuesta.data[0]["bloque_json"])
    return None


def actualizar_bloque(usuario_id, bloque):
    """
    Actualiza el bloque actual del usuario.
    """
    supabase = get_supabase_client()
    respuesta = (
        supabase.table("bloques")
        .select("id")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if respuesta.data:
        bloque_id = respuesta.data[0]["id"]
        supabase.table("bloques").update({
            "bloque_json": json.dumps(bloque, ensure_ascii=False)
        }).eq("id", bloque_id).execute()


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
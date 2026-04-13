# database.py
import os
import json
from supabase import create_client


def get_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise Exception("❌ No se encontraron las variables SUPABASE_URL y SUPABASE_KEY.")
    return create_client(url, key)


def registrar_usuario(email, password):
    supabase = get_supabase_client()
    try:
        respuesta = supabase.auth.sign_up({"email": email, "password": password})
        if respuesta.user:
            return {"ok": True, "user": respuesta.user, "session": respuesta.session}
        return {"ok": False, "error": "No se pudo crear la cuenta."}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def login_usuario(email, password):
    supabase = get_supabase_client()
    try:
        respuesta = supabase.auth.sign_in_with_password({"email": email, "password": password})
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


def guardar_perfil(auth_user_id, perfil):
    supabase = get_supabase_client()
    datos = {
        "auth_user_id":          auth_user_id,
        "nombre":                perfil["nombre"],
        "edad":                  perfil["edad"],
        "peso":                  perfil["peso"],
        "genero":                perfil.get("genero", "Prefiero no decirlo"),
        "nivel_texto":           perfil["nivel_texto"],
        "nivel_num":             perfil["nivel_num"],
        "objetivo":              perfil["objetivo"],
        "musculos_prioritarios": json.dumps(perfil.get("musculos_prioritarios", [])),
        "dias":                  perfil["dias"],
        "minutos":               perfil["minutos"],
        "equipamiento":          perfil["equipamiento"],
        "lesiones":              perfil.get("lesiones", "")
    }
    respuesta = supabase.table("usuarios").insert(datos).execute()
    return respuesta.data[0]["id"]


def obtener_perfil(auth_user_id):
    supabase  = get_supabase_client()
    respuesta = (
        supabase.table("usuarios")
        .select("*")
        .eq("auth_user_id", auth_user_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if respuesta.data:
        perfil = respuesta.data[0]
        if isinstance(perfil.get("musculos_prioritarios"), str):
            try:
                perfil["musculos_prioritarios"] = json.loads(perfil["musculos_prioritarios"])
            except Exception:
                perfil["musculos_prioritarios"] = []
        return perfil
    return None


def guardar_rutina(usuario_id, rutina):
    supabase = get_supabase_client()
    supabase.table("rutinas").insert({
        "usuario_id":  usuario_id,
        "rutina_json": json.dumps(rutina, ensure_ascii=False)
    }).execute()


def obtener_rutina(usuario_id):
    supabase  = get_supabase_client()
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
    nuevos_pesos = {r["ejercicio"]: r["nuevo_peso"] for r in resultados_ia}
    for dia in rutina_actual["dias"]:
        for ejercicio in dia["ejercicios"]:
            if ejercicio["nombre"] in nuevos_pesos:
                ejercicio["peso_sugerido"] = nuevos_pesos[ejercicio["nombre"]]
    supabase  = get_supabase_client()
    respuesta = (
        supabase.table("rutinas")
        .select("id")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if respuesta.data:
        supabase.table("rutinas").update({
            "rutina_json": json.dumps(rutina_actual, ensure_ascii=False)
        }).eq("id", respuesta.data[0]["id"]).execute()
    return rutina_actual


def guardar_bloque(usuario_id, bloque):
    supabase = get_supabase_client()
    supabase.table("bloques").insert({
        "usuario_id":  usuario_id,
        "bloque_json": json.dumps(bloque, ensure_ascii=False)
    }).execute()


def obtener_bloque_actual(usuario_id):
    supabase  = get_supabase_client()
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
    supabase  = get_supabase_client()
    respuesta = (
        supabase.table("bloques")
        .select("id")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if respuesta.data:
        supabase.table("bloques").update({
            "bloque_json": json.dumps(bloque, ensure_ascii=False)
        }).eq("id", respuesta.data[0]["id"]).execute()


def guardar_sesion(usuario_id, dia_nombre, resultados):
    supabase = get_supabase_client()
    supabase.table("sesiones").insert({
        "usuario_id":      usuario_id,
        "dia_nombre":      dia_nombre,
        "resultados_json": json.dumps(resultados, ensure_ascii=False)
    }).execute()


def obtener_historial_sesiones(usuario_id, limite=10):
    supabase  = get_supabase_client()
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


def obtener_sesiones_mes(usuario_id, anio, mes):
    """
    Obtiene todas las sesiones de un mes concreto.

    anio → año (ej: 2026)
    mes  → mes en número (ej: 4 para abril)

    Devuelve un diccionario donde la clave es la fecha (string "YYYY-MM-DD")
    y el valor es una lista de sesiones de ese día.

    Ejemplo:
    {
        "2026-04-10": [
            {"dia": "Lunes", "enfoque": "Empuje", "resultados": [...]}
        ],
        "2026-04-14": [...]
    }
    """
    import calendar

    supabase = get_supabase_client()

    # Calcular primer y último día del mes
    ultimo_dia   = calendar.monthrange(anio, mes)[1]
    fecha_inicio = f"{anio}-{mes:02d}-01"
    fecha_fin    = f"{anio}-{mes:02d}-{ultimo_dia}"

    respuesta = (
        supabase.table("sesiones")
        .select("*")
        .eq("usuario_id", usuario_id)
        .gte("created_at", fecha_inicio)
        .lte("created_at", fecha_fin + "T23:59:59")
        .order("created_at", desc=False)
        .execute()
    )

    sesiones_por_dia = {}
    for fila in respuesta.data:
        fecha = fila["created_at"][:10]
        if fecha not in sesiones_por_dia:
            sesiones_por_dia[fecha] = []
        sesiones_por_dia[fecha].append({
            "dia":        fila["dia_nombre"],
            "resultados": json.loads(fila["resultados_json"])
        })

    return sesiones_por_dia


def obtener_todas_sesiones(usuario_id):
    """
    Obtiene TODAS las sesiones del usuario para calcular
    rachas y estadísticas globales.
    Devuelve lista de fechas únicas ordenadas.
    """
    supabase  = get_supabase_client()
    respuesta = (
        supabase.table("sesiones")
        .select("created_at, dia_nombre")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=False)
        .execute()
    )

    fechas = sorted(set(fila["created_at"][:10] for fila in respuesta.data))
    return fechas


def obtener_progreso_por_ejercicio(usuario_id):
    supabase  = get_supabase_client()
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


def guardar_favoritos(usuario_id, favoritos):
    supabase  = get_supabase_client()
    respuesta = (
        supabase.table("favoritos")
        .select("id")
        .eq("usuario_id", usuario_id)
        .execute()
    )
    datos = {
        "usuario_id":     usuario_id,
        "favoritos_json": json.dumps(favoritos, ensure_ascii=False)
    }
    if respuesta.data:
        supabase.table("favoritos").update({
            "favoritos_json": json.dumps(favoritos, ensure_ascii=False)
        }).eq("usuario_id", usuario_id).execute()
    else:
        supabase.table("favoritos").insert(datos).execute()


def obtener_favoritos(usuario_id):
    supabase  = get_supabase_client()
    respuesta = (
        supabase.table("favoritos")
        .select("*")
        .eq("usuario_id", usuario_id)
        .execute()
    )
    if respuesta.data:
        return json.loads(respuesta.data[0]["favoritos_json"])
    return []


def guardar_niveles_sesion(usuario_id, niveles):
    supabase = get_supabase_client()
    supabase.table("historial_niveles").insert({
        "usuario_id":   usuario_id,
        "niveles_json": json.dumps(niveles, ensure_ascii=False)
    }).execute()


def obtener_ultimo_nivel(usuario_id, ejercicio):
    supabase  = get_supabase_client()
    respuesta = (
        supabase.table("historial_niveles")
        .select("*")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=True)
        .limit(10)
        .execute()
    )
    for fila in respuesta.data:
        niveles = json.loads(fila["niveles_json"])
        for n in niveles:
            if n["ejercicio"] == ejercicio:
                return n
    return None
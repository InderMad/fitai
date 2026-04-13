# app.py
import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date, timedelta
from generador_rutinas import generar_rutina, EJERCICIOS
from algoritmo_ia import analizar_sesion_completa
from ia_feedback import generar_feedback_sesion
from strength_standards import (
    calcular_nivel_fuerza, ejercicios_con_standard, NIVELES
)
from bloques import (
    crear_bloque_inicial, calcular_semana_del_bloque,
    obtener_fase_actual, ajustar_rutina_por_fase,
    generar_resumen_bloque
)
from database import (
    registrar_usuario, login_usuario, logout_usuario,
    guardar_perfil, obtener_perfil,
    guardar_rutina, obtener_rutina, actualizar_pesos_rutina,
    guardar_sesion, obtener_historial_sesiones,
    obtener_sesiones_mes, obtener_todas_sesiones,
    obtener_progreso_por_ejercicio,
    guardar_bloque, obtener_bloque_actual, actualizar_bloque,
    guardar_favoritos, obtener_favoritos,
    guardar_niveles_sesion, obtener_ultimo_nivel,
    get_supabase_client
)
import json

# =====================================================
# CONFIGURACIÓN
# =====================================================
st.set_page_config(
    page_title="FitAI - Tu entrenador inteligente",
    page_icon="🏋️",
    layout="centered"
)

# =====================================================
# SELECTOR DE RPE
# =====================================================
def selector_rpe(key, valor_defecto=7):
    state_key = f"rpe_{key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = valor_defecto

    def color_rpe(n):
        if n <= 4:   return "🟢"
        elif n <= 7: return "🟠"
        else:        return "🔴"

    cols = st.columns(10)
    for i, col in enumerate(cols):
        numero       = i + 1
        icono        = color_rpe(numero)
        seleccionado = st.session_state[state_key] == numero
        with col:
            etiqueta = f"{icono}\n{numero}" if seleccionado else str(numero)
            if st.button(etiqueta, key=f"rpe_btn_{key}_{numero}"):
                st.session_state[state_key] = numero
                st.rerun()

    valor = st.session_state[state_key]
    if valor <= 4:
        st.caption(f"RPE {valor} — 🟢 Esfuerzo bajo · Te quedan muchas repeticiones")
    elif valor <= 7:
        st.caption(f"RPE {valor} — 🟠 Esfuerzo medio · Te quedan 2–4 repeticiones")
    else:
        st.caption(f"RPE {valor} — 🔴 Esfuerzo alto · Estás cerca del límite")
    return valor


# =====================================================
# COMPONENTE: BARRA DE NIVEL DE FUERZA
# =====================================================
def mostrar_nivel_fuerza(resultado_nivel):
    if not resultado_nivel:
        return
    nivel     = resultado_nivel["nivel"]
    nivel_idx = resultado_nivel["nivel_idx"]
    percentil = resultado_nivel["percentil"]
    rm1       = resultado_nivel["rm1_estimado"]
    umbrales  = resultado_nivel["umbrales_kg"]
    siguiente = resultado_nivel["siguiente_nivel"]
    colores_nivel = {"Principiante":"🔵","Novato":"🟢","Intermedio":"🟡","Avanzado":"🟠","Elite":"🔴"}
    icono = colores_nivel.get(nivel, "⚪")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nivel", f"{icono} {nivel}")
    with col2:
        st.metric("Top mundial", f"{100 - percentil}%")
    if nivel_idx < len(NIVELES) - 1:
        umbral_actual    = umbrales[nivel_idx]
        umbral_siguiente = umbrales[nivel_idx + 1]
        if umbral_siguiente > umbral_actual:
            pct = min(max((rm1 - umbral_actual) / (umbral_siguiente - umbral_actual), 0.0), 1.0)
        else:
            pct = 1.0
        progreso_global = (nivel_idx + pct) / (len(NIVELES) - 1)
    else:
        progreso_global = 1.0
    st.progress(progreso_global, text="Principiante → Novato → Intermedio → Avanzado → Elite")
    st.caption(f"Tu 1RM estimado: **{rm1} kg**")
    with st.expander("📊 Ver umbrales de referencia"):
        for nombre_nivel, umbral in zip(NIVELES, umbrales):
            marcador = "▶️ " if nombre_nivel == nivel else "   "
            st.write(f"{marcador}**{nombre_nivel}:** {umbral} kg")
    if siguiente:
        st.info(f"🎯 Para llegar a **{siguiente['nombre']}** necesitas **{siguiente['umbral_kg']} kg** · Te faltan **{siguiente['faltan_kg']} kg**")
    else:
        st.success("🏆 ¡Has alcanzado el nivel Elite!")


# =====================================================
# FUNCIÓN: EJERCICIOS SIMILARES
# =====================================================
def obtener_ejercicios_similares(grupo, nombre_actual, nivel):
    return [
        e["nombre"] for e in EJERCICIOS.get(grupo, [])
        if e["nombre"] != nombre_actual and e["nivel_min"] <= nivel
    ]

def calcular_peso_para_ejercicio(grupo, nombre_ejercicio, peso_usuario):
    from generador_rutinas import calcular_peso_inicial
    ejercicio = next((e for e in EJERCICIOS.get(grupo, []) if e["nombre"] == nombre_ejercicio), None)
    if ejercicio:
        return calcular_peso_inicial(peso_usuario, ejercicio["peso_inicial_pct"])
    return None


# =====================================================
# FUNCIÓN: CALCULAR RACHA
# =====================================================
def calcular_racha(fechas_entrenadas):
    """
    Calcula la racha actual de días consecutivos entrenando.
    fechas_entrenadas → lista de strings "YYYY-MM-DD" ordenadas
    """
    if not fechas_entrenadas:
        return 0

    hoy        = date.today()
    fechas_set = set(date.fromisoformat(f) for f in fechas_entrenadas)

    # Empezamos desde hoy o ayer (si hoy no entrenó todavía)
    inicio = hoy if hoy in fechas_set else hoy - timedelta(days=1)

    if inicio not in fechas_set:
        return 0

    racha = 0
    dia   = inicio
    while dia in fechas_set:
        racha += 1
        dia   -= timedelta(days=1)

    return racha


# =====================================================
# INICIALIZAR SESSION STATE
# =====================================================
for key, default in {
    "auth_user_id":       None,
    "usuario_id":         None,
    "perfil":             None,
    "rutina":             None,
    "bloque":             None,
    "pantalla":           "rutina",
    "resultados_sesion":  [],
    "dia_seleccionado":   None,
    "auth_pantalla":      "login",
    "feedback_ia":        None,
    "subidas_nivel":      [],
    "favoritos":          [],
    "cambios_ejercicios": {},
    "cal_anio":           datetime.now().year,
    "cal_mes":            datetime.now().month,
    "cal_dia_detalle":    None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Recuperar sesión automáticamente ──
if not st.session_state.auth_user_id:
    try:
        token = st.query_params.get("token", None)
        if token:
            supabase     = get_supabase_client()
            sesion       = supabase.auth.get_user(token)
            if sesion and sesion.user:
                auth_id      = sesion.user.id
                perfil_db    = obtener_perfil(auth_id)
                if perfil_db:
                    rutina_db    = obtener_rutina(perfil_db["id"])
                    bloque_db    = obtener_bloque_actual(perfil_db["id"])
                    favoritos_db = obtener_favoritos(perfil_db["id"])
                    st.session_state.auth_user_id = auth_id
                    st.session_state.usuario_id   = perfil_db["id"]
                    st.session_state.perfil       = perfil_db
                    st.session_state.rutina       = rutina_db
                    st.session_state.bloque       = bloque_db
                    st.session_state.favoritos    = favoritos_db
                    st.session_state.pantalla     = "rutina"
    except Exception:
        pass


# =====================================================
# PANTALLA DE AUTENTICACIÓN
# =====================================================
if not st.session_state.auth_user_id:

    st.title("🏋️ FitAI")
    st.write("Tu entrenador personal inteligente.")
    st.divider()

    tab_login, tab_registro = st.tabs(["🔑 Iniciar sesión", "✨ Crear cuenta"])

    with tab_login:
        st.subheader("Bienvenido de vuelta")
        email_login    = st.text_input("Email", key="email_login", placeholder="tu@email.com")
        password_login = st.text_input("Contraseña", type="password", key="pass_login", placeholder="Tu contraseña")
        if st.button("Entrar →", use_container_width=True, type="primary"):
            if not email_login or not password_login:
                st.error("Por favor rellena el email y la contraseña.")
            else:
                with st.spinner("Verificando credenciales..."):
                    resultado = login_usuario(email_login, password_login)
                if resultado["ok"]:
                    auth_id = resultado["user"].id
                    if resultado["session"]:
                        st.query_params["token"] = resultado["session"].access_token
                    perfil_db = obtener_perfil(auth_id)
                    if perfil_db:
                        rutina_db    = obtener_rutina(perfil_db["id"])
                        bloque_db    = obtener_bloque_actual(perfil_db["id"])
                        favoritos_db = obtener_favoritos(perfil_db["id"])
                        st.session_state.auth_user_id = auth_id
                        st.session_state.usuario_id   = perfil_db["id"]
                        st.session_state.perfil       = perfil_db
                        st.session_state.rutina       = rutina_db
                        st.session_state.bloque       = bloque_db
                        st.session_state.favoritos    = favoritos_db
                        st.session_state.pantalla     = "rutina"
                    else:
                        st.session_state.auth_user_id = auth_id
                        st.session_state.pantalla     = "crear_perfil"
                    st.rerun()
                else:
                    st.error(f"❌ {resultado['error']}")

    with tab_registro:
        st.subheader("Crea tu cuenta gratuita")
        email_reg    = st.text_input("Email", key="email_reg", placeholder="tu@email.com")
        password_reg = st.text_input("Contraseña", type="password", key="pass_reg", placeholder="Mínimo 6 caracteres")
        password_rep = st.text_input("Repite la contraseña", type="password", key="pass_rep", placeholder="Repite la contraseña")
        if st.button("Crear cuenta →", use_container_width=True, type="primary"):
            if not email_reg or not password_reg:
                st.error("Rellena todos los campos.")
            elif password_reg != password_rep:
                st.error("Las contraseñas no coinciden.")
            elif len(password_reg) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                with st.spinner("Creando tu cuenta..."):
                    resultado = registrar_usuario(email_reg, password_reg)
                if resultado["ok"]:
                    if resultado["session"]:
                        st.query_params["token"] = resultado["session"].access_token
                    st.session_state.auth_user_id = resultado["user"].id
                    st.session_state.pantalla     = "crear_perfil"
                    st.rerun()
                else:
                    st.error(f"❌ {resultado['error']}")


# =====================================================
# PANTALLA DE CREAR PERFIL
# =====================================================
elif st.session_state.auth_user_id and not st.session_state.perfil:

    st.title("🏋️ Crea tu perfil de entrenamiento")
    st.write("Solo necesitamos esto una vez para generar tu rutina personalizada.")

    st.header("1️⃣ Datos personales")
    nombre = st.text_input("¿Cómo te llamas?", placeholder="Tu nombre")
    col1, col2 = st.columns(2)
    with col1:
        edad = st.number_input("Tu edad", min_value=16, max_value=70, value=25)
    with col2:
        peso = st.number_input("Tu peso (kg)", min_value=40.0, max_value=200.0, value=70.0, step=0.5)
    st.divider()

    st.header("2️⃣ Género")
    st.caption("Nos ayuda a personalizar el enfoque muscular y la división de tu rutina.")
    genero = st.radio("Género:", options=["Hombre","Mujer","Prefiero no decirlo"],
                       label_visibility="collapsed", horizontal=True)
    st.divider()

    st.header("3️⃣ Tu experiencia")
    nivel_texto = st.selectbox("¿Cuánto tiempo llevas entrenando?", options=[
        "Principiante — Menos de 6 meses",
        "Intermedio — Entre 6 meses y 2 años",
        "Avanzado — Más de 2 años"
    ])
    nivel_num = 1 if "Principiante" in nivel_texto else (2 if "Intermedio" in nivel_texto else 3)
    if nivel_num == 3:
        st.success("💡 Como usuario avanzado, tu rutina incluirá técnicas avanzadas.")
    st.divider()

    st.header("4️⃣ Tu objetivo")
    objetivo = st.radio("Objetivo:", options=[
        "💪 Ganar músculo (hipertrofia)",
        "🔥 Perder grasa (mantener músculo)",
        "🏋️ Ganar fuerza máxima",
        "🏃 Mejorar condición física general"
    ], label_visibility="collapsed")
    st.divider()

    st.header("5️⃣ ¿En qué músculos quieres enfocarte más?")
    st.caption("Recibirán más ejercicios en tu rutina.")
    opciones_musculos = {
        "🍑 Glúteos":"gluteos","🦵 Piernas":"piernas","🫁 Pecho":"pecho",
        "🔙 Espalda":"espalda","🥥 Hombros":"hombros","💪 Bíceps":"biceps",
        "🔱 Tríceps":"triceps","🎯 Deltoides medio":"deltoides_medio",
        "🦵 Cuádriceps":"cuadriceps","🔻 Femoral":"femoral",
    }
    musculos_seleccionados = st.multiselect("Selecciona tus músculos prioritarios (opcional):",
                                             options=list(opciones_musculos.keys()), default=[])
    musculos_prioritarios = [opciones_musculos[m] for m in musculos_seleccionados]
    st.divider()

    st.header("6️⃣ Disponibilidad")
    dias = st.select_slider("Días/semana", options=[1,2,3,4,5,6], value=3)
    objetivo_lower = objetivo.lower()
    if dias == 1:
        st.info("💡 Haremos un Full Body completo.")
    elif dias == 2:
        st.info("💡 Haremos Tren Superior / Tren Inferior.")
    elif dias == 3:
        st.info("💡 Haremos Superior + Inferior + Full Body." if (genero=="Mujer" or "grasa" in objetivo_lower) else "💡 Haremos Empuje / Tirón / Pierna.")
    elif dias == 4:
        st.info("💡 Haremos 4 días adaptados a tu objetivo y género.")
    elif dias == 5:
        st.info("💡 Haremos 5 días adaptados a tu objetivo y género.")
    else:
        st.info("💡 Haremos 6 días adaptados a tu objetivo y género.")
    minutos = st.selectbox("Tiempo por sesión", options=[30,45,60,90],
                            index=2, format_func=lambda x: f"{x} minutos")
    st.divider()

    st.header("7️⃣ Equipamiento")
    equipamiento = st.radio("¿Con qué entrenas?", options=[
        "🏠 Sin equipamiento (solo peso corporal)",
        "🏠 Tengo mancuernas en casa",
        "🏢 Tengo acceso a un gimnasio completo"
    ])
    st.divider()

    st.header("8️⃣ Lesiones")
    tiene_lesiones = st.toggle("¿Tienes alguna lesión actualmente?")
    lesiones_texto = ""
    if tiene_lesiones:
        lesiones_texto = st.text_area("Descríbela:", placeholder="Ejemplo: molestias en rodilla derecha")
    st.divider()

    if st.button("Guardar perfil y generar mi rutina →", disabled=not nombre,
                  use_container_width=True, type="primary"):
        perfil = {
            "nombre":nombre,"edad":edad,"peso":peso,"genero":genero,
            "nivel_texto":nivel_texto,"nivel_num":nivel_num,"objetivo":objetivo,
            "musculos_prioritarios":musculos_prioritarios,"dias":dias,"minutos":minutos,
            "equipamiento":equipamiento,"lesiones":lesiones_texto
        }
        with st.spinner("Generando tu rutina personalizada..."):
            usuario_id = guardar_perfil(st.session_state.auth_user_id, perfil)
            rutina     = generar_rutina(perfil)
            guardar_rutina(usuario_id, rutina)
            bloque     = crear_bloque_inicial()
            guardar_bloque(usuario_id, bloque)
        st.session_state.usuario_id = usuario_id
        st.session_state.perfil     = perfil
        st.session_state.rutina     = rutina
        st.session_state.bloque     = bloque
        st.session_state.favoritos  = []
        st.session_state.pantalla   = "rutina"
        st.rerun()


# =====================================================
# PANTALLAS PRINCIPALES
# =====================================================
else:
    perfil = st.session_state.perfil
    rutina = st.session_state.rutina
    bloque = st.session_state.bloque

    if not bloque:
        bloque = crear_bloque_inicial()
        guardar_bloque(st.session_state.usuario_id, bloque)
        st.session_state.bloque = bloque

    info_semana = calcular_semana_del_bloque(bloque["fecha_inicio"])
    fase_actual = obtener_fase_actual(info_semana["semana_en_bloque"])
    rutina_hoy  = ajustar_rutina_por_fase(rutina, fase_actual)

    # --------------------------------------------------
    # PANTALLA: RUTINA
    # --------------------------------------------------
    if st.session_state.pantalla == "rutina":

        col_titulo, col_logout = st.columns([4, 1])
        with col_titulo:
            st.title(f"💪 Tu rutina, {perfil['nombre']}")
        with col_logout:
            if st.button("Salir", use_container_width=True):
                logout_usuario()
                st.query_params.clear()
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        for subida in st.session_state.get("subidas_nivel", []):
            st.success(f"⬆️ ¡Subiste de nivel en **{subida['ejercicio']}**! Ahora eres **{subida['nivel_nuevo']}** (Top {100-subida['percentil']}% mundial)")
        st.session_state.subidas_nivel = []

        color_fase = {"blue":"info","green":"success","orange":"warning"}.get(fase_actual["color"],"info")
        getattr(st, color_fase)(
            f"**Bloque {info_semana['numero_bloque']} · Semana {info_semana['semana_en_bloque']} de 8 · "
            f"Fase: {fase_actual['nombre']}** — {fase_actual['descripcion']}"
        )
        if info_semana["semana_en_bloque"] == 8:
            st.warning("🔄 Esta semana es tu **semana de deload**.")
        if info_semana["semana_en_bloque"] == 7:
            st.info("⚠️ La próxima semana es tu semana de deload. ¡Aprieta fuerte esta semana!")

        st.progress(info_semana["semana_en_bloque"]/8,
                    text=f"Progreso del bloque: semana {info_semana['semana_en_bloque']}/8")
        st.divider()

        nombres_estructura = {
            "fullbody_1dia":"Full Body","superior_inferior":"Superior / Inferior",
            "superior_inferior_fullbody":"Superior + Inferior + Full Body",
            "empuje_tiron_pierna":"Empuje / Tirón / Pierna",
            "4dias_chica_masa":"4 Días — Especialización Femenina",
            "4dias_grasa":"4 Días — Pérdida de Grasa",
            "4dias_chico_masa":"Empuje / Tirón / Pierna / Hombro+Brazo",
            "5dias_chica_masa":"5 Días — Especialización Femenina",
            "5dias_grasa":"5 Días — Pérdida de Grasa",
            "5dias_chico_masa":"Empuje × 2 / Tirón × 2 / Pierna",
            "6dias_chica_masa":"6 Días — Especialización Femenina",
            "6dias_grasa":"6 Días — Pérdida de Grasa",
            "6dias_chico_masa":"Empuje × 2 / Tirón × 2 / Pierna × 2",
        }
        nombre_estructura = nombres_estructura.get(rutina["estructura"], rutina["estructura"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Series HOY",   f"{fase_actual['series']} series")
        col2.metric("Repeticiones", f"{rutina['reps_min']}–{rutina['reps_max']} reps")
        col3.metric("RPE objetivo", f"{fase_actual['rpe_objetivo']}/10")
        st.markdown(f"**División:** {nombre_estructura}")

        prioritarios = perfil.get("musculos_prioritarios", [])
        if prioritarios:
            st.caption(f"🎯 Músculos prioritarios: {', '.join(prioritarios)}")

        st.divider()

        # Navegación — ahora con 5 botones en 2 filas
        col_n1, col_n2, col_n3 = st.columns(3)
        with col_n1:
            if st.button("📈 Progreso", use_container_width=True):
                st.session_state.pantalla = "progreso"
                st.rerun()
        with col_n2:
            if st.button("📅 Calendario", use_container_width=True):
                st.session_state.pantalla    = "calendario"
                st.session_state.cal_anio    = datetime.now().year
                st.session_state.cal_mes     = datetime.now().month
                st.session_state.cal_dia_detalle = None
                st.rerun()
        with col_n3:
            if st.button("📊 Bloque", use_container_width=True):
                st.session_state.pantalla = "resumen_bloque"
                st.rerun()

        col_n4, col_n5, _ = st.columns(3)
        with col_n4:
            if st.button("🏆 Ranking", use_container_width=True):
                st.session_state.pantalla = "ranking"
                st.rerun()
        with col_n5:
            if st.button("✏️ Perfil", use_container_width=True):
                st.session_state.pantalla = "editar_perfil"
                st.rerun()

        st.divider()
        st.subheader("📋 ¿Listo para entrenar hoy?")
        opciones_dias = [d["dia"] for d in rutina_hoy["dias"]]
        dia_elegido   = st.selectbox("¿Qué día entrenas hoy?", opciones_dias)

        if st.button("🏋️ Empezar sesión de hoy →", use_container_width=True, type="primary"):
            st.session_state.dia_seleccionado = dia_elegido
            st.session_state.pantalla = "sesion"
            st.rerun()

        st.divider()

        historial = obtener_historial_sesiones(st.session_state.usuario_id, limite=5)
        if historial:
            st.subheader("📅 Tus últimas sesiones")
            for sesion in historial:
                with st.expander(f"📅 {sesion['fecha']} — {sesion['dia']}"):
                    for resultado in sesion["resultados"]:
                        emoji = resultado.get("emoji","➡️")
                        st.write(f"{emoji} **{resultado['ejercicio']}** → {resultado['nuevo_peso']} kg")

        st.divider()
        st.subheader("📅 Tu rutina completa")
        nivel_usuario = perfil.get("nivel_num", 1)

        if "cambios_ejercicios" not in st.session_state:
            st.session_state.cambios_ejercicios = {}

        for idx_dia, dia in enumerate(rutina_hoy["dias"]):
            with st.expander(f"📅 {dia['dia']} — {dia['enfoque']}"):
                for idx_ej, ejercicio in enumerate(dia["ejercicios"]):
                    peso_texto   = f"{ejercicio['peso_sugerido']} kg" if ejercicio["peso_sugerido"] else "Peso corporal"
                    grupo        = ejercicio["grupo"]
                    nombre_ej    = ejercicio["nombre"]
                    cambio_key   = f"cambio_{idx_dia}_{idx_ej}"
                    selector_key = f"selector_{idx_dia}_{idx_ej}"

                    with st.container(border=True):
                        col_num, col_info, col_peso, col_btn = st.columns([0.4, 2.5, 1.5, 1.2])
                        with col_num:
                            st.markdown(f"### {idx_ej+1}")
                        with col_info:
                            st.markdown(f"**{nombre_ej}**")
                            st.caption(f"Grupo: {grupo.replace('_',' ').capitalize()}")
                            if ejercicio.get("tecnica"):
                                st.caption(f"⚡ {ejercicio['tecnica']['nombre']}: {ejercicio['tecnica']['descripcion']}")
                        with col_peso:
                            st.markdown(f"**{ejercicio['series']} × {ejercicio['reps_min']}–{ejercicio['reps_max']} reps**")
                            st.markdown(f"📦 {peso_texto}")
                        with col_btn:
                            abierto = st.session_state.cambios_ejercicios.get(cambio_key, False)
                            if st.button("✕ Cerrar" if abierto else "🔄 Cambiar",
                                          key=f"btn_{cambio_key}", use_container_width=True):
                                st.session_state.cambios_ejercicios[cambio_key] = not abierto
                                st.rerun()

                    if st.session_state.cambios_ejercicios.get(cambio_key, False):
                        similares = obtener_ejercicios_similares(grupo, nombre_ej, nivel_usuario)
                        if not similares:
                            st.warning("No hay más ejercicios disponibles para este grupo y nivel.")
                        else:
                            with st.container(border=True):
                                st.caption(f"🔄 Elige un alternativo de **{grupo.replace('_',' ').capitalize()}**:")
                                ejercicio_nuevo = st.selectbox("", options=similares, key=selector_key,
                                                                label_visibility="collapsed")
                                col_conf, col_cancel = st.columns(2)
                                with col_conf:
                                    if st.button("✅ Confirmar", key=f"confirm_{cambio_key}",
                                                  use_container_width=True, type="primary"):
                                        nuevo_peso = calcular_peso_para_ejercicio(grupo, ejercicio_nuevo, perfil["peso"])
                                        ra = st.session_state.rutina
                                        ra["dias"][idx_dia]["ejercicios"][idx_ej]["nombre"]        = ejercicio_nuevo
                                        ra["dias"][idx_dia]["ejercicios"][idx_ej]["peso_sugerido"] = nuevo_peso
                                        ra["dias"][idx_dia]["ejercicios"][idx_ej]["tecnica"]       = None
                                        st.session_state.rutina = ra
                                        supa = get_supabase_client()
                                        resp = (supa.table("rutinas").select("id")
                                                .eq("usuario_id", st.session_state.usuario_id)
                                                .order("created_at", desc=True).limit(1).execute())
                                        if resp.data:
                                            supa.table("rutinas").update({
                                                "rutina_json": json.dumps(ra, ensure_ascii=False)
                                            }).eq("id", resp.data[0]["id"]).execute()
                                        st.session_state.cambios_ejercicios[cambio_key] = False
                                        st.success(f"✅ Cambiado a **{ejercicio_nuevo}**")
                                        st.rerun()
                                with col_cancel:
                                    if st.button("✕ Cancelar", key=f"cancel_{cambio_key}", use_container_width=True):
                                        st.session_state.cambios_ejercicios[cambio_key] = False
                                        st.rerun()

    # --------------------------------------------------
    # PANTALLA: CALENDARIO ← NUEVA
    # --------------------------------------------------
    elif st.session_state.pantalla == "calendario":

        st.title("📅 Calendario de entrenamientos")

        if st.button("← Volver a la rutina"):
            st.session_state.pantalla = "rutina"
            st.rerun()

        st.divider()

        # ── Navegación mes ──
        col_ant, col_mes, col_sig = st.columns([1, 3, 1])
        with col_ant:
            if st.button("◀", use_container_width=True):
                if st.session_state.cal_mes == 1:
                    st.session_state.cal_mes  = 12
                    st.session_state.cal_anio -= 1
                else:
                    st.session_state.cal_mes -= 1
                st.session_state.cal_dia_detalle = None
                st.rerun()
        with col_mes:
            nombres_meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                             "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
            st.markdown(f"### {nombres_meses[st.session_state.cal_mes-1]} {st.session_state.cal_anio}",
                        unsafe_allow_html=False)
        with col_sig:
            if st.button("▶", use_container_width=True):
                if st.session_state.cal_mes == 12:
                    st.session_state.cal_mes  = 1
                    st.session_state.cal_anio += 1
                else:
                    st.session_state.cal_mes += 1
                st.session_state.cal_dia_detalle = None
                st.rerun()

        # ── Cargar sesiones del mes ──
        with st.spinner("Cargando..."):
            sesiones_mes   = obtener_sesiones_mes(
                st.session_state.usuario_id,
                st.session_state.cal_anio,
                st.session_state.cal_mes
            )
            todas_fechas   = obtener_todas_sesiones(st.session_state.usuario_id)
            racha          = calcular_racha(todas_fechas)
            total_mes      = len(sesiones_mes)

        # ── Métricas ──
        col1, col2, col3 = st.columns(3)
        col1.metric("Sesiones este mes", total_mes)
        col2.metric("🔥 Racha actual",   f"{racha} días")
        col3.metric("Total histórico",   len(todas_fechas))

        st.divider()

        # ── Calendario visual ──
        anio = st.session_state.cal_anio
        mes  = st.session_state.cal_mes

        # Obtener matriz del mes (semanas como filas, días como columnas)
        cal       = calendar.monthcalendar(anio, mes)
        dias_sem  = ["L", "M", "X", "J", "V", "S", "D"]

        # Cabecera de días
        cols_header = st.columns(7)
        for i, dia_sem in enumerate(dias_sem):
            cols_header[i].markdown(f"**{dia_sem}**")

        # Filas del calendario
        hoy_str = date.today().isoformat()

        for semana in cal:
            cols_semana = st.columns(7)
            for i, num_dia in enumerate(semana):
                if num_dia == 0:
                    cols_semana[i].write("")
                    continue

                fecha_str = f"{anio}-{mes:02d}-{num_dia:02d}"
                entrenado = fecha_str in sesiones_mes
                es_hoy    = fecha_str == hoy_str

                # Emoji según el estado del día
                if entrenado and es_hoy:
                    etiqueta = f"✅{num_dia}🌟"
                elif entrenado:
                    etiqueta = f"✅{num_dia}"
                elif es_hoy:
                    etiqueta = f"**{num_dia}**🔵"
                else:
                    etiqueta = str(num_dia)

                with cols_semana[i]:
                    if entrenado:
                        if st.button(etiqueta, key=f"cal_{fecha_str}",
                                      use_container_width=True, type="primary"):
                            st.session_state.cal_dia_detalle = fecha_str
                            st.rerun()
                    else:
                        st.markdown(etiqueta)

        st.divider()

        # ── Leyenda ──
        st.caption("✅ = Día entrenado · 🔵 = Hoy · 🌟 = Hoy y entrenado")

        # ── Detalle del día seleccionado ──
        if st.session_state.cal_dia_detalle:
            fecha_detalle = st.session_state.cal_dia_detalle
            sesiones_dia  = sesiones_mes.get(fecha_detalle, [])

            st.divider()
            st.subheader(f"📋 Sesiones del {fecha_detalle}")

            for sesion in sesiones_dia:
                with st.container(border=True):
                    st.markdown(f"**{sesion['dia']}**")
                    for resultado in sesion["resultados"]:
                        emoji = resultado.get("emoji","➡️")
                        decision_texto = {
                            "subir":    "⬆️ Subió de peso",
                            "bajar":    "⬇️ Bajó de peso",
                            "mantener": "➡️ Mantuvo peso"
                        }.get(resultado.get("decision",""), "")
                        st.write(
                            f"{emoji} **{resultado['ejercicio']}** — "
                            f"{resultado.get('peso_usado',0):.1f} kg · "
                            f"{resultado.get('pct_reps',0):.0f}% reps · "
                            f"RPE {resultado.get('rpe_promedio',0):.1f} · "
                            f"{decision_texto}"
                        )

    # --------------------------------------------------
    # PANTALLA: EDITAR PERFIL
    # --------------------------------------------------
    elif st.session_state.pantalla == "editar_perfil":

        st.title("✏️ Editar perfil")
        st.write("Actualiza tus datos. El historial de entrenamientos se conserva siempre.")

        if st.button("← Volver a la rutina"):
            st.session_state.pantalla = "rutina"
            st.rerun()

        st.divider()

        perfil_actual = st.session_state.perfil

        st.header("1️⃣ Datos personales")
        nombre_ed = st.text_input("Nombre", value=perfil_actual.get("nombre",""))
        col1, col2 = st.columns(2)
        with col1:
            edad_ed = st.number_input("Edad", min_value=16, max_value=70,
                                       value=int(perfil_actual.get("edad",25)))
        with col2:
            peso_ed = st.number_input("Peso (kg)", min_value=40.0, max_value=200.0,
                                       value=float(perfil_actual.get("peso",70.0)), step=0.5)
        st.divider()

        st.header("2️⃣ Género")
        opciones_genero = ["Hombre","Mujer","Prefiero no decirlo"]
        genero_actual   = perfil_actual.get("genero","Prefiero no decirlo")
        idx_genero      = opciones_genero.index(genero_actual) if genero_actual in opciones_genero else 0
        genero_ed = st.radio("Género:", options=opciones_genero, index=idx_genero,
                              label_visibility="collapsed", horizontal=True)
        if genero_ed != genero_actual:
            st.warning("⚠️ Cambiar el género modifica drásticamente la estructura de la rutina.")
        st.divider()

        st.header("3️⃣ Nivel de experiencia")
        opciones_nivel = ["Principiante — Menos de 6 meses","Intermedio — Entre 6 meses y 2 años","Avanzado — Más de 2 años"]
        nivel_actual   = perfil_actual.get("nivel_texto", opciones_nivel[0])
        idx_nivel      = opciones_nivel.index(nivel_actual) if nivel_actual in opciones_nivel else 0
        nivel_ed       = st.selectbox("Nivel:", options=opciones_nivel, index=idx_nivel)
        nivel_num_ed   = 1 if "Principiante" in nivel_ed else (2 if "Intermedio" in nivel_ed else 3)
        if nivel_ed != nivel_actual:
            st.warning("⚠️ Cambiar el nivel puede modificar los ejercicios y las técnicas avanzadas.")
        st.divider()

        st.header("4️⃣ Objetivo")
        opciones_objetivo = [
            "💪 Ganar músculo (hipertrofia)","🔥 Perder grasa (mantener músculo)",
            "🏋️ Ganar fuerza máxima","🏃 Mejorar condición física general"
        ]
        objetivo_actual = perfil_actual.get("objetivo", opciones_objetivo[0])
        idx_objetivo    = opciones_objetivo.index(objetivo_actual) if objetivo_actual in opciones_objetivo else 0
        objetivo_ed     = st.radio("Objetivo:", options=opciones_objetivo,
                                    index=idx_objetivo, label_visibility="collapsed")
        st.divider()

        st.header("5️⃣ Músculos prioritarios")
        opciones_musculos = {
            "🍑 Glúteos":"gluteos","🦵 Piernas":"piernas","🫁 Pecho":"pecho",
            "🔙 Espalda":"espalda","🥥 Hombros":"hombros","💪 Bíceps":"biceps",
            "🔱 Tríceps":"triceps","🎯 Deltoides medio":"deltoides_medio",
            "🦵 Cuádriceps":"cuadriceps","🔻 Femoral":"femoral",
        }
        musculos_inverso    = {v:k for k,v in opciones_musculos.items()}
        prioritarios_actual = perfil_actual.get("musculos_prioritarios",[])
        if isinstance(prioritarios_actual, str):
            try:
                prioritarios_actual = json.loads(prioritarios_actual)
            except Exception:
                prioritarios_actual = []
        default_musculos = [musculos_inverso[m] for m in prioritarios_actual if m in musculos_inverso]
        musculos_ed      = st.multiselect("Músculos prioritarios:", options=list(opciones_musculos.keys()),
                                           default=default_musculos)
        musculos_prioritarios_ed = [opciones_musculos[m] for m in musculos_ed]
        st.divider()

        st.header("6️⃣ Disponibilidad")
        dias_actual = int(perfil_actual.get("dias", 3))
        dias_ed     = st.select_slider("Días/semana", options=[1,2,3,4,5,6], value=dias_actual)
        minutos_ed  = st.selectbox("Tiempo por sesión", options=[30,45,60,90],
                                    index=[30,45,60,90].index(int(perfil_actual.get("minutos",60))),
                                    format_func=lambda x: f"{x} minutos")
        st.divider()

        st.header("7️⃣ Equipamiento")
        opciones_equip  = ["🏠 Sin equipamiento (solo peso corporal)","🏠 Tengo mancuernas en casa","🏢 Tengo acceso a un gimnasio completo"]
        equip_actual    = perfil_actual.get("equipamiento", opciones_equip[2])
        idx_equip       = opciones_equip.index(equip_actual) if equip_actual in opciones_equip else 2
        equipamiento_ed = st.radio("Equipamiento:", options=opciones_equip,
                                    index=idx_equip, label_visibility="collapsed")
        st.divider()

        st.header("8️⃣ Lesiones")
        lesiones_actual   = perfil_actual.get("lesiones","")
        tiene_lesiones_ed = st.toggle("¿Tienes alguna lesión actualmente?", value=bool(lesiones_actual))
        lesiones_ed = ""
        if tiene_lesiones_ed:
            lesiones_ed = st.text_area("Descríbela:", value=lesiones_actual,
                                        placeholder="Ejemplo: molestias en rodilla derecha")
        st.divider()

        cambio_critico    = (genero_ed != genero_actual or nivel_ed != nivel_actual)
        cambio_estructura = (dias_ed != int(perfil_actual.get("dias",3)) or
                             objetivo_ed != objetivo_actual or
                             equipamiento_ed != equip_actual)

        if st.button("💾 Guardar cambios", use_container_width=True, type="primary", disabled=not nombre_ed):
            perfil_nuevo = {
                "nombre":nombre_ed,"edad":edad_ed,"peso":peso_ed,"genero":genero_ed,
                "nivel_texto":nivel_ed,"nivel_num":nivel_num_ed,"objetivo":objetivo_ed,
                "musculos_prioritarios":musculos_prioritarios_ed,"dias":dias_ed,
                "minutos":minutos_ed,"equipamiento":equipamiento_ed,"lesiones":lesiones_ed
            }
            with st.spinner("Guardando cambios..."):
                nuevo_usuario_id = guardar_perfil(st.session_state.auth_user_id, perfil_nuevo)
            st.session_state.perfil     = perfil_nuevo
            st.session_state.usuario_id = nuevo_usuario_id

            if cambio_critico or cambio_estructura:
                st.session_state.perfil_pendiente_rutina = perfil_nuevo
                st.session_state.pantalla = "confirmar_rutina"
                st.rerun()
            else:
                st.success("✅ Perfil actualizado correctamente.")
                st.session_state.pantalla = "rutina"
                st.rerun()

    # --------------------------------------------------
    # PANTALLA: CONFIRMAR CAMBIO DE RUTINA
    # --------------------------------------------------
    elif st.session_state.pantalla == "confirmar_rutina":

        perfil_nuevo = st.session_state.get("perfil_pendiente_rutina", perfil)

        st.title("⚠️ Cambios importantes detectados")
        st.write("Has modificado campos que afectan significativamente tu rutina.")

        with st.container(border=True):
            st.subheader("📋 Resumen de cambios")
            if perfil_nuevo.get("genero") != perfil.get("genero"):
                st.write(f"• **Género:** {perfil.get('genero')} → {perfil_nuevo.get('genero')}")
            if perfil_nuevo.get("nivel_texto") != perfil.get("nivel_texto"):
                st.write(f"• **Nivel:** {perfil.get('nivel_texto')} → {perfil_nuevo.get('nivel_texto')}")
            if perfil_nuevo.get("objetivo") != perfil.get("objetivo"):
                st.write(f"• **Objetivo:** {perfil.get('objetivo')} → {perfil_nuevo.get('objetivo')}")
            if perfil_nuevo.get("dias") != perfil.get("dias"):
                st.write(f"• **Días/semana:** {perfil.get('dias')} → {perfil_nuevo.get('dias')}")
            if perfil_nuevo.get("equipamiento") != perfil.get("equipamiento"):
                st.write(f"• **Equipamiento:** cambiado")

        st.divider()
        st.subheader("¿Qué quieres hacer con tu rutina?")
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("### 🔄 Regenerar rutina")
                st.write("Se creará una rutina nueva. Tu **historial se conserva**.")
                if st.button("Regenerar rutina nueva →", use_container_width=True, type="primary"):
                    with st.spinner("Generando tu nueva rutina..."):
                        nueva_rutina = generar_rutina(perfil_nuevo)
                        guardar_rutina(st.session_state.usuario_id, nueva_rutina)
                        nuevo_bloque = crear_bloque_inicial()
                        guardar_bloque(st.session_state.usuario_id, nuevo_bloque)
                    st.session_state.rutina  = nueva_rutina
                    st.session_state.bloque  = nuevo_bloque
                    st.session_state.perfil  = perfil_nuevo
                    st.session_state.cambios_ejercicios = {}
                    if "perfil_pendiente_rutina" in st.session_state:
                        del st.session_state.perfil_pendiente_rutina
                    st.session_state.pantalla = "rutina"
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.markdown("### ➡️ Mantener rutina actual")
                st.write("Se actualizan tus datos pero se **mantiene la rutina actual**.")
                if st.button("Mantener rutina actual →", use_container_width=True):
                    st.session_state.perfil = perfil_nuevo
                    if "perfil_pendiente_rutina" in st.session_state:
                        del st.session_state.perfil_pendiente_rutina
                    st.session_state.pantalla = "rutina"
                    st.rerun()

    # --------------------------------------------------
    # PANTALLA: SESIÓN ACTIVA
    # --------------------------------------------------
    elif st.session_state.pantalla == "sesion":

        dia_nombre     = st.session_state.dia_seleccionado
        ejercicios_hoy = next(d["ejercicios"] for d in rutina_hoy["dias"] if d["dia"] == dia_nombre)
        enfoque_hoy    = next(d["enfoque"]    for d in rutina_hoy["dias"] if d["dia"] == dia_nombre)

        st.title("🏋️ Sesión de hoy")
        st.subheader(f"📅 {dia_nombre} — {enfoque_hoy}")
        st.info(f"**Fase: {fase_actual['nombre']}** · {fase_actual['series']} series · RPE objetivo {fase_actual['rpe_objetivo']}")

        with st.expander("❓ ¿Qué es el RPE?"):
            st.write("""
            - 🟢 **1–4:** Esfuerzo bajo
            - 🟠 **5–7:** Esfuerzo medio
            - 🔴 **8–10:** Esfuerzo alto
            """)

        st.divider()
        registros = {}

        for ejercicio in ejercicios_hoy:
            nombre_ej  = ejercicio["nombre"]
            peso_base  = ejercicio["peso_sugerido"] or 20.0
            num_series = ejercicio["series"]
            reps_obj   = rutina_hoy["reps_max"]
            tecnica    = ejercicio.get("tecnica")

            st.subheader(f"💪 {nombre_ej}")
            st.caption(f"Objetivo: {num_series} × {rutina_hoy['reps_min']}–{reps_obj} reps @ {peso_base} kg")

            if tecnica:
                st.warning(f"⚡ **{tecnica['nombre']} ({tecnica['abreviatura']}):** {tecnica['descripcion']}")

            series_del_ejercicio = []
            for i in range(1, num_series + 1):
                st.write(f"**Serie {i}**")
                col1, col2 = st.columns(2)
                with col1:
                    peso_real = st.number_input("Peso (kg)", min_value=0.0, max_value=500.0,
                                                value=float(peso_base), step=2.5, key=f"{nombre_ej}_peso_{i}")
                with col2:
                    reps_real = st.number_input("Reps", min_value=0, max_value=50,
                                                value=int(reps_obj), step=1, key=f"{nombre_ej}_reps_{i}")
                st.write("**Esfuerzo (RPE):**")
                rpe_real = selector_rpe(key=f"{nombre_ej}_s{i}", valor_defecto=fase_actual["rpe_objetivo"])
                series_del_ejercicio.append({"peso":peso_real,"reps":reps_real,"rpe":rpe_real})
                st.write("---")

            registros[nombre_ej] = {"series":series_del_ejercicio,"reps_objetivo":reps_obj}
            st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Volver"):
                st.session_state.pantalla = "rutina"
                st.rerun()
        with col2:
            if st.button("✅ Finalizar sesión →", use_container_width=True, type="primary"):
                registros_algoritmo = {n:d["series"] for n,d in registros.items()}
                resultados = analizar_sesion_completa(registros_algoritmo, rutina_hoy["reps_max"])

                with st.spinner("Guardando y analizando tu sesión..."):
                    guardar_sesion(st.session_state.usuario_id, dia_nombre, resultados)
                    rutina_actualizada = actualizar_pesos_rutina(st.session_state.usuario_id, resultados)
                    if rutina_actualizada:
                        st.session_state.rutina = rutina_actualizada
                    feedback = generar_feedback_sesion(perfil, resultados, fase_actual, info_semana)
                    st.session_state.feedback_ia = feedback

                    favoritos      = st.session_state.get("favoritos", [])
                    niveles_nuevos = []
                    subidas_nivel  = []
                    for resultado in resultados:
                        nombre_ej = resultado["ejercicio"]
                        if nombre_ej in favoritos:
                            nivel_nuevo = calcular_nivel_fuerza(
                                nombre_ej, perfil["peso"],
                                perfil.get("genero","Prefiero no decirlo"),
                                resultado["peso_usado"], int(rutina_hoy["reps_max"])
                            )
                            if nivel_nuevo:
                                niveles_nuevos.append({
                                    "ejercicio":nivel_nuevo["ejercicio"],
                                    "nivel":    nivel_nuevo["nivel"],
                                    "nivel_idx":nivel_nuevo["nivel_idx"],
                                    "percentil":nivel_nuevo["percentil"]
                                })
                                nivel_anterior = obtener_ultimo_nivel(st.session_state.usuario_id, nombre_ej)
                                if nivel_anterior and nivel_nuevo["nivel_idx"] > nivel_anterior.get("nivel_idx",0):
                                    subidas_nivel.append({
                                        "ejercicio":   nombre_ej,
                                        "nivel_nuevo": nivel_nuevo["nivel"],
                                        "percentil":   nivel_nuevo["percentil"]
                                    })
                    if niveles_nuevos:
                        guardar_niveles_sesion(st.session_state.usuario_id, niveles_nuevos)
                    st.session_state.subidas_nivel = subidas_nivel

                st.session_state.resultados_sesion = resultados
                st.session_state.pantalla = "resultados"
                st.rerun()

    # --------------------------------------------------
    # PANTALLA: RESULTADOS
    # --------------------------------------------------
    elif st.session_state.pantalla == "resultados":

        st.title("📊 Análisis de tu sesión")
        resultados = st.session_state.resultados_sesion

        subidas  = sum(1 for r in resultados if r["decision"] == "subir")
        bajadas  = sum(1 for r in resultados if r["decision"] == "bajar")
        mantiene = sum(1 for r in resultados if r["decision"] == "mantener")

        col1, col2, col3 = st.columns(3)
        col1.metric("⬆️ Suben",     subidas)
        col2.metric("➡️ Mantienen", mantiene)
        col3.metric("⬇️ Bajan",     bajadas)
        st.info(f"Semana {info_semana['semana_en_bloque']}/8 · Fase: {fase_actual['nombre']}")
        st.divider()

        feedback = st.session_state.get("feedback_ia")
        if feedback:
            with st.container(border=True):
                st.markdown("### 🤖 Tu entrenador IA")
                st.write(feedback)
            st.divider()

        for resultado in resultados:
            with st.container(border=True):
                st.markdown(f"### {resultado['emoji']} {resultado['ejercicio']}")
                col1, col2, col3 = st.columns(3)
                col1.metric("Peso usado",      f"{resultado['peso_usado']:.1f} kg")
                col2.metric("% Reps logradas", f"{resultado['pct_reps']:.0f}%")
                col3.metric("RPE promedio",     f"{resultado['rpe_promedio']:.1f}")
                if resultado["decision"] == "subir":
                    st.success(f"**Próxima sesión:** {resultado['mensaje']}")
                elif resultado["decision"] == "bajar":
                    st.warning(f"**Próxima sesión:** {resultado['mensaje']}")
                else:
                    st.info(f"**Próxima sesión:** {resultado['mensaje']}")

        st.divider()
        if subidas > bajadas:
            st.balloons()
            st.success("🎉 ¡Gran sesión!")
        elif bajadas > subidas:
            st.warning("💪 Sesión exigente. La IA ajustó los pesos.")
        else:
            st.info("✅ Sesión sólida.")

        if st.button("← Volver a mi rutina", use_container_width=True, type="primary"):
            st.session_state.pantalla          = "rutina"
            st.session_state.resultados_sesion = []
            st.session_state.feedback_ia       = None
            st.rerun()

    # --------------------------------------------------
    # PANTALLA: RANKING GLOBAL
    # --------------------------------------------------
    elif st.session_state.pantalla == "ranking":

        st.title("🏆 Tu Ranking Global")
        st.write("Compara tu fuerza con la comunidad mundial de levantadores.")

        if st.button("← Volver a la rutina"):
            st.session_state.pantalla = "rutina"
            st.rerun()

        st.divider()
        st.subheader("⭐ Mis ejercicios favoritos")
        st.caption("Selecciona los ejercicios que quieres seguir en el ranking.")

        ejercicios_disponibles = ejercicios_con_standard()
        favoritos_actuales     = st.session_state.get("favoritos", [])
        favoritos_nuevos = st.multiselect("Elige tus ejercicios favoritos:",
                                           options=ejercicios_disponibles, default=favoritos_actuales)
        if favoritos_nuevos != favoritos_actuales:
            guardar_favoritos(st.session_state.usuario_id, favoritos_nuevos)
            st.session_state.favoritos = favoritos_nuevos
            st.success("✅ Favoritos actualizados")

        st.divider()

        if not favoritos_nuevos:
            st.info("Selecciona al menos un ejercicio favorito para ver tu ranking.")
        else:
            st.subheader("📊 Tu posición actual")
            progreso = obtener_progreso_por_ejercicio(st.session_state.usuario_id)
            for ejercicio_fav in favoritos_nuevos:
                st.markdown(f"#### 🏋️ {ejercicio_fav}")
                datos_ejercicio = progreso.get(ejercicio_fav, [])
                if not datos_ejercicio:
                    st.caption("Aún no tienes sesiones registradas con este ejercicio.")
                    st.divider()
                    continue
                ultimo_dato     = datos_ejercicio[-1]
                nivel_resultado = calcular_nivel_fuerza(
                    ejercicio_fav, perfil["peso"],
                    perfil.get("genero","Prefiero no decirlo"),
                    ultimo_dato["peso_usado"], rutina["reps_max"]
                )
                if nivel_resultado:
                    st.caption(f"Basado en: {ultimo_dato['peso_usado']} kg × {rutina['reps_max']} reps")
                    mostrar_nivel_fuerza(nivel_resultado)
                else:
                    st.caption("No hay estándares disponibles para este ejercicio.")
                st.divider()

    # --------------------------------------------------
    # PANTALLA: RESUMEN DEL BLOQUE
    # --------------------------------------------------
    elif st.session_state.pantalla == "resumen_bloque":

        st.title(f"📊 Bloque {info_semana['numero_bloque']}")
        st.write(f"Iniciado el **{bloque['fecha_inicio']}** · Semana actual: **{info_semana['semana_en_bloque']} de 8**")

        if st.button("← Volver a la rutina"):
            st.session_state.pantalla = "rutina"
            st.rerun()

        st.divider()
        st.subheader("🗓️ Fases del bloque")

        for fase in [
            {"nombre":"Adaptación",     "semanas":"1–2","series":3,"rpe":7},
            {"nombre":"Acumulación",    "semanas":"3–5","series":4,"rpe":8},
            {"nombre":"Intensificación","semanas":"6–7","series":4,"rpe":9},
            {"nombre":"Deload",         "semanas":"8",  "series":2,"rpe":6},
        ]:
            es_actual = fase["nombre"] == fase_actual["nombre"]
            with st.container(border=True):
                col_f1, col_f2, col_f3, col_f4 = st.columns([2,1,1,1])
                with col_f1:
                    st.markdown(f"**▶️ {fase['nombre']}**") if es_actual else st.write(fase["nombre"])
                    st.caption(f"Semanas {fase['semanas']}")
                with col_f2:
                    st.metric("Series", fase["series"])
                with col_f3:
                    st.metric("RPE obj.", fase["rpe"])
                with col_f4:
                    if es_actual: st.success("ACTUAL")

        st.divider()
        st.subheader("📈 Estadísticas del bloque actual")
        historial = obtener_historial_sesiones(st.session_state.usuario_id, limite=50)
        resumen   = generar_resumen_bloque(historial, info_semana["numero_bloque"])

        if resumen:
            col1, col2, col3 = st.columns(3)
            col1.metric("Sesiones completadas",   resumen["total_sesiones"])
            col2.metric("Ejercicios que subieron", resumen["ejercicios_subidos"])
            col3.metric("% de progreso",           f"{resumen['pct_progreso']:.0f}%")
        else:
            st.info("Completa tu primera sesión para ver las estadísticas del bloque.")

    # --------------------------------------------------
    # PANTALLA: PROGRESO
    # --------------------------------------------------
    elif st.session_state.pantalla == "progreso":

        st.title("📈 Tu progreso")
        st.write("Evolución de tus pesos a lo largo de las sesiones.")

        if st.button("← Volver a la rutina"):
            st.session_state.pantalla = "rutina"
            st.rerun()

        st.divider()

        with st.spinner("Cargando historial..."):
            progreso = obtener_progreso_por_ejercicio(st.session_state.usuario_id)

        if not progreso:
            st.info("Completa tu primera sesión para ver tu progreso aquí.")
        else:
            ejercicios_disponibles = list(progreso.keys())
            ejercicio_elegido = st.selectbox("Selecciona un ejercicio:", ejercicios_disponibles)
            datos_ejercicio   = progreso[ejercicio_elegido]

            if len(datos_ejercicio) < 2:
                st.info(f"Necesitas al menos 2 sesiones de **{ejercicio_elegido}** para ver la gráfica.")
            else:
                df = pd.DataFrame({
                    "Sesión":         [d["sesion"]    for d in datos_ejercicio],
                    "Fecha":          [d["fecha"]      for d in datos_ejercicio],
                    "Peso usado":     [d["peso_usado"] for d in datos_ejercicio],
                    "Peso siguiente": [d["nuevo_peso"] for d in datos_ejercicio]
                })
                st.subheader(f"📊 {ejercicio_elegido}")
                st.line_chart(df.set_index("Sesión")[["Peso usado","Peso siguiente"]])

                peso_inicial = datos_ejercicio[0]["peso_usado"]
                peso_actual  = datos_ejercicio[-1]["peso_usado"]
                diferencia   = peso_actual - peso_inicial

                if diferencia > 0:
                    pct = (diferencia / peso_inicial) * 100
                    st.success(f"✅ Has subido **{diferencia:.1f} kg** en {len(datos_ejercicio)} sesiones (+{pct:.0f}%)")
                elif diferencia < 0:
                    st.warning(f"📉 El peso bajó {abs(diferencia):.1f} kg.")
                else:
                    st.info("➡️ Peso estable.")

                st.divider()
                st.subheader("📋 Detalle por sesión")
                st.dataframe(df, use_container_width=True, hide_index=True)

            st.divider()
            st.subheader("🏆 Resumen global")
            filas = []
            for nombre_ej, datos in progreso.items():
                if datos:
                    inicial   = datos[0]["peso_usado"]
                    actual    = datos[-1]["peso_usado"]
                    diff      = actual - inicial
                    if inicial > 0:
                        pct       = (diff / inicial) * 100
                        tendencia = "⬆️" if diff > 0 else ("⬇️" if diff < 0 else "➡️")
                        filas.append({
                            "Ejercicio":nombre_ej,"Inicial":f"{inicial} kg","Actual":f"{actual} kg",
                            "Cambio":f"{diff:+.1f} kg","% Cambio":f"{pct:+.0f}%",
                            "Sesiones":len(datos),"Tendencia":tendencia
                        })
            if filas:
                st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)
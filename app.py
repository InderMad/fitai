# app.py
import streamlit as st
from generador_rutinas import generar_rutina
from algoritmo_ia import analizar_sesion_completa
from database import (
    guardar_usuario, buscar_usuario_por_nombre,
    guardar_rutina, obtener_rutina,
    guardar_sesion, obtener_historial_sesiones
)

# =====================================================
# CONFIGURACIÓN
# =====================================================
st.set_page_config(
    page_title="FitAI - Tu entrenador inteligente",
    page_icon="🏋️",
    layout="centered"
)

# =====================================================
# INICIALIZAR SESSION STATE
# =====================================================
if "perfil_guardado" not in st.session_state:
    st.session_state.perfil_guardado = False
if "perfil" not in st.session_state:
    st.session_state.perfil = {}
if "usuario_id" not in st.session_state:
    st.session_state.usuario_id = None
if "rutina" not in st.session_state:
    st.session_state.rutina = None
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "rutina"
if "resultados_sesion" not in st.session_state:
    st.session_state.resultados_sesion = []
if "dia_seleccionado" not in st.session_state:
    st.session_state.dia_seleccionado = None


# =====================================================
# PANTALLA 1: FORMULARIO DE PERFIL
# =====================================================
if not st.session_state.perfil_guardado:

    st.title("🏋️ Crea tu perfil de entrenamiento")
    st.write("Responde estas preguntas con sinceridad. Cuanto más precisas sean, mejor será tu rutina.")

    # --- Opción de recuperar perfil existente ---
    st.info("💡 ¿Ya tienes perfil? Escribe tu nombre y lo recuperamos automáticamente.")
    nombre_recuperar = st.text_input("Nombre para recuperar perfil existente:",
                                      placeholder="Escribe tu nombre y pulsa Enter")

    if nombre_recuperar:
        usuario_existente = buscar_usuario_por_nombre(nombre_recuperar)
        if usuario_existente:
            if st.button(f"✅ Recuperar perfil de {nombre_recuperar}"):
                rutina_guardada = obtener_rutina(usuario_existente["id"])
                if rutina_guardada:
                    st.session_state.perfil      = usuario_existente
                    st.session_state.usuario_id  = usuario_existente["id"]
                    st.session_state.rutina      = rutina_guardada
                    st.session_state.perfil_guardado = True
                    st.rerun()
                else:
                    st.warning("Perfil encontrado pero sin rutina. Crea una nueva abajo.")
        else:
            st.caption("No se encontró ese nombre. Crea tu perfil nuevo abajo.")

    st.divider()
    st.subheader("➕ Crear perfil nuevo")

    st.header("1️⃣ Datos personales")
    nombre = st.text_input("¿Cómo te llamas?", placeholder="Escribe tu nombre aquí")
    col1, col2 = st.columns(2)
    with col1:
        edad = st.number_input("Tu edad", min_value=16, max_value=70, value=25)
    with col2:
        peso = st.number_input("Tu peso (kg)", min_value=40.0, max_value=200.0, value=70.0, step=0.5)
    st.divider()

    st.header("2️⃣ Tu experiencia en el gimnasio")
    nivel_texto = st.selectbox("¿Cuánto tiempo llevas entrenando?", options=[
        "Principiante — Menos de 6 meses",
        "Intermedio — Entre 6 meses y 2 años",
        "Avanzado — Más de 2 años"
    ])
    nivel_num = 1 if "Principiante" in nivel_texto else (2 if "Intermedio" in nivel_texto else 3)
    st.divider()

    st.header("3️⃣ Tu objetivo principal")
    objetivo = st.radio("Objetivo:", options=[
        "💪 Ganar músculo (hipertrofia)",
        "🔥 Perder grasa (mantener músculo)",
        "🏋️ Ganar fuerza máxima",
        "🏃 Mejorar condición física general"
    ], label_visibility="collapsed")
    st.divider()

    st.header("4️⃣ Tu disponibilidad semanal")
    dias = st.select_slider("¿Cuántos días a la semana?", options=[2,3,4,5,6], value=3)
    if dias <= 3:
        st.info("💡 Haremos rutinas Fullbody.")
    elif dias == 4:
        st.info("💡 Haremos Torso/Pierna.")
    else:
        st.info("💡 Haremos Push/Pull/Legs.")
    minutos = st.selectbox("¿Cuánto tiempo por sesión?", options=[30,45,60,90],
                           index=2, format_func=lambda x: f"{x} minutos")
    st.divider()

    st.header("5️⃣ Tu equipamiento")
    equipamiento = st.radio("¿Con qué equipamiento cuentas?", options=[
        "🏠 Sin equipamiento (solo peso corporal)",
        "🏠 Tengo mancuernas en casa",
        "🏢 Tengo acceso a un gimnasio completo"
    ])
    st.divider()

    st.header("6️⃣ Lesiones o limitaciones")
    tiene_lesiones = st.toggle("¿Tienes alguna lesión actualmente?")
    lesiones_texto = ""
    if tiene_lesiones:
        lesiones_texto = st.text_area("Descríbela:", placeholder="Ejemplo: molestias en rodilla derecha")
    st.divider()

    boton_guardar = st.button("Guardar perfil y generar mi rutina →",
                               disabled=not nombre,
                               use_container_width=True,
                               type="primary")
    if boton_guardar:
        perfil = {
            "nombre": nombre, "edad": edad, "peso": peso,
            "nivel_texto": nivel_texto, "nivel_num": nivel_num,
            "objetivo": objetivo, "dias": dias, "minutos": minutos,
            "equipamiento": equipamiento, "lesiones": lesiones_texto
        }

        with st.spinner("Guardando tu perfil..."):
            # Guardar en Supabase y obtener el ID
            usuario_id = guardar_usuario(perfil)
            rutina     = generar_rutina(perfil)
            guardar_rutina(usuario_id, rutina)

        st.session_state.perfil          = perfil
        st.session_state.usuario_id      = usuario_id
        st.session_state.rutina          = rutina
        st.session_state.perfil_guardado = True
        st.session_state.pantalla        = "rutina"
        st.rerun()


# =====================================================
# PANTALLAS PRINCIPALES
# =====================================================
else:
    perfil = st.session_state.perfil
    rutina = st.session_state.rutina

    # --------------------------------------------------
    # PANTALLA 2: VISTA DE RUTINA
    # --------------------------------------------------
    if st.session_state.pantalla == "rutina":

        st.title(f"💪 Tu rutina, {perfil['nombre']}")
        st.success("Rutina cargada correctamente.")

        nombres_estructura = {
            "fullbody":       "Fullbody",
            "torso_pierna":   "Torso / Pierna",
            "push_pull_legs": "Push / Pull / Legs"
        }
        nombre_estructura = nombres_estructura.get(rutina["estructura"], rutina["estructura"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Series",       f"{rutina['series']} series")
        col2.metric("Repeticiones", f"{rutina['reps_min']}–{rutina['reps_max']} reps")
        col3.metric("Descanso",     f"{rutina['descanso_seg']}s")
        st.markdown(f"**Tipo de rutina:** {nombre_estructura}")
        st.divider()

        st.subheader("📋 ¿Listo para entrenar hoy?")
        opciones_dias = [d["dia"] for d in rutina["dias"]]
        dia_elegido   = st.selectbox("¿Qué día entrenas hoy?", opciones_dias)

        if st.button("🏋️ Empezar sesión de hoy →", use_container_width=True, type="primary"):
            st.session_state.dia_seleccionado = dia_elegido
            st.session_state.pantalla = "sesion"
            st.rerun()

        st.divider()

        # Historial de sesiones anteriores
        if st.session_state.usuario_id:
            historial = obtener_historial_sesiones(st.session_state.usuario_id, limite=5)
            if historial:
                st.subheader("📈 Tus últimas sesiones")
                for sesion in historial:
                    with st.expander(f"📅 {sesion['fecha']} — {sesion['dia']}"):
                        for resultado in sesion["resultados"]:
                            emoji = resultado.get("emoji", "➡️")
                            st.write(f"{emoji} **{resultado['ejercicio']}** → {resultado['nuevo_peso']} kg")

        st.divider()

        st.subheader("📅 Tu rutina completa")
        for dia in rutina["dias"]:
            with st.expander(f"📅 {dia['dia']} — {dia['enfoque']}"):
                for i, ejercicio in enumerate(dia["ejercicios"], 1):
                    peso_texto = f"{ejercicio['peso_sugerido']} kg" if ejercicio["peso_sugerido"] else "Peso corporal"
                    with st.container(border=True):
                        col_num, col_info, col_peso = st.columns([0.5, 3, 2])
                        with col_num:
                            st.markdown(f"### {i}")
                        with col_info:
                            st.markdown(f"**{ejercicio['nombre']}**")
                            st.caption(f"Grupo: {ejercicio['grupo'].capitalize()}")
                        with col_peso:
                            st.markdown(f"**{ejercicio['series']} × {ejercicio['reps_min']}–{ejercicio['reps_max']} reps**")
                            st.markdown(f"📦 {peso_texto}")

        if st.button("← Modificar perfil y regenerar"):
            st.session_state.perfil_guardado = False
            st.session_state.rutina = None
            st.session_state.pantalla = "rutina"
            st.rerun()

    # --------------------------------------------------
    # PANTALLA 3: SESIÓN ACTIVA
    # --------------------------------------------------
    elif st.session_state.pantalla == "sesion":

        dia_nombre    = st.session_state.dia_seleccionado
        ejercicios_hoy = next(d["ejercicios"] for d in rutina["dias"] if d["dia"] == dia_nombre)
        enfoque_hoy    = next(d["enfoque"]    for d in rutina["dias"] if d["dia"] == dia_nombre)

        st.title("🏋️ Sesión de hoy")
        st.subheader(f"📅 {dia_nombre} — {enfoque_hoy}")
        st.write("Registra el peso, repeticiones y esfuerzo de cada serie.")

        with st.expander("❓ ¿Qué es el RPE?"):
            st.write("""
            El **RPE** (Esfuerzo Percibido) es una escala del 1 al 10:
            - **1–5:** Muy fácil, podría hacer muchas más repeticiones
            - **6–7:** Moderado, me quedan 3–4 repeticiones en el tanque
            - **8:** Difícil, me quedan 1–2 repeticiones
            - **9:** Casi al límite, podría hacer 1 repetición más
            - **10:** Fallo total, no puedo hacer ni una más

            **Objetivo ideal:** RPE 7–8 en las últimas series.
            """)

        st.divider()

        registros = {}

        for ejercicio in ejercicios_hoy:
            nombre_ej  = ejercicio["nombre"]
            peso_base  = ejercicio["peso_sugerido"] or 20.0
            num_series = ejercicio["series"]
            reps_obj   = ejercicio["reps_max"]

            st.subheader(f"💪 {nombre_ej}")
            st.caption(f"Objetivo: {num_series} series × {ejercicio['reps_min']}–{reps_obj} reps @ {peso_base} kg sugerido")

            series_del_ejercicio = []

            for i in range(1, num_series + 1):
                st.write(f"**Serie {i}**")
                col1, col2, col3 = st.columns(3)

                with col1:
                    peso_real = st.number_input(
                        "Peso (kg)", min_value=0.0, max_value=500.0,
                        value=float(peso_base), step=2.5,
                        key=f"{nombre_ej}_peso_{i}"
                    )
                with col2:
                    reps_real = st.number_input(
                        "Reps", min_value=0, max_value=50,
                        value=int(reps_obj), step=1,
                        key=f"{nombre_ej}_reps_{i}"
                    )
                with col3:
                    rpe_real = st.select_slider(
                        "RPE", options=[1,2,3,4,5,6,7,8,9,10],
                        value=7, key=f"{nombre_ej}_rpe_{i}"
                    )

                series_del_ejercicio.append({
                    "peso": peso_real, "reps": reps_real, "rpe": rpe_real
                })

            registros[nombre_ej] = {
                "series": series_del_ejercicio,
                "reps_objetivo": reps_obj
            }
            st.divider()

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("← Volver a la rutina"):
                st.session_state.pantalla = "rutina"
                st.rerun()

        with col_btn2:
            if st.button("✅ Finalizar sesión →", use_container_width=True, type="primary"):

                registros_para_algoritmo = {
                    nombre: datos["series"]
                    for nombre, datos in registros.items()
                }

                resultados = analizar_sesion_completa(
                    registros_para_algoritmo,
                    rutina["reps_max"]
                )

                # Guardar sesión en Supabase
                with st.spinner("Guardando sesión..."):
                    guardar_sesion(
                        st.session_state.usuario_id,
                        dia_nombre,
                        resultados
                    )

                st.session_state.resultados_sesion = resultados
                st.session_state.pantalla = "resultados"
                st.rerun()

    # --------------------------------------------------
    # PANTALLA 4: RESULTADOS
    # --------------------------------------------------
    elif st.session_state.pantalla == "resultados":

        st.title("📊 Análisis de tu sesión")
        st.write("Esto es lo que ha decidido la IA para tu próxima sesión:")

        resultados = st.session_state.resultados_sesion

        subidas  = sum(1 for r in resultados if r["decision"] == "subir")
        bajadas  = sum(1 for r in resultados if r["decision"] == "bajar")
        mantiene = sum(1 for r in resultados if r["decision"] == "mantener")

        col1, col2, col3 = st.columns(3)
        col1.metric("⬆️ Suben de peso",  subidas)
        col2.metric("➡️ Se mantienen",   mantiene)
        col3.metric("⬇️ Bajan de peso",  bajadas)

        st.divider()

        for resultado in resultados:
            with st.container(border=True):
                st.markdown(f"### {resultado['emoji']} {resultado['ejercicio']}")

                col1, col2, col3 = st.columns(3)
                col1.metric("Peso usado",       f"{resultado['peso_usado']:.1f} kg")
                col2.metric("% Reps logradas",  f"{resultado['pct_reps']:.0f}%")
                col3.metric("RPE promedio",      f"{resultado['rpe_promedio']:.1f}")

                if resultado["decision"] == "subir":
                    st.success(f"**Próxima sesión:** {resultado['mensaje']}")
                elif resultado["decision"] == "bajar":
                    st.warning(f"**Próxima sesión:** {resultado['mensaje']}")
                else:
                    st.info(f"**Próxima sesión:** {resultado['mensaje']}")

        st.divider()

        if subidas > bajadas:
            st.balloons()
            st.success("🎉 ¡Gran sesión! Estás progresando en la mayoría de ejercicios.")
        elif bajadas > subidas:
            st.warning("💪 Sesión exigente. La IA ha ajustado los pesos para la próxima.")
        else:
            st.info("✅ Sesión sólida. Mantén la consistencia.")

        if st.button("← Volver a mi rutina", use_container_width=True, type="primary"):
            st.session_state.pantalla = "rutina"
            st.session_state.resultados_sesion = []
            st.rerun()
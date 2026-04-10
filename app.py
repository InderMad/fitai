# app.py
import streamlit as st
from generador_rutinas import generar_rutina
from algoritmo_ia import analizar_sesion_completa

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
if "rutina" not in st.session_state:
    st.session_state.rutina = None
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "rutina"   # puede ser: "rutina", "sesion", "resultados"
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

    st.header("1️⃣ Datos personales")
    nombre = st.text_input("¿Cómo te llamas?", placeholder="Escribe tu nombre aquí")
    col1, col2 = st.columns(2)
    with col1:
        edad = st.number_input("Tu edad", min_value=16, max_value=70, value=25)
    with col2:
        peso = st.number_input("Tu peso (kg)", min_value=40.0, max_value=200.0, value=70.0, step=0.5)
    st.divider()

    st.header("2️⃣ Tu experiencia en el gimnasio")
    nivel_texto = st.selectbox("¿Cuánto tiempo llevas entrenando de forma consistente?", options=[
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
    dias = st.select_slider("¿Cuántos días a la semana puedes entrenar?", options=[2,3,4,5,6], value=3)
    if dias <= 3:
        st.info("💡 Haremos rutinas Fullbody — ideal para tu frecuencia.")
    elif dias == 4:
        st.info("💡 Haremos Torso/Pierna — buen equilibrio volumen/recuperación.")
    else:
        st.info("💡 Haremos Push/Pull/Legs — máxima especialización por grupo muscular.")
    minutos = st.selectbox("¿Cuánto tiempo tienes por sesión?", options=[30,45,60,90],
                           index=2, format_func=lambda x: f"{x} minutos")
    st.divider()

    st.header("5️⃣ Tu equipamiento disponible")
    equipamiento = st.radio("¿Con qué equipamiento cuentas?", options=[
        "🏠 Sin equipamiento (solo peso corporal)",
        "🏠 Tengo mancuernas en casa",
        "🏢 Tengo acceso a un gimnasio completo"
    ])
    st.divider()

    st.header("6️⃣ Lesiones o limitaciones")
    tiene_lesiones = st.toggle("¿Tienes alguna lesión o limitación física actualmente?")
    lesiones_texto = ""
    if tiene_lesiones:
        lesiones_texto = st.text_area("Descríbela brevemente:", placeholder="Ejemplo: molestias en rodilla derecha")
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
        st.session_state.perfil          = perfil
        st.session_state.rutina          = generar_rutina(perfil)
        st.session_state.perfil_guardado = True
        st.session_state.pantalla        = "rutina"
        st.rerun()


# =====================================================
# PANTALLAS PRINCIPALES (una vez el perfil está guardado)
# =====================================================
else:
    perfil = st.session_state.perfil
    rutina = st.session_state.rutina

    # --------------------------------------------------
    # PANTALLA 2: VISTA DE RUTINA COMPLETA
    # --------------------------------------------------
    if st.session_state.pantalla == "rutina":

        st.title(f"💪 Tu rutina, {perfil['nombre']}")
        st.success("Rutina generada correctamente según tu perfil.")

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

        # Botón para ir a registrar una sesión
        st.subheader("📋 ¿Listo para entrenar hoy?")
        st.write("Selecciona el día de hoy y empieza a registrar tu sesión:")

        opciones_dias = [d["dia"] for d in rutina["dias"]]
        dia_elegido = st.selectbox("¿Qué día entrenas hoy?", opciones_dias)

        if st.button("🏋️ Empezar sesión de hoy →", use_container_width=True, type="primary"):
            st.session_state.dia_seleccionado = dia_elegido
            st.session_state.pantalla = "sesion"
            st.rerun()

        st.divider()

        # Mostrar la rutina completa debajo
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

        dia_nombre = st.session_state.dia_seleccionado

        # Encontrar los ejercicios del día seleccionado
        ejercicios_hoy = next(
            d["ejercicios"] for d in rutina["dias"] if d["dia"] == dia_nombre
        )
        enfoque_hoy = next(
            d["enfoque"] for d in rutina["dias"] if d["dia"] == dia_nombre
        )

        st.title(f"🏋️ Sesión de hoy")
        st.subheader(f"📅 {dia_nombre} — {enfoque_hoy}")
        st.write("Registra el peso, repeticiones y esfuerzo de cada serie.")

        # Explicación del RPE para que el usuario sepa qué marcar
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

        # Diccionario donde guardaremos los registros de esta sesión
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
                        "Peso (kg)",
                        min_value=0.0,
                        max_value=500.0,
                        value=float(peso_base),
                        step=2.5,
                        key=f"{nombre_ej}_peso_{i}",
                        label_visibility="visible"
                    )
                with col2:
                    reps_real = st.number_input(
                        "Reps",
                        min_value=0,
                        max_value=50,
                        value=int(reps_obj),
                        step=1,
                        key=f"{nombre_ej}_reps_{i}"
                    )
                with col3:
                    rpe_real = st.select_slider(
                        "RPE",
                        options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        value=7,
                        key=f"{nombre_ej}_rpe_{i}"
                    )

                series_del_ejercicio.append({
                    "peso": peso_real,
                    "reps": reps_real,
                    "rpe":  rpe_real
                })

            registros[nombre_ej] = {
                "series":       series_del_ejercicio,
                "reps_objetivo": reps_obj
            }

            st.divider()

        # Botones de acción
        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("← Volver a la rutina"):
                st.session_state.pantalla = "rutina"
                st.rerun()

        with col_btn2:
            if st.button("✅ Finalizar sesión y ver análisis →",
                         use_container_width=True, type="primary"):

                # Preparar los datos en el formato que espera el algoritmo
                registros_para_algoritmo = {
                    nombre: datos["series"]
                    for nombre, datos in registros.items()
                }

                # Ejecutar el algoritmo de IA
                resultados = analizar_sesion_completa(
                    registros_para_algoritmo,
                    rutina["reps_max"]
                )

                # Guardar resultados y cambiar de pantalla
                st.session_state.resultados_sesion = resultados
                st.session_state.pantalla = "resultados"
                st.rerun()

    # --------------------------------------------------
    # PANTALLA 4: RESULTADOS Y ANÁLISIS DE LA IA
    # --------------------------------------------------
    elif st.session_state.pantalla == "resultados":

        st.title("📊 Análisis de tu sesión")
        st.write("Esto es lo que ha decidido la IA para tu próxima sesión:")

        resultados = st.session_state.resultados_sesion

        # Contadores para el resumen
        subidas  = sum(1 for r in resultados if r["decision"] == "subir")
        bajadas  = sum(1 for r in resultados if r["decision"] == "bajar")
        mantiene = sum(1 for r in resultados if r["decision"] == "mantener")

        # Resumen rápido en métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("⬆️ Suben de peso",    subidas)
        col2.metric("➡️ Se mantienen",     mantiene)
        col3.metric("⬇️ Bajan de peso",    bajadas)

        st.divider()

        # Detalle por ejercicio
        for resultado in resultados:
            color_map = {
                "green":  "🟢",
                "blue":   "🔵",
                "orange": "🟠"
            }
            icono_color = color_map.get(resultado["color"], "⚪")

            with st.container(border=True):
                st.markdown(f"### {resultado['emoji']} {resultado['ejercicio']}")

                col1, col2, col3 = st.columns(3)
                col1.metric("Peso usado",      f"{resultado['peso_usado']:.1f} kg")
                col2.metric("% Reps logradas", f"{resultado['pct_reps']:.0f}%")
                col3.metric("RPE promedio",     f"{resultado['rpe_promedio']:.1f}")

                # El mensaje explicativo de la decisión
                if resultado["decision"] == "subir":
                    st.success(f"**Próxima sesión:** {resultado['mensaje']}")
                elif resultado["decision"] == "bajar":
                    st.warning(f"**Próxima sesión:** {resultado['mensaje']}")
                else:
                    st.info(f"**Próxima sesión:** {resultado['mensaje']}")

        st.divider()

        # Mensaje motivacional global
        if subidas > bajadas:
            st.balloons()
            st.success("🎉 ¡Gran sesión! Estás progresando en la mayoría de ejercicios.")
        elif bajadas > subidas:
            st.warning("💪 Sesión exigente. La IA ha ajustado los pesos para que la próxima sea más productiva.")
        else:
            st.info("✅ Sesión sólida. Mantén la consistencia y los resultados llegarán.")

        st.divider()

        # Botón para volver
        if st.button("← Volver a mi rutina", use_container_width=True, type="primary"):
            st.session_state.pantalla = "rutina"
            st.session_state.resultados_sesion = []
            st.rerun()
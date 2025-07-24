import streamlit as st
import json
import random
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Test Interactivo", layout="centered")

# Archivos disponibles
CATEGORIAS = {
    "Programación": "preguntas/Programacion.json",
    "Ciberseguridad": "preguntas/Ciberseguridad.json",
    "Redes": "preguntas/Redes.json",
    "Base de Datos": "preguntas/BDD.json",
    "Cultura General (Informática)": "preguntas/Cultura.json",
    "Todas mezcladas": "preguntas/Todas.json"
}

@st.cache_data
def cargar_preguntas(path_json):
    with open(path_json, "r", encoding="utf-8") as f:
        preguntas = json.load(f)
    return preguntas

# Inicializar estados
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.correctas = 0
    st.session_state.respondidas = []
    st.session_state.preguntas = []
    st.session_state.opciones_preguntas = {}
    st.session_state.test_iniciado = False

# Interfaz de selección
st.markdown("<h1 style='text-align: center;'>🧠 Test Interactivo</h1>", unsafe_allow_html=True)
st.markdown("---")

if not st.session_state.test_iniciado:
    categoria = st.selectbox("📂 Selecciona una categoría", list(CATEGORIAS.keys()))
    archivo = CATEGORIAS[categoria]
    preguntas = cargar_preguntas(archivo)
    total_disponibles = len(preguntas)
    cantidad = st.slider(f"🔢 ¿Cuántas preguntas deseas responder? (de {total_disponibles})", 1, total_disponibles, 10)

    if st.button("🎯 Empezar Test"):
        seleccionadas = random.sample(preguntas, cantidad)
        st.session_state.preguntas = seleccionadas
        st.session_state.test_iniciado = True
        st.rerun()

# Mostrar preguntas
if st.session_state.test_iniciado:
    preguntas = st.session_state.preguntas
    total = len(preguntas)

    if st.session_state.indice < total:
        i = st.session_state.indice
        actual = preguntas[i]
        clave = actual["pregunta"]

        if clave not in st.session_state.opciones_preguntas:
            opciones = actual["opciones"].copy()
            random.shuffle(opciones)
            st.session_state.opciones_preguntas[clave] = opciones
        else:
            opciones = st.session_state.opciones_preguntas[clave]

        st.info(f"**Pregunta {i + 1} de {total}**  |  **Nivel:** {actual['nivel']}")
        seleccion = st.radio(actual["pregunta"], opciones, key=f"radio_{i}")

        if st.button("Responder", key=f"boton_{i}"):
            correcta = actual["respuesta"]
            if seleccion == correcta:
                st.success("✅ ¡Correcto!")
                st.session_state.correctas += 1
            else:
                st.error(f"❌ Incorrecto. La respuesta correcta era: **{correcta}**")

            st.session_state.respondidas.append({
                "Pregunta": actual["pregunta"],
                "Tu respuesta": seleccion,
                "Correcta": correcta,
                "Resultado": "✅" if seleccion == correcta else "❌"
            })

            st.session_state.indice += 1
            st.rerun()
    else:
        st.balloons()
        st.success("🎉 ¡Has terminado el test!")
        st.write(f"**Puntaje final:** {st.session_state.correctas} / {total} ({round(st.session_state.correctas / total * 100)}%)")
        st.progress(st.session_state.correctas / total)

        st.markdown("### 📋 Resultados detallados")
        df = pd.DataFrame(st.session_state.respondidas)
        st.dataframe(df, use_container_width=True)

        json_resultado = json.dumps(st.session_state.respondidas, indent=2)
        st.download_button("📥 Descargar reporte JSON", data=json_resultado, file_name="resultados_test.json", mime="application/json")

        if st.button("🔄 Reiniciar test"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

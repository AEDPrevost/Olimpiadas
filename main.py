import streamlit as st
import json
import random
import pandas as pd

st.set_page_config(page_title="Test de Programación", layout="centered")

# Carga y baraja preguntas
@st.cache_data
def cargar_preguntas(ruta_json):
    preguntas = json.load(ruta_json)
    return preguntas

# Inicialización
if "preguntas_seleccionadas" not in st.session_state:
    st.session_state.preguntas_seleccionadas = []
    st.session_state.indice = 0
    st.session_state.correctas = 0
    st.session_state.respondidas = []
    st.session_state.opciones_preguntas = {}

# Estilo general
st.markdown("<h1 style='text-align: center;'>🧠 Test de Programación</h1>", unsafe_allow_html=True)
st.markdown("---")

archivo = st.file_uploader("📂 Sube tu archivo de preguntas (.json)", type=["json"])

if archivo:
    todas = cargar_preguntas(archivo)
    total_disponibles = len(todas)
    
    if not st.session_state.preguntas_seleccionadas:
        st.success(f"✅ Archivo cargado correctamente con {total_disponibles} preguntas disponibles.")

        cantidad = st.number_input("🎯 ¿Cuántas preguntas quieres responder?", 
                                   min_value=1, max_value=total_disponibles, value=min(10, total_disponibles), step=1)

        if st.button("Iniciar test"):
            st.session_state.preguntas_seleccionadas = random.sample(todas, cantidad)
            st.rerun()

    elif st.session_state.indice < len(st.session_state.preguntas_seleccionadas):
        i = st.session_state.indice
        actual = st.session_state.preguntas_seleccionadas[i]
        clave = actual["pregunta"]

        if clave not in st.session_state.opciones_preguntas:
            opciones = actual["opciones"].copy()
            random.shuffle(opciones)
            st.session_state.opciones_preguntas[clave] = opciones
        else:
            opciones = st.session_state.opciones_preguntas[clave]

        st.info(f"**Pregunta {i + 1} de {len(st.session_state.preguntas_seleccionadas)}**  |  **Nivel:** {actual['nivel']}")
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
        total = len(st.session_state.preguntas_seleccionadas)
        st.success("🎉 ¡Has terminado el test!")
        st.write(f"**Puntaje final:** {st.session_state.correctas} / {total} ({round(st.session_state.correctas / total * 100)}%)")
        st.progress(st.session_state.correctas / total)

        st.markdown("### 📋 Resultados detallados")
        df = pd.DataFrame(st.session_state.respondidas)
        st.dataframe(df, use_container_width=True)

        json_resultado = json.dumps(st.session_state.respondidas, indent=2)
        st.download_button("📥 Descargar reporte JSON", data=json_resultado, file_name="resultados_test.json", mime="application/json")

        if st.button("🔄 Reiniciar test"):
            for k in ["preguntas_seleccionadas", "indice", "correctas", "respondidas", "opciones_preguntas"]:
                st.session_state.pop(k, None)
            st.rerun()
else:
    st.warning("Por favor, sube un archivo `.json` válido con las preguntas.")

# Test de Programación con Streamlit

Este proyecto es una aplicación en Streamlit para realizar un test de programación con preguntas clasificadas por nivel de dificultad (Fácil, Medio, Difícil, Práctica). Las preguntas deben cargarse desde un archivo `preguntas.json`.

## ¿Cómo ejecutarlo?

```bash
streamlit run test_programacion.py
```

## Estructura esperada del archivo JSON

```json
[
  {
    "nivel": "Fácil",
    "pregunta": "¿Qué método HTTP se usa para obtener información?",
    "opciones": ["GET", "POST", "PUT", "DELETE"],
    "respuesta": "GET"
  },
  ...
]
```

## Despliegue en Streamlit Cloud

1. Sube este repositorio a GitHub.
2. Entra a [https://streamlit.io/cloud](https://streamlit.io/cloud).
3. Conecta tu cuenta de GitHub y selecciona este repositorio.
4. Establece `test_programacion.py` como archivo principal.
5. ¡Listo!

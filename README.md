# VEIL Memory Booth — Mio Úmore
### Demo interactiva · L'Oréal Brandstorm 2026

---

## Setup (una sola vez)

```bash
# 1. Clona el repo
git clone https://github.com/TU_USUARIO/mio-umore-ai.git
cd mio-umore-ai

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Corre la app
streamlit run app.py
```

Se abre automáticamente en `http://localhost:8501`

---

## Estructura del proyecto

```
mio-umore-ai/
├── app.py                      ← App principal Streamlit
├── requirements.txt
├── data/
│   ├── emotion_scent_map.json  ← Probabilidades del dataset (825 votos, Dani Sanz)
│   └── accord_library.json     ← Librería de acordes (Ana Quemistry — TODO: completar)
└── README.md
```

---

## Cómo actualizar los acordes (Ana)

Abre `data/accord_library.json` y busca todos los campos que dicen `"TODO"`.
Para cada acorde, completa:
- `ingredientes_ana`: nombre INCI, % en fórmula, origen, costo por gramo
- Verifica `ifra_ok` para ylang ylang (marcado como pendiente en AC08)

---

## Cómo actualizar las preguntas (Dani)

En `app.py`, busca el comentario `# STEP 1 — PREGUNTAS DE INTENCIÓN` (~línea 220).
Cambia el texto de las opciones en los `st.radio()` según el copy final.
Si cambias las opciones, actualiza también los diccionarios en la función `emotion_from_answers()`.

---

## Base de datos del modelo

Las probabilidades emoción → familia olfativa vienen del análisis de **825 votos reales**
(55 respondentes × 15 escenarios, encuesta Dani Sanz).

Asociaciones con mayor confianza estadística:
- Esperanza → Aquatic/Mineral (80%, CI [56%, 93%])
- Triunfo → Sparkling/Boozy (62%, CI [41%, 79%])
- Romance → Floral (82%)
- Renovación → Green/Earthy (61%)

Escenarios estadísticamente significativos (permutation p-value):
- Escenario 15: p ≈ 0.008, Cramér's V = 0.416
- Escenario 4:  p ≈ 0.021, V = 0.361
- Escenario 8:  p ≈ 0.045, V = 0.348

---

## Equipo

| Rol | Nombre | Responsabilidad en este repo |
|-----|--------|------------------------------|
| IA + Ingeniería | María Fernanda | app.py, emotion_scent_map.json |
| Marketing + UX | Dani Sanz | copy de preguntas, memory titles |
| Química | Ana Quemistry | accord_library.json (ingredientes) |

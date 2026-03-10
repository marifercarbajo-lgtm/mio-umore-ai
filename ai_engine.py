"""
ai_engine.py — Motor de IA para Mio Úmore
Usa OpenAI GPT para interpretar historias libres del usuario
y extraer emociones + keywords sensoriales.

Pipeline:
  Historia libre → GPT analiza → JSON {emocion, keywords_sensoriales, intensidad}
  → emotion_scent_map (probabilidades de Dani) → familia olfativa
  → accord_library (fichas de Ana) → acorde final

Fallback: si no hay API key o la llamada falla, usa keyword matching local.
"""

import json
import os
import re
import random


# ── SYSTEM PROMPT PARA GPT ─────────────────────────────────────────────

SYSTEM_PROMPT = """Eres un perfumista emocional experto. Tu trabajo es analizar la historia 
personal de un cliente y extraer la esencia emocional que se convertirá en un perfume personalizado.

El cliente te dará:
- Una historia libre (un recuerdo, una persona, un lugar, un momento)
- La ocasión para la que quiere el perfume
- Cómo quiere sentirse

Debes responder ÚNICAMENTE con un JSON válido (sin markdown, sin backticks, sin texto adicional) 
con esta estructura exacta:

{
  "emocion_primaria": "una de: Esperanza, Romance, Triunfo, Renovación, Intimidad, Calma, Confianza, Determinación, Emoción, Confort, Libertad, Serenidad, Gratitud, Inspiración, Claridad",
  "emocion_secundaria": "otra emoción de la lista anterior, diferente a la primaria",
  "keywords_sensoriales": ["lista", "de", "3-5", "palabras", "que evoquen sentidos"],
  "ambiente": "descripción breve del ambiente emocional en 1 frase corta",
  "intensidad": "suave | media | intensa",
  "temperatura_emocional": "fría | templada | cálida",
  "nombres_sugeridos": ["Nombre 1", "Nombre 2", "Nombre 3"]
}

REGLAS IMPORTANTES:
- La emoción primaria es la que DOMINA la historia del cliente
- La emoción secundaria es el matiz que la complementa
- Los keywords sensoriales deben ser concretos y olfativos: olores, texturas, temperaturas, materiales
- Ejemplos de buenos keywords: "sal marina", "madera húmeda", "piel cálida", "humo de leña", "pétalos frescos"
- La ocasión y el sentimiento deseado deben MODULAR tu análisis, no dominarlo
- Si la historia es corta o vaga, infiere con sensibilidad poética
- Los nombres_sugeridos son nombres POÉTICOS para grabar en la botella del perfume
- Los nombres DEBEN estar inspirados directamente en la historia del cliente, no ser genéricos
- Ejemplo: si habla de tulipanes en Amsterdam → "Tulipanes de Abril", "Ámsterdam en Flor", "El Canal y Tú"
- Ejemplo: si habla de su abuela cocinando → "La Cocina de Siempre", "Manos de Canela", "Domingo con Ella"
- Los nombres deben ser cortos (2-5 palabras), en español, emotivos y personales
- NUNCA devuelvas texto fuera del JSON
- NUNCA uses backticks ni markdown
"""


def analyze_with_llm(story: str, ocasion: str, sentir: str, api_key: str = None) -> dict:
    """
    Llama a Anthropic Claude para analizar la historia del usuario.
    Devuelve un dict con emocion_primaria, emocion_secundaria, etc.
    Si falla, devuelve None y el caller usa el fallback de keywords.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)

        user_message = f"""OCASIÓN: {ocasion}
CÓMO QUIERE SENTIRSE: {sentir}

HISTORIA DEL CLIENTE:
\"{story}\""""

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ],
        )

        raw = response.content[0].text.strip()
        raw = re.sub(r'^```(?:json)?\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)

        result = json.loads(raw)

        required = ["emocion_primaria", "emocion_secundaria", "keywords_sensoriales", "ambiente"]
        for field in required:
            if field not in result:
                return None

        return result

    except Exception as e:
        print(f"[AI Engine] GPT call failed: {e}")
        return None


# ── FALLBACK: KEYWORD MATCHING LOCAL ─────────────────────────────────

STORY_KEYWORDS = {
    # ── Mar / Agua ──
    "mar": ("Esperanza", 3), "océano": ("Esperanza", 3), "playa": ("Esperanza", 2),
    "agua": ("Calma", 2), "lluvia": ("Renovación", 3), "olas": ("Esperanza", 2),
    "río": ("Serenidad", 2), "lago": ("Calma", 2), "cascada": ("Libertad", 2),
    # ── Naturaleza / Tierra ──
    "tierra": ("Renovación", 2), "bosque": ("Serenidad", 3), "pino": ("Serenidad", 2),
    "montaña": ("Libertad", 2), "campo": ("Serenidad", 2), "hierba": ("Renovación", 2),
    "árbol": ("Serenidad", 2), "selva": ("Libertad", 2), "pradera": ("Calma", 2),
    # ── Flores (TODAS deben mapear a Romance o Gratitud, NO a tierra) ──
    "flores": ("Romance", 3), "flor": ("Romance", 3), "rosa": ("Romance", 3),
    "rosas": ("Romance", 3), "tulipán": ("Romance", 3), "tulipanes": ("Romance", 3),
    "jazmín": ("Romance", 3), "pétalos": ("Romance", 2), "lavanda": ("Calma", 3),
    "orquídea": ("Romance", 2), "girasol": ("Esperanza", 2), "girasoles": ("Esperanza", 2),
    "margarita": ("Calma", 2), "lirio": ("Romance", 2), "violeta": ("Romance", 2),
    "clavel": ("Gratitud", 2), "gardenia": ("Romance", 2), "azalea": ("Romance", 2),
    "jardín": ("Romance", 2), "ramo": ("Romance", 2), "bouquet": ("Romance", 2),
    "florero": ("Romance", 2), "primavera": ("Renovación", 3),
    # ── Hogar / Familia ──
    "casa": ("Confort", 3), "hogar": ("Confort", 3), "cocina": ("Confort", 2),
    "familia": ("Gratitud", 3), "mamá": ("Gratitud", 2), "abuela": ("Gratitud", 2),
    "papá": ("Gratitud", 2), "hijo": ("Gratitud", 2), "hija": ("Gratitud", 2),
    "abuelo": ("Gratitud", 2), "hermano": ("Gratitud", 2), "hermana": ("Gratitud", 2),
    # ── Amor / Intimidad ──
    "amor": ("Romance", 3), "beso": ("Romance", 2), "abrazo": ("Intimidad", 3),
    "piel": ("Intimidad", 2), "cariño": ("Romance", 2), "enamorad": ("Romance", 3),
    "pareja": ("Romance", 2), "corazón": ("Romance", 2),
    # ── Viaje / Libertad ──
    "viaje": ("Libertad", 3), "aventura": ("Libertad", 2), "volar": ("Libertad", 2),
    "escapar": ("Libertad", 2), "correr": ("Libertad", 2), "explorar": ("Libertad", 2),
    "camino": ("Libertad", 2), "vuelo": ("Libertad", 2), "tren": ("Emoción", 2),
    # ── Ciudades / Lugares ──
    "ciudad": ("Emoción", 2), "parís": ("Romance", 3), "paris": ("Romance", 3),
    "amsterdam": ("Romance", 2), "roma": ("Romance", 2), "venecia": ("Romance", 3),
    "tokyo": ("Emoción", 2), "nueva york": ("Emoción", 2), "barcelona": ("Emoción", 2),
    "italia": ("Romance", 2), "francia": ("Romance", 2), "europa": ("Emoción", 2),
    # ── Noche / Misterio ──
    "noche": ("Intimidad", 2), "luna": ("Serenidad", 2), "estrellas": ("Esperanza", 2),
    "oscuro": ("Determinación", 2), "misterio": ("Intimidad", 2), "sombra": ("Intimidad", 2),
    # ── Fuerza / Logro ──
    "fuerza": ("Determinación", 3), "poder": ("Confianza", 3), "logré": ("Triunfo", 3),
    "gané": ("Triunfo", 3), "victoria": ("Triunfo", 2), "éxito": ("Triunfo", 2),
    "conquist": ("Triunfo", 2), "meta": ("Determinación", 2),
    # ── Calma / Paz ──
    "paz": ("Serenidad", 3), "silencio": ("Serenidad", 2), "calma": ("Calma", 3),
    "tranquil": ("Calma", 3), "meditar": ("Serenidad", 2), "respir": ("Calma", 2),
    # ── Renovación ──
    "libre": ("Libertad", 3), "nuevo": ("Renovación", 3), "empezar": ("Renovación", 2),
    "cambio": ("Renovación", 2), "renacer": ("Renovación", 3),
    # ── Creatividad ──
    "libro": ("Inspiración", 3), "arte": ("Inspiración", 2), "crear": ("Inspiración", 2),
    "música": ("Emoción", 2), "baile": ("Libertad", 2), "pintar": ("Inspiración", 2),
    "canción": ("Emoción", 2), "poema": ("Inspiración", 2),
    # ── Comida / Bebida ──
    "café": ("Confort", 2), "vino": ("Romance", 2), "champagne": ("Triunfo", 2),
    "chocolate": ("Confort", 2), "pan": ("Confort", 2), "cocinar": ("Confort", 2),
    "cena": ("Romance", 2), "desayuno": ("Confort", 2),
    # ── Decisión ──
    "decidí": ("Determinación", 3), "elegí": ("Confianza", 2), "confío": ("Confianza", 2),
    # ── Luz / Clima ──
    "luz": ("Claridad", 2), "sol": ("Emoción", 2), "brillo": ("Confianza", 2),
    "amanecer": ("Esperanza", 2), "atardecer": ("Serenidad", 2),
    "nieve": ("Calma", 2), "verano": ("Emoción", 2), "otoño": ("Serenidad", 2),
    "invierno": ("Calma", 2),
    # ── Misc ──
    "perfume": ("Confianza", 1), "recuerdo": ("Gratitud", 2), "infancia": ("Confort", 3),
    "niñez": ("Confort", 2), "colegio": ("Emoción", 2), "universidad": ("Emoción", 2),
    "cumpleaños": ("Gratitud", 2), "boda": ("Romance", 3), "graduación": ("Triunfo", 2),
}

OCASION_MAP = {
    "Para el día a día":        {"Calma": 2, "Confort": 2, "Claridad": 1},
    "Para una noche especial":  {"Confianza": 2, "Romance": 2, "Triunfo": 1},
    "Solo para mí":             {"Libertad": 2, "Serenidad": 2, "Gratitud": 1},
}

SENTIR_MAP = {
    "Poderosa e imparable":  {"Confianza": 3, "Determinación": 2, "Triunfo": 2},
    "Tranquila y en paz":    {"Calma": 3, "Serenidad": 3},
    "Libre y sin límites":   {"Libertad": 3, "Esperanza": 2, "Renovación": 2},
    "Misteriosa y profunda": {"Intimidad": 2, "Determinación": 2, "Inspiración": 2},
    "Luminosa y renovada":   {"Renovación": 3, "Esperanza": 3, "Claridad": 2},
}


def analyze_with_keywords(story: str, ocasion: str, sentir: str, emotion_map: dict) -> dict:
    """Fallback: keyword matching + ocasión/sentimiento."""
    valid_emotions = [e for e in emotion_map.keys() if e != "_meta"]
    scores = {e: 0 for e in valid_emotions}

    matched_keywords = []
    if story:
        s = story.lower()
        for kw, (emotion, boost) in STORY_KEYWORDS.items():
            if kw in s and emotion in scores:
                scores[emotion] += boost
                matched_keywords.append(kw)
        if len(story.split()) > 80:
            scores["Intimidad"] = scores.get("Intimidad", 0) + 2
            scores["Inspiración"] = scores.get("Inspiración", 0) + 1

    for k, v in OCASION_MAP.items():
        if ocasion == k:
            for e, pts in v.items():
                if e in scores:
                    scores[e] += pts
    for k, v in SENTIR_MAP.items():
        if sentir == k:
            for e, pts in v.items():
                if e in scores:
                    scores[e] += pts

    sorted_emo = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_emo[0][0] if sorted_emo[0][1] > 0 else "Calma"
    secondary = sorted_emo[1][0] if len(sorted_emo) > 1 and sorted_emo[1][1] > 0 else "Serenidad"

    return {
        "emocion_primaria": primary,
        "emocion_secundaria": secondary,
        "keywords_sensoriales": matched_keywords[:5] if matched_keywords else ["brisa", "luz", "calma"],
        "ambiente": f"Un momento de {primary.lower()} con matices de {secondary.lower()}",
        "intensidad": "media",
        "temperatura_emocional": "templada",
    }


# ── PIPELINE COMPLETO ────────────────────────────────────────────────

MEMORY_TITLES = {
    "Renovación":    ["El día que empecé de nuevo", "Tierra fresca", "La mañana después"],
    "Esperanza":     ["Lo que viene", "El mar antes de llegar", "Todavía"],
    "Triunfo":       ["La noche que lo logré", "Brindis solo", "Merecido"],
    "Intimidad":     ["Más cerca que nadie", "Lo que no se dice", "Tú y yo, punto"],
    "Calma":         ["Cuando por fin", "La lluvia de afuera", "Sin prisa"],
    "Confianza":     ["Así entro yo", "Ya sé quién soy", "Firme"],
    "Claridad":      ["Todo tiene sentido", "La brisa que aclaró", "Sin ruido"],
    "Inspiración":   ["Cuando se me ocurrió", "El momento antes de todo", "De repente"],
    "Determinación": ["No hay vuelta atrás", "Ya decidí", "El bosque y yo"],
    "Emoción":       ["Que empiece", "A punto de todo", "Ese cosquilleo"],
    "Romance":       ["Como la primera vez", "Flores de noche", "El perfume que me recuerdas"],
    "Confort":       ["Quedarse", "Domingo lento", "Mi lugar"],
    "Libertad":      ["Sin mapa", "Por fin fuera", "El bosque no tiene paredes"],
    "Serenidad":     ["Nada que resolver", "Solo el silencio", "El pino y el frío"],
    "Gratitud":      ["Por todo esto", "Gracias en silencio", "Lo que tengo"],
}


def full_analysis(story: str, ocasion: str, sentir: str,
                  emotion_map: dict, accord_lib: dict,
                  api_key: str = None) -> dict:
    """
    Pipeline completo. Reemplaza analyze_story + get_accord + get_memory_title.

    Retorna dict compatible con st.session_state.result:
    {
        "emotion": str,
        "accord": dict,
        "memory_title": str,
        "analysis": dict,       # metadata del análisis GPT/keywords
        "method": str,           # "gpt" o "keywords"
    }
    """

    # ── PASO 1: Interpretar historia ──
    gpt_result = analyze_with_llm(story, ocasion, sentir, api_key)

    if gpt_result:
        analysis = gpt_result
        method = "gpt"
    else:
        analysis = analyze_with_keywords(story, ocasion, sentir, emotion_map)
        method = "keywords"

    primary_emotion = analysis["emocion_primaria"]

    # ── PASO 2: Emoción → Familia olfativa (probabilidades de Dani) ──
    if primary_emotion in emotion_map:
        emotion_data = emotion_map[primary_emotion]
        distribution = emotion_data.get("distribution", {})
        families = list(distribution.keys())
        weights = list(distribution.values())
        if families and weights:
            chosen_family = random.choices(families, weights=weights, k=1)[0]
        else:
            chosen_family = emotion_data.get("top_family", "Floral")
    else:
        chosen_family = "Floral"

    # ── PASO 3: Familia → Acorde (de la librería de Ana) ──
    acordes = accord_lib.get("acordes", [])

    # Primero: match por emoción directa (como el get_accord original)
    candidates = [a for a in acordes if primary_emotion in a.get("emociones", [])]

    if not candidates:
        # Segundo: match por familia olfativa
        candidates = [a for a in acordes if a.get("familia", "") == chosen_family]

    if not candidates:
        # Último fallback
        candidates = acordes if acordes else [{
            "nombre": "Éphémère",
            "familia": chosen_family,
            "descripcion": "Un acorde delicado que captura la esencia de tu recuerdo",
            "notas": {"salida": ["bergamota"], "corazon": ["rosa"], "base": ["sándalo"]},
            "emociones": [primary_emotion],
        }]

    chosen_accord = random.choice(candidates)

    # ── PASO 4: Nombres para la botella ──
    # Si Claude generó nombres personalizados, usarlos. Si no, fallback al diccionario.
    if method == "gpt" and "nombres_sugeridos" in analysis:
        suggested_names = analysis["nombres_sugeridos"][:3]
    else:
        suggested_names = MEMORY_TITLES.get(primary_emotion, ["Lo que fue mío", "Sin nombre aún", "El momento"])

    memory_title = suggested_names[0] if suggested_names else "Mi Recuerdo"

    return {
        "emotion": primary_emotion,
        "accord": chosen_accord,
        "memory_title": memory_title,
        "suggested_names": suggested_names,
        "analysis": analysis,
        "method": method,
    }

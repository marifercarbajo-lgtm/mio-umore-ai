import streamlit as st
import json
import random
import time
from pathlib import Path

st.set_page_config(
    page_title="Mio Úmore",
    page_icon="◆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

@st.cache_data
def load_data():
    base = Path(__file__).parent / "data"
    with open(base / "emotion_scent_map.json", encoding="utf-8") as f:
        emotion_map = json.load(f)
    with open(base / "accord_library.json", encoding="utf-8") as f:
        accord_lib = json.load(f)
    return emotion_map, accord_lib

emotion_map, accord_lib = load_data()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Didact+Gothic&family=EB+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Didact Gothic', sans-serif;
    background-color: #080608;
    color: #D4C9BC;
}
.stApp {
    background: #080608;
    background-image:
        radial-gradient(ellipse at 20% 0%, rgba(180,140,100,0.04) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 100%, rgba(120,90,140,0.03) 0%, transparent 60%);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 3rem; padding-bottom: 4rem; max-width: 620px; }

.monogram { text-align: center; margin-bottom: 0.5rem; }
.monogram-inner {
    display: inline-block; width: 52px; height: 52px;
    border: 1px solid rgba(180,150,100,0.4); border-radius: 50%;
    line-height: 52px; font-family: 'Playfair Display', serif;
    font-size: 1.1rem; color: #B4966A; letter-spacing: 0.05em; position: relative;
}
.monogram-inner::before {
    content: ''; position: absolute; inset: 4px; border-radius: 50%;
    border: 1px solid rgba(180,150,100,0.15);
}
.brand-name {
    font-family: 'Playfair Display', serif; font-size: 2.8rem; font-weight: 300;
    letter-spacing: 0.18em; text-align: center; color: #EDE5D8;
    margin-bottom: 0.3rem; text-transform: uppercase;
}
.brand-tagline {
    font-family: 'EB Garamond', serif; font-size: 0.8rem; letter-spacing: 0.45em;
    text-align: center; color: #6B5E50; text-transform: uppercase; margin-bottom: 0.6rem;
}
.ornament { text-align: center; color: #B4966A; font-size: 0.7rem; letter-spacing: 0.5em; margin-bottom: 2.5rem; opacity: 0.6; }

.rule { display: flex; align-items: center; gap: 1rem; margin: 2rem 0; }
.rule-line { flex: 1; height: 1px; background: rgba(180,150,100,0.15); }
.rule-diamond { color: #B4966A; font-size: 0.5rem; opacity: 0.6; }

.q-step { font-size: 0.58rem; letter-spacing: 0.4em; color: #4A3F35; text-transform: uppercase; margin-bottom: 0.5rem; text-align: center; }
.q-text { font-family: 'Playfair Display', serif; font-size: 1.35rem; font-weight: 300; font-style: italic; color: #C9B89A; text-align: center; margin-bottom: 1.6rem; line-height: 1.5; }

div[role="radiogroup"] { display: flex; flex-direction: column; gap: 0.4rem; }
div[role="radiogroup"] label {
    background: transparent !important; border: 1px solid rgba(180,150,100,0.12) !important;
    border-radius: 0 !important; padding: 0.75rem 1.2rem !important; color: #9A8C7E !important;
    font-family: 'Didact Gothic', sans-serif !important; font-size: 0.82rem !important;
    letter-spacing: 0.08em !important; transition: all 0.25s ease !important;
    cursor: pointer !important; text-align: center !important;
}
div[role="radiogroup"] label:hover {
    border-color: rgba(180,150,100,0.45) !important; color: #D4C9BC !important;
    background: rgba(180,150,100,0.03) !important;
}

.stTextArea textarea {
    background: rgba(180,150,100,0.02) !important; border: 1px solid rgba(180,150,100,0.2) !important;
    border-radius: 0 !important; color: #D4C9BC !important;
    font-family: 'EB Garamond', serif !important; font-size: 1.05rem !important;
    font-style: italic !important; line-height: 1.8 !important; padding: 1.2rem !important; resize: none !important;
}
.stTextArea textarea:focus { border-color: rgba(180,150,100,0.5) !important; box-shadow: none !important; }
.stTextArea textarea::placeholder { color: #3D342A !important; font-style: italic !important; }

.stButton > button {
    background: transparent !important; border: 1px solid rgba(180,150,100,0.4) !important;
    color: #B4966A !important; font-family: 'Didact Gothic', sans-serif !important;
    font-size: 0.68rem !important; font-weight: 400 !important; letter-spacing: 0.35em !important;
    text-transform: uppercase !important; padding: 0.9rem 2rem !important;
    border-radius: 0 !important; transition: all 0.3s ease !important; width: 100% !important; margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: rgba(180,150,100,0.08) !important;
    border-color: rgba(180,150,100,0.7) !important; color: #D4B98A !important;
}

.mirror-container { text-align: center; padding: 3rem 2rem; }
.mirror-frame {
    display: inline-block; position: relative; padding: 2.5rem 3rem;
    border: 1px solid rgba(180,150,100,0.2);
    border-top: 2px solid rgba(180,150,100,0.5);
    border-bottom: 2px solid rgba(180,150,100,0.5);
}
.mirror-frame::before, .mirror-frame::after {
    content: '◆'; position: absolute; color: #B4966A; font-size: 0.5rem; opacity: 0.6;
}
.mirror-frame::before { top: -0.4rem; left: 50%; transform: translateX(-50%); }
.mirror-frame::after { bottom: -0.4rem; left: 50%; transform: translateX(-50%); }
.mirror-eye { font-size: 2rem; margin-bottom: 1rem; animation: pulse 2s ease-in-out infinite; }
.mirror-reading { font-family: 'Playfair Display', serif; font-size: 1rem; font-style: italic; color: #8A7A6A; letter-spacing: 0.1em; animation: flicker 1.5s ease-in-out infinite; }
@keyframes pulse { 0%, 100% { opacity: 0.4; transform: scale(1); } 50% { opacity: 1; transform: scale(1.08); } }
@keyframes flicker { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }

@keyframes smokeRise {
    0% { opacity: 0; transform: translateY(30px) scale(0.9); filter: blur(8px); }
    40% { opacity: 0.6; filter: blur(3px); }
    100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}
@keyframes bottleReveal {
    0% { opacity: 0; transform: translateY(40px); filter: blur(10px) brightness(0); }
    50% { filter: blur(2px) brightness(0.7); }
    100% { opacity: 1; transform: translateY(0); filter: blur(0) brightness(1); }
}
@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 20px rgba(180,150,100,0.1), 0 0 60px rgba(180,150,100,0.05); }
    50% { box-shadow: 0 0 40px rgba(180,150,100,0.2), 0 0 100px rgba(180,150,100,0.1); }
}
@keyframes smokeParticle {
    0% { opacity: 0.6; transform: translateY(0) translateX(0) scale(1); }
    100% { opacity: 0; transform: translateY(-80px) translateX(var(--dx)) scale(2.5); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes nameEngrave {
    0% { opacity: 0; letter-spacing: 0.5em; filter: blur(4px); }
    100% { opacity: 1; letter-spacing: 0.12em; filter: blur(0); }
}

.reveal-wrapper { animation: smokeRise 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards; }

.smoke-container { position: relative; height: 60px; margin-bottom: -10px; overflow: visible; }
.smoke-particle {
    position: absolute; bottom: 0; left: 50%; width: 40px; height: 40px; border-radius: 50%;
    background: radial-gradient(circle, rgba(200,180,160,0.15) 0%, transparent 70%);
    animation: smokeParticle 2.5s ease-out infinite;
}

.bottle-visual { width: 140px; margin: 0 auto; animation: bottleReveal 1.4s cubic-bezier(0.22, 1, 0.36, 1) 0.5s both; position: relative; }
.bottle-svg-container { position: relative; display: flex; justify-content: center; align-items: center; }
.bottle-glow {
    position: absolute; inset: -30px;
    background: radial-gradient(ellipse, rgba(180,150,100,0.12) 0%, transparent 70%);
    border-radius: 50%; animation: glowPulse 2.5s ease-in-out infinite;
}

.accord-reveal-card {
    background: linear-gradient(180deg, #0D0A08 0%, #080608 100%);
    border: 1px solid rgba(180,150,100,0.15); border-top: 2px solid #B4966A;
    padding: 2.5rem 2rem 2rem; margin-top: 1.5rem;
    animation: fadeInUp 0.8s ease 1.2s both; position: relative; overflow: hidden;
}
.accord-reveal-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(180,150,100,0.6), transparent);
}
.accord-name-reveal { font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 300; color: #EDE5D8; letter-spacing: 0.06em; margin-bottom: 0.2rem; animation: fadeInUp 0.6s ease 1.4s both; }
.accord-family-reveal { font-size: 0.6rem; letter-spacing: 0.45em; color: #5A4E42; text-transform: uppercase; margin-bottom: 1.4rem; animation: fadeInUp 0.6s ease 1.5s both; }
.accord-desc-reveal { font-family: 'EB Garamond', serif; font-size: 1.1rem; font-style: italic; color: #9A8C7E; line-height: 1.75; margin-bottom: 1.6rem; animation: fadeInUp 0.6s ease 1.6s both; }

.notes-row { display: flex; gap: 0; margin-bottom: 1.5rem; border-top: 1px solid rgba(180,150,100,0.08); border-bottom: 1px solid rgba(180,150,100,0.08); padding: 1rem 0; animation: fadeInUp 0.6s ease 1.7s both; }
.note-col { flex: 1; text-align: center; padding: 0 0.5rem; }
.note-col + .note-col { border-left: 1px solid rgba(180,150,100,0.08); }
.note-label { font-size: 0.55rem; letter-spacing: 0.35em; color: #4A3F35; text-transform: uppercase; margin-bottom: 0.4rem; }
.note-value { font-size: 0.78rem; color: #8A7A6A; line-height: 1.5; }

.engraved-section { background: #060504; border: 1px solid rgba(180,150,100,0.12); padding: 1.4rem; text-align: center; animation: fadeInUp 0.6s ease 1.9s both; position: relative; }
.engraved-section::before { content: '— ◆ —'; display: block; font-size: 0.5rem; color: rgba(180,150,100,0.3); letter-spacing: 0.4em; margin-bottom: 0.7rem; }
.engraved-section::after { content: '— ◆ —'; display: block; font-size: 0.5rem; color: rgba(180,150,100,0.3); letter-spacing: 0.4em; margin-top: 0.7rem; }
.engraved-name { font-family: 'Playfair Display', serif; font-size: 1.7rem; font-weight: 300; font-style: italic; color: #C9A87A; animation: nameEngrave 1.2s cubic-bezier(0.22,1,0.36,1) 2.2s both; letter-spacing: 0.12em; }
.engraved-sub { font-size: 0.58rem; letter-spacing: 0.35em; color: #3A3028; text-transform: uppercase; margin-top: 0.5rem; animation: fadeInUp 0.6s ease 2.6s both; }
.clean-badge { display: inline-block; font-size: 0.58rem; letter-spacing: 0.25em; text-transform: uppercase; border: 1px solid rgba(74,124,89,0.3); color: #4A7C59; padding: 0.3rem 0.8rem; margin-top: 1.2rem; animation: fadeInUp 0.6s ease 2.4s both; }
.hashtag { font-size: 0.65rem; letter-spacing: 0.2em; color: #3A3028; text-transform: uppercase; margin-top: 1rem; animation: fadeInUp 0.6s ease 2.8s both; }

.stProgress > div > div { background: rgba(180,150,100,0.08) !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, #6B5040, #B4966A) !important; }

.intro-container { text-align: center; padding: 2rem 1rem 3rem; }
.intro-text { font-family: 'EB Garamond', serif; font-size: 1.2rem; font-style: italic; color: #6B5E50; line-height: 1.9; max-width: 380px; margin: 0 auto 2.5rem; }
.intro-detail { font-size: 0.62rem; letter-spacing: 0.35em; color: #3A3028; text-transform: uppercase; margin-bottom: 2rem; }

.mirror-prompt { background: rgba(180,150,100,0.02); border-left: 2px solid rgba(180,150,100,0.25); padding: 1.2rem 1.4rem; margin-bottom: 1.2rem; font-family: 'EB Garamond', serif; font-size: 1rem; font-style: italic; color: #7A6A5A; line-height: 1.7; }
</style>
""", unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────
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

STORY_KEYWORDS = {
    "mar": ("Esperanza", 3), "océano": ("Esperanza", 3), "playa": ("Esperanza", 2),
    "agua": ("Calma", 2), "lluvia": ("Renovación", 3), "tierra": ("Renovación", 2),
    "bosque": ("Serenidad", 3), "pino": ("Serenidad", 2), "flores": ("Romance", 2),
    "rosa": ("Romance", 2), "jardín": ("Gratitud", 2), "casa": ("Confort", 3),
    "hogar": ("Confort", 3), "cocina": ("Confort", 2), "familia": ("Gratitud", 3),
    "mamá": ("Gratitud", 2), "abuela": ("Gratitud", 2), "amor": ("Romance", 3),
    "beso": ("Romance", 2), "abrazo": ("Intimidad", 3), "viaje": ("Libertad", 3),
    "aventura": ("Libertad", 2), "noche": ("Intimidad", 2), "luna": ("Serenidad", 2),
    "estrellas": ("Esperanza", 2), "fuerza": ("Determinación", 3), "poder": ("Confianza", 3),
    "logré": ("Triunfo", 3), "gané": ("Triunfo", 3), "victoria": ("Triunfo", 2),
    "éxito": ("Triunfo", 2), "paz": ("Serenidad", 3), "silencio": ("Serenidad", 2),
    "libre": ("Libertad", 3), "volar": ("Libertad", 2), "nuevo": ("Renovación", 3),
    "empezar": ("Renovación", 2), "cambio": ("Renovación", 2), "luz": ("Claridad", 2),
    "oscuro": ("Determinación", 2), "misterio": ("Intimidad", 2), "champagne": ("Triunfo", 2),
    "libro": ("Inspiración", 3), "arte": ("Inspiración", 2), "crear": ("Inspiración", 2),
    "decidí": ("Determinación", 3), "confío": ("Confianza", 2), "ciudad": ("Emoción", 2),
    "música": ("Emoción", 2), "baile": ("Libertad", 2), "café": ("Confort", 2),
    "vino": ("Romance", 2), "perfume": ("Confianza", 1), "tranquil": ("Calma", 3),
}

def analyze_story(story_text, ocasion, sentir):
    scores = {e: 0 for e in emotion_map.keys() if e != "_meta"}
    if story_text:
        s = story_text.lower()
        for kw, (emotion, boost) in STORY_KEYWORDS.items():
            if kw in s and emotion in scores:
                scores[emotion] += boost
        word_count = len(story_text.split())
        if word_count > 80:
            scores["Intimidad"] = scores.get("Intimidad", 0) + 2
            scores["Inspiración"] = scores.get("Inspiración", 0) + 1

    ocasion_map = {
        "Para el día a día":       {"Calma": 2, "Confort": 2, "Claridad": 1},
        "Para una noche especial": {"Confianza": 2, "Romance": 2, "Triunfo": 1},
        "Solo para mí":            {"Libertad": 2, "Serenidad": 2, "Gratitud": 1},
    }
    sentir_map = {
        "Poderosa e imparable":  {"Confianza": 3, "Determinación": 2, "Triunfo": 2},
        "Tranquila y en paz":    {"Calma": 3, "Serenidad": 3},
        "Libre y sin límites":   {"Libertad": 3, "Esperanza": 2, "Renovación": 2},
        "Misteriosa y profunda": {"Intimidad": 2, "Determinación": 2, "Inspiración": 2},
        "Luminosa y renovada":   {"Renovación": 3, "Esperanza": 3, "Claridad": 2},
    }
    for k, v in ocasion_map.items():
        if ocasion == k:
            for e, pts in v.items():
                scores[e] = scores.get(e, 0) + pts
    for k, v in sentir_map.items():
        if sentir == k:
            for e, pts in v.items():
                scores[e] = scores.get(e, 0) + pts

    return max(scores, key=lambda e: scores[e])

def get_accord(emotion):
    candidates = [a for a in accord_lib["acordes"] if emotion in a["emociones"]]
    if candidates:
        return random.choice(candidates)
    top_family = emotion_map.get(emotion, {}).get("top_family", "Clean/Fresh")
    family_c = [a for a in accord_lib["acordes"] if a["familia"] == top_family]
    return random.choice(family_c) if family_c else accord_lib["acordes"][0]

def get_memory_title(emotion):
    titles = MEMORY_TITLES.get(emotion, ["Lo que fue mío", "Sin nombre aún", "El momento"])
    return random.choice(titles)

def bottle_svg():
    return """
    <svg width="120" height="180" viewBox="0 0 120 180" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="glassGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#1A1510;stop-opacity:0.95"/>
          <stop offset="40%" style="stop-color:#2A2018;stop-opacity:0.85"/>
          <stop offset="100%" style="stop-color:#0D0A08;stop-opacity:0.98"/>
        </linearGradient>
        <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#6B5040"/>
          <stop offset="50%" style="stop-color:#B4966A"/>
          <stop offset="100%" style="stop-color:#6B5040"/>
        </linearGradient>
        <linearGradient id="shineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:rgba(255,255,255,0)"/>
          <stop offset="30%" style="stop-color:rgba(255,240,210,0.06)"/>
          <stop offset="100%" style="stop-color:rgba(255,255,255,0)"/>
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <rect x="46" y="8" width="28" height="6" rx="1" fill="url(#goldGrad)" opacity="0.9"/>
      <rect x="50" y="4" width="20" height="8" rx="1" fill="url(#goldGrad)" opacity="0.8"/>
      <rect x="54" y="1" width="12" height="6" rx="1" fill="url(#goldGrad)" opacity="0.7"/>
      <rect x="48" y="14" width="24" height="16" rx="1" fill="url(#glassGrad)" stroke="#B4966A" stroke-width="0.5" stroke-opacity="0.4"/>
      <rect x="50" y="15" width="8" height="14" fill="url(#shineGrad)"/>
      <rect x="46" y="28" width="28" height="3" fill="url(#goldGrad)" opacity="0.7"/>
      <path d="M28 35 Q25 38 24 50 L24 155 Q24 162 30 164 L90 164 Q96 162 96 155 L96 50 Q95 38 92 35 Z" fill="url(#glassGrad)" stroke="#B4966A" stroke-width="0.6" stroke-opacity="0.3"/>
      <path d="M32 38 Q30 42 30 55 L30 150 Q30 156 34 158 L46 158 L46 38 Z" fill="url(#shineGrad)" opacity="0.5"/>
      <ellipse cx="60" cy="110" rx="28" ry="40" fill="none" stroke="#B4966A" stroke-width="0.5" stroke-opacity="0.08" filter="url(#glow)"/>
      <ellipse cx="60" cy="110" rx="18" ry="28" fill="#B4966A" opacity="0.04"/>
      <rect x="24" y="158" width="72" height="4" fill="url(#goldGrad)" opacity="0.5"/>
      <rect x="24" y="162" width="72" height="2" fill="url(#goldGrad)" opacity="0.3"/>
      <polygon points="60,90 64,96 60,102 56,96" fill="none" stroke="#B4966A" stroke-width="0.8" stroke-opacity="0.4"/>
      <polygon points="60,93 62,96 60,99 58,96" fill="#B4966A" opacity="0.15"/>
      <line x1="28" y1="35" x2="34" y2="35" stroke="#B4966A" stroke-width="0.6" stroke-opacity="0.5"/>
      <line x1="28" y1="35" x2="28" y2="42" stroke="#B4966A" stroke-width="0.6" stroke-opacity="0.5"/>
      <line x1="92" y1="35" x2="86" y2="35" stroke="#B4966A" stroke-width="0.6" stroke-opacity="0.5"/>
      <line x1="92" y1="35" x2="92" y2="42" stroke="#B4966A" stroke-width="0.6" stroke-opacity="0.5"/>
    </svg>
    """

# ── SESSION STATE ──────────────────────────────────────────
for key, val in [("step", 0), ("result", None), ("ocasion", ""), ("sentir", ""), ("final_name", "")]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── HEADER ─────────────────────────────────────────────────
st.markdown('<div class="monogram"><div class="monogram-inner">M</div></div>', unsafe_allow_html=True)
st.markdown('<div class="brand-name">Mio Úmore</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-tagline">Maison de Parfum · Paris</div>', unsafe_allow_html=True)
st.markdown('<div class="ornament">◆ ◆ ◆</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# STEP 0 — INTRO
# ══════════════════════════════════════════════════════════
if st.session_state.step == 0:
    st.markdown("""
    <div class="intro-container">
        <p class="intro-text">Le miroir vous écoute.<br>Parlez-lui de vous.</p>
        <p class="intro-detail">Deux questions · Une histoire · Votre parfum</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Entrer"):
        st.session_state.step = 1
        st.rerun()

# ══════════════════════════════════════════════════════════
# STEP 1 — DOS PREGUNTAS
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    st.markdown('<div class="q-step">I · Contexte</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-text">¿Para qué momento es este perfume?</div>', unsafe_allow_html=True)
    ocasion = st.radio("ocasion", ["Para el día a día", "Para una noche especial", "Solo para mí"], label_visibility="collapsed")

    st.markdown('<div class="rule"><div class="rule-line"></div><div class="rule-diamond">◆</div><div class="rule-line"></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="q-step">II · Désir</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-text">¿Cómo quieres sentirte al usarlo?</div>', unsafe_allow_html=True)
    sentir = st.radio("sentir", ["Poderosa e imparable", "Tranquila y en paz", "Libre y sin límites", "Misteriosa y profunda", "Luminosa y renovada"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continuer →"):
        st.session_state.ocasion = ocasion
        st.session_state.sentir = sentir
        st.session_state.step = 2
        st.rerun()

# ══════════════════════════════════════════════════════════
# STEP 2 — LA HISTORIA
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.markdown('<div class="q-step">III · Le Miroir vous écoute</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-text">Cuéntale algo al espejo.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="mirror-prompt">
        Una persona, un lugar, un recuerdo — o algo que aún no ha pasado pero lo deseas.
        Describe a alguien que amas. Cuenta una noche que no olvidarás.
        Lo que sea. El espejo lo convierte en perfume.
    </div>
    """, unsafe_allow_html=True)

    historia = st.text_area("historia", placeholder="Escribe aquí... no hay respuesta correcta.", height=160, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("← Volver"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("El espejo interpreta →"):
            if historia.strip():
                emotion = analyze_story(historia, st.session_state.ocasion, st.session_state.sentir)
                accord = get_accord(emotion)
                memory_title = get_memory_title(emotion)
                st.session_state.result = {"emotion": emotion, "accord": accord, "memory_title": memory_title}
                st.session_state.step = 3
                st.rerun()
            else:
                st.markdown('<div style="font-size:0.75rem;color:#5A4E42;text-align:center;font-style:italic;margin-top:0.5rem;">El espejo espera tus palabras...</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# STEP 3 — MIRROR PROCESSING
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.markdown("""
    <div class="mirror-container">
        <div class="mirror-frame">
            <div class="mirror-eye">🜲</div>
            <div class="mirror-reading">Le miroir lit votre histoire...</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    progress = st.progress(0)
    msg_ph = st.empty()
    messages = ["Analizando tu historia...", "Identificando tu esencia...", "Componiendo tu fórmula...", "Grabando tu botella..."]
    for i, msg in enumerate(messages):
        time.sleep(0.55)
        progress.progress(int((i + 1) * 25))
        msg_ph.markdown(f'<div style="text-align:center;font-family:\'EB Garamond\',serif;font-style:italic;color:#4A3F35;font-size:0.9rem;letter-spacing:0.1em;margin-top:0.5rem;">{msg}</div>', unsafe_allow_html=True)

    time.sleep(0.3)
    st.session_state.step = 4
    st.rerun()

# ══════════════════════════════════════════════════════════
# STEP 4 — NOMBRE GRABADO
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    r = st.session_state.result
    memory_title = r["memory_title"]
    suggested = MEMORY_TITLES.get(r["emotion"], ["Lo que fue mío", "Sin nombre aún", "El momento"])

    st.markdown('<div class="q-step">IV · Votre gravure</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-text">Este nombre quedará grabado<br>en tu botella para siempre.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'EB Garamond',serif;font-size:0.9rem;font-style:italic;
                color:#5A4E42;text-align:center;margin-bottom:1.5rem;letter-spacing:0.05em;">
        El espejo sugiere estos títulos — o escribe el tuyo.
    </div>
    """, unsafe_allow_html=True)

    titulo_elegido = st.radio(
        "titulo",
        options=suggested + ["✦ Escribir el mío"],
        label_visibility="collapsed"
    )

    titulo_custom = ""
    if titulo_elegido == "✦ Escribir el mío":
        titulo_custom = st.text_area(
            "custom_name",
            placeholder="El nombre de tu recuerdo...",
            height=68,
            label_visibility="collapsed"
        )

    titulo_final = titulo_custom.strip() if titulo_elegido == "✦ Escribir el mío" else titulo_elegido

    if titulo_final and titulo_final != "✦ Escribir el mío":
        st.markdown(f"""
        <div style="margin:1.5rem 0;text-align:center;">
            <div style="font-size:0.55rem;letter-spacing:0.4em;color:#3A3028;text-transform:uppercase;margin-bottom:0.6rem;">
                Preview · Grabado en tu botella
            </div>
            <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:300;
                        font-style:italic;color:#C9A87A;letter-spacing:0.1em;
                        padding:1rem 1.5rem;border:1px solid rgba(180,150,100,0.15);
                        border-top:2px solid rgba(180,150,100,0.5);display:inline-block;">
                {titulo_final}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("← Volver"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        btn_label = "Graver et révéler →" if titulo_final else "Choisir un nom d'abord"
        if st.button(btn_label):
            if titulo_final:
                st.session_state.final_name = titulo_final
                st.session_state.step = 5
                st.rerun()

# ══════════════════════════════════════════════════════════
# STEP 5 — REVEAL DRAMÁTICO
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    r = st.session_state.result
    accord = r["accord"]
    emotion = r["emotion"]
    final_name = st.session_state.final_name

    notes_s = " · ".join(accord["notas"]["salida"])
    notes_c = " · ".join(accord["notas"]["corazon"])
    notes_b = " · ".join(accord["notas"]["base"])

    # 1 — Humo (sin f-string, sin variables)
    st.markdown("""
    <div class="smoke-container">
        <div class="smoke-particle" style="--dx:-20px;animation-delay:0s"></div>
        <div class="smoke-particle" style="--dx:15px;animation-delay:0.4s"></div>
        <div class="smoke-particle" style="--dx:-8px;animation-delay:0.8s"></div>
        <div class="smoke-particle" style="--dx:25px;animation-delay:1.2s"></div>
        <div class="smoke-particle" style="--dx:-15px;animation-delay:0.6s"></div>
    </div>
    """, unsafe_allow_html=True)

    # 2 — Botella (SVG puro, sin f-string)
    st.markdown("""
    <div class="bottle-visual">
      <div class="bottle-svg-container">
        <div class="bottle-glow"></div>
        <svg width="120" height="180" viewBox="0 0 120 180" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="gG" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#1A1510;stop-opacity:0.95"/>
              <stop offset="40%" style="stop-color:#2A2018;stop-opacity:0.85"/>
              <stop offset="100%" style="stop-color:#0D0A08;stop-opacity:0.98"/>
            </linearGradient>
            <linearGradient id="goG" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" style="stop-color:#6B5040"/>
              <stop offset="50%" style="stop-color:#B4966A"/>
              <stop offset="100%" style="stop-color:#6B5040"/>
            </linearGradient>
            <linearGradient id="gsG" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="white" stop-opacity="0"/>
              <stop offset="30%" stop-color="#FFF0D2" stop-opacity="0.06"/>
              <stop offset="100%" stop-color="white" stop-opacity="0"/>
            </linearGradient>
          </defs>
          <rect x="46" y="8" width="28" height="6" rx="1" fill="url(#goG)" opacity="0.9"/>
          <rect x="50" y="4" width="20" height="8" rx="1" fill="url(#goG)" opacity="0.8"/>
          <rect x="54" y="1" width="12" height="6" rx="1" fill="url(#goG)" opacity="0.7"/>
          <rect x="48" y="14" width="24" height="16" rx="1" fill="url(#gG)" stroke="#B4966A" stroke-width="0.5" stroke-opacity="0.4"/>
          <rect x="50" y="15" width="8" height="14" fill="url(#gsG)"/>
          <rect x="46" y="28" width="28" height="3" fill="url(#goG)" opacity="0.7"/>
          <path d="M28 35 Q25 38 24 50 L24 155 Q24 162 30 164 L90 164 Q96 162 96 155 L96 50 Q95 38 92 35 Z" fill="url(#gG)" stroke="#B4966A" stroke-width="0.6" stroke-opacity="0.3"/>
          <path d="M32 38 Q30 42 30 55 L30 150 Q30 156 34 158 L46 158 L46 38 Z" fill="url(#gsG)" opacity="0.5"/>
          <ellipse cx="60" cy="110" rx="18" ry="28" fill="#B4966A" opacity="0.04"/>
          <rect x="24" y="158" width="72" height="4" fill="url(#goG)" opacity="0.5"/>
          <rect x="24" y="162" width="72" height="2" fill="url(#goG)" opacity="0.3"/>
          <polygon points="60,90 64,96 60,102 56,96" fill="none" stroke="#B4966A" stroke-width="0.8" stroke-opacity="0.4"/>
          <polygon points="60,93 62,96 60,99 58,96" fill="#B4966A" opacity="0.15"/>
          <line x1="28" y1="35" x2="34" y2="35" stroke="#B4966A" stroke-width="0.6" stroke-opacity="0.5"/>
          <line x1="28" y1="35" x2="28" y2="42" stroke="#B4966A" stroke-width="0.6" stroke-opacity="0.5"/>
          <line x1="92" y1="35" x2="86" y2="35" stroke="#B4966A" stroke-width="0.6" stroke-opacity="0.5"/>
          <line x1="92" y1="35" x2="92" y2="42" stroke="#B4966A" stroke-width="0.6" stroke-opacity="0.5"/>
        </svg>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 3 — Card con datos del acord (f-string solo con texto, sin SVG)
    st.markdown(f"""
    <div class="accord-reveal-card">
        <div class="accord-name-reveal">{accord["nombre"]}</div>
        <div class="accord-family-reveal">{accord["familia"]} · {emotion}</div>
        <div class="accord-desc-reveal">{accord["descripcion"]}</div>
        <div class="notes-row">
            <div class="note-col">
                <div class="note-label">Sortie</div>
                <div class="note-value">{notes_s}</div>
            </div>
            <div class="note-col">
                <div class="note-label">Cœur</div>
                <div class="note-value">{notes_c}</div>
            </div>
            <div class="note-col">
                <div class="note-label">Fond</div>
                <div class="note-value">{notes_b}</div>
            </div>
        </div>
        <div class="engraved-section">
            <div class="engraved-name">{final_name}</div>
            <div class="engraved-sub">Gravé sur votre flacon</div>
        </div>
        <div style="text-align:center;">
            <div class="clean-badge">✦ Formule propre · Rechargeable</div>
            <div class="hashtag">#MioUmore</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Créer un autre parfum"):
        st.session_state.step = 0
        st.session_state.result = None
        st.session_state.final_name = ""
        st.rerun()

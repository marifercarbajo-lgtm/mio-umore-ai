import streamlit as st
import json
import random
import time
from pathlib import Path
from ai_engine import full_analysis

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
    font-family: 'EB Garamond', serif; font-size: 0.85rem; letter-spacing: 0.45em;
    text-align: center; color: #B4966A; text-transform: uppercase; margin-bottom: 0.6rem;
}
.ornament { text-align: center; color: #B4966A; font-size: 0.7rem; letter-spacing: 0.5em; margin-bottom: 2.5rem; opacity: 0.6; }

.rule { display: flex; align-items: center; gap: 1rem; margin: 2rem 0; }
.rule-line { flex: 1; height: 1px; background: rgba(180,150,100,0.15); }
.rule-diamond { color: #B4966A; font-size: 0.5rem; opacity: 0.6; }

.q-step { font-size: 0.72rem; letter-spacing: 0.35em; color: #B4966A; text-transform: uppercase; margin-bottom: 0.6rem; text-align: center; }
.q-text { font-family: 'Playfair Display', serif; font-size: 1.55rem; font-weight: 400; font-style: italic; color: #E8DDD0; text-align: center; margin-bottom: 1.6rem; line-height: 1.6; }

div[role="radiogroup"] { display: flex; flex-direction: column; gap: 0.5rem; }
div[role="radiogroup"] label {
    background: transparent !important; border: 1px solid rgba(180,150,100,0.12) !important;
    border-radius: 0 !important; padding: 0.9rem 1.4rem !important; color: #B0A090 !important;
    font-family: 'Didact Gothic', sans-serif !important; font-size: 1rem !important;
    letter-spacing: 0.06em !important; transition: all 0.25s ease !important;
    cursor: pointer !important; text-align: center !important;
}
div[role="radiogroup"] label:hover {
    border-color: rgba(180,150,100,0.45) !important; color: #D4C9BC !important;
    background: rgba(180,150,100,0.03) !important;
}

.stTextArea textarea {
    background: rgba(180,150,100,0.02) !important; border: 1px solid rgba(180,150,100,0.2) !important;
    border-radius: 0 !important; color: #D4C9BC !important;
    font-family: 'EB Garamond', serif !important; font-size: 1.2rem !important;
    font-style: italic !important; line-height: 1.8 !important; padding: 1.2rem !important; resize: none !important;
}
.stTextArea textarea:focus { border-color: rgba(180,150,100,0.5) !important; box-shadow: none !important; }
.stTextArea textarea::placeholder { color: #3D342A !important; font-style: italic !important; }

.stButton > button {
    background: transparent !important; border: 1px solid rgba(180,150,100,0.4) !important;
    color: #B4966A !important; font-family: 'Didact Gothic', sans-serif !important;
    font-size: 0.82rem !important; font-weight: 400 !important; letter-spacing: 0.28em !important;
    text-transform: uppercase !important; padding: 1rem 2.5rem !important;
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
.accord-name-reveal { font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 300; color: #F2EBE0; letter-spacing: 0.06em; margin-bottom: 0.2rem; animation: fadeInUp 0.6s ease 1.4s both; }
.accord-family-reveal { font-size: 0.7rem; letter-spacing: 0.45em; color: #B4966A; text-transform: uppercase; margin-bottom: 1.4rem; animation: fadeInUp 0.6s ease 1.5s both; }
.accord-desc-reveal { font-family: 'EB Garamond', serif; font-size: 1.15rem; font-style: italic; color: #C9B89A; line-height: 1.75; margin-bottom: 1.6rem; animation: fadeInUp 0.6s ease 1.6s both; }

.notes-row { display: flex; gap: 0; margin-bottom: 1.5rem; border-top: 1px solid rgba(180,150,100,0.15); border-bottom: 1px solid rgba(180,150,100,0.15); padding: 1rem 0; animation: fadeInUp 0.6s ease 1.7s both; }
.note-col { flex: 1; text-align: center; padding: 0 0.5rem; }
.note-col + .note-col { border-left: 1px solid rgba(180,150,100,0.12); }
.note-label { font-size: 0.65rem; letter-spacing: 0.35em; color: #B4966A; text-transform: uppercase; margin-bottom: 0.4rem; }
.note-value { font-size: 0.85rem; color: #D4C9BC; line-height: 1.5; }

.engraved-section { background: #060504; border: 1px solid rgba(180,150,100,0.18); padding: 1.4rem; text-align: center; animation: fadeInUp 0.6s ease 1.9s both; position: relative; }
.engraved-section::before { content: '— ◆ —'; display: block; font-size: 0.5rem; color: rgba(180,150,100,0.4); letter-spacing: 0.4em; margin-bottom: 0.7rem; }
.engraved-section::after { content: '— ◆ —'; display: block; font-size: 0.5rem; color: rgba(180,150,100,0.4); letter-spacing: 0.4em; margin-top: 0.7rem; }
.engraved-name { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 300; font-style: italic; color: #D4B98A; animation: nameEngrave 1.2s cubic-bezier(0.22,1,0.36,1) 2.2s both; letter-spacing: 0.12em; }
.engraved-sub { font-size: 0.65rem; letter-spacing: 0.35em; color: #8A7A6A; text-transform: uppercase; margin-top: 0.5rem; animation: fadeInUp 0.6s ease 2.6s both; }
.clean-badge { display: inline-block; font-size: 0.65rem; letter-spacing: 0.25em; text-transform: uppercase; border: 1px solid rgba(74,124,89,0.4); color: #6A9C79; padding: 0.3rem 0.8rem; margin-top: 1.2rem; animation: fadeInUp 0.6s ease 2.4s both; }
.hashtag { font-size: 0.7rem; letter-spacing: 0.2em; color: #8A7A6A; text-transform: uppercase; margin-top: 1rem; animation: fadeInUp 0.6s ease 2.8s both; }

.stProgress > div > div { background: rgba(180,150,100,0.08) !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, #6B5040, #B4966A) !important; }

.intro-container { text-align: center; padding: 2rem 1rem 3rem; }
.intro-text { font-family: 'EB Garamond', serif; font-size: 1.5rem; font-style: italic; color: #C9B89A; line-height: 1.9; max-width: 380px; margin: 0 auto 2.5rem; }
.intro-detail { font-size: 0.78rem; letter-spacing: 0.3em; color: #8A7A6A; text-transform: uppercase; margin-bottom: 2rem; }

.mirror-prompt { background: rgba(180,150,100,0.02); border-left: 2px solid rgba(180,150,100,0.25); padding: 1.2rem 1.4rem; margin-bottom: 1.2rem; font-family: 'EB Garamond', serif; font-size: 1rem; font-style: italic; color: #B0A090; line-height: 1.7; }
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

STORY_KEYWORDS = {}  # Moved to ai_engine.py — kept empty here for reference

def analyze_and_build_result(story_text, ocasion, sentir):
    """Calls ai_engine.full_analysis — Claude API first, keyword fallback if no API key."""
    api_key = None
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        api_key = None

    return full_analysis(
        story=story_text,
        ocasion=ocasion,
        sentir=sentir,
        emotion_map=emotion_map,
        accord_lib=accord_lib,
        api_key=api_key,
    )

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
st.markdown('<div class="brand-tagline">Tu memoria hecha perfume</div>', unsafe_allow_html=True)
st.markdown('<div class="ornament">◆ ◆ ◆</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# STEP 0 — INTRO
# ══════════════════════════════════════════════════════════
if st.session_state.step == 0:
    st.markdown("""
    <div class="intro-container">
        <p class="intro-text">El espejo te escucha.<br>Cuéntale algo de ti.</p>
        <p class="intro-detail">Dos preguntas · Una historia · Tu perfume</p>
    </div>
    """, unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button("Comenzar"):
            st.session_state.step = 1
            st.rerun()

# ══════════════════════════════════════════════════════════
# STEP 1 — DOS PREGUNTAS
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    st.markdown('<div class="q-step">I · Contexto</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-text">¿Para qué momento es este perfume?</div>', unsafe_allow_html=True)
    ocasion = st.radio("ocasion", ["Para el día a día", "Para una noche especial", "Solo para mí"], label_visibility="collapsed")

    st.markdown('<div class="rule"><div class="rule-line"></div><div class="rule-diamond">◆</div><div class="rule-line"></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="q-step">II · Deseo</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-text">¿Cómo quieres sentirte al usarlo?</div>', unsafe_allow_html=True)
    sentir = st.radio("sentir", ["Poderosa e imparable", "Tranquila y en paz", "Libre y sin límites", "Misteriosa y profunda", "Luminosa y renovada"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continuar →"):
        st.session_state.ocasion = ocasion
        st.session_state.sentir = sentir
        st.session_state.step = 2
        st.rerun()

# ══════════════════════════════════════════════════════════
# STEP 2 — LA HISTORIA
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.markdown('<div class="q-step">III · El espejo te escucha</div>', unsafe_allow_html=True)
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
                result = analyze_and_build_result(historia, st.session_state.ocasion, st.session_state.sentir)
                st.session_state.result = result
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
            <div class="mirror-reading">El espejo lee tu historia...</div>
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
    suggested = r.get("suggested_names", MEMORY_TITLES.get(r["emotion"], ["Lo que fue mío", "Sin nombre aún", "El momento"]))

    st.markdown('<div class="q-step">IV · Tu grabado</div>', unsafe_allow_html=True)
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
        btn_label = "Grabar y revelar →" if titulo_final else "Elige un nombre primero"
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
                <div class="note-label">Salida</div>
                <div class="note-value">{notes_s}</div>
            </div>
            <div class="note-col">
                <div class="note-label">Corazón</div>
                <div class="note-value">{notes_c}</div>
            </div>
            <div class="note-col">
                <div class="note-label">Fondo</div>
                <div class="note-value">{notes_b}</div>
            </div>
        </div>
        <div class="engraved-section">
            <div class="engraved-name">{final_name}</div>
            <div class="engraved-sub">Grabado en tu botella</div>
        </div>
        <div style="text-align:center;">
            <div class="clean-badge">✦ Fórmula limpia · Recargable</div>
            <div class="hashtag">#MioUmore</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 — Ingredientes activos y sus beneficios emocionales
    INGREDIENT_BENEFITS = {
        "bergamota": {"activo": "Linalool + Limoneno", "beneficio": "Reduce ansiedad y eleva el ánimo", "origen": "Cítrico natural, Calabria"},
        "pomelo": {"activo": "Limoneno", "beneficio": "Energiza y aporta claridad mental", "origen": "Cítrico natural"},
        "mandarina": {"activo": "Limoneno + Gamma-terpineno", "beneficio": "Optimismo y vitalidad", "origen": "Cítrico natural"},
        "limón": {"activo": "Limoneno", "beneficio": "Energía y claridad mental", "origen": "Cítrico natural"},
        "rosa": {"activo": "Phenylethyl alcohol", "beneficio": "Romanticismo y calma interior", "origen": "Rosa centifolia, Grasse"},
        "jazmín": {"activo": "Hedione", "beneficio": "Atracción y luminosidad emocional", "origen": "Floral sintético-natural"},
        "jazmín sambac": {"activo": "Indol + Hedione", "beneficio": "Atracción, reduce el estrés", "origen": "Floral natural, India"},
        "lavanda": {"activo": "Linalool + Acetato de linalilo", "beneficio": "Relajación profunda, reduce el cortisol", "origen": "Floral natural, Provenza"},
        "neroli": {"activo": "Linalool + Nerolidol", "beneficio": "Serenidad y equilibrio emocional", "origen": "Flor de naranjo, Grasse"},
        "ylang-ylang": {"activo": "Germacreno + Linalool", "beneficio": "Sensualidad y calma", "origen": "Floral natural, Madagascar"},
        "geranio": {"activo": "Geraniol + Citronelol", "beneficio": "Equilibrio hormonal, frescura", "origen": "Floral-herbal natural"},
        "rosa de mayo": {"activo": "Phenylethyl alcohol", "beneficio": "Romanticismo y calma interior", "origen": "Rosa centifolia, Grasse"},
        "sándalo": {"activo": "Santalol alfa + beta", "beneficio": "Calma profunda, meditación", "origen": "Madera natural, India/Australia"},
        "cedro": {"activo": "Cedrol", "beneficio": "Estabilidad emocional y enfoque", "origen": "Madera natural, Atlas"},
        "vetiver": {"activo": "Vetiverol + Khusimol", "beneficio": "Conexión con la tierra, anti-ansiedad", "origen": "Raíz natural, Haití"},
        "patchouli": {"activo": "Patchoulol", "beneficio": "Grounding profundo, equilibrio", "origen": "Hoja natural, Indonesia"},
        "vainilla": {"activo": "Vanilina", "beneficio": "Nostalgia, confort, reduce la tensión", "origen": "Orquídea, Madagascar"},
        "canela": {"activo": "Cinamaldehído", "beneficio": "Calidez emocional y energía", "origen": "Corteza natural, Sri Lanka"},
        "cardamomo": {"activo": "1,8-Cineol + Acetato de terpinilo", "beneficio": "Claridad mental y calidez", "origen": "Especia natural, Guatemala"},
        "pimienta negra": {"activo": "Piperina + Beta-cariofileno", "beneficio": "Energía y determinación", "origen": "Especia natural, India"},
        "pimienta rosa": {"activo": "Limoneno + Mirceno", "beneficio": "Frescura delicada y alegría", "origen": "Baya natural, Brasil"},
        "ámbar": {"activo": "Ambroxan", "beneficio": "Sensualidad y calidez envolvente", "origen": "Molécula sustentable"},
        "almizcle blanco": {"activo": "Galaxolide", "beneficio": "Limpieza emocional, suavidad", "origen": "Molécula sintética limpia"},
        "Iso E Super": {"activo": "Iso E Super", "beneficio": "Calidez de piel, efecto magnético", "origen": "Molécula de autor"},
        "hoja verde": {"activo": "Cis-3-hexenol", "beneficio": "Frescura vital, conexión con naturaleza", "origen": "Molécula verde natural"},
        "musgo de roble": {"activo": "Evernyl (oakmoss sintético)", "beneficio": "Profundidad terrosa, nostalgia", "origen": "Sintético sustentable (IFRA safe)"},
        "nenúfar": {"activo": "Hedione + notas acuáticas", "beneficio": "Frescura acuática y serenidad", "origen": "Acorde floral-acuático"},
        "sal marina": {"activo": "Calone + minerales", "beneficio": "Esperanza, amplitud emocional", "origen": "Molécula marina"},
    }

    # Collect all notes from the accord
    all_notes = []
    for layer in ["salida", "corazon", "base"]:
        all_notes.extend(accord.get("notas", {}).get(layer, []))

    # Find matching ingredients with benefits
    active_ingredients = []
    for note in all_notes:
        note_lower = note.lower()
        for key, info in INGREDIENT_BENEFITS.items():
            if isinstance(info, dict) and key.lower() in note_lower:
                active_ingredients.append({"nota": note, **info})
                break

    if active_ingredients:
        for ing in active_ingredients[:4]:
            st.markdown(f"""
            <div style="padding:0.8rem 0;border-bottom:1px solid rgba(180,150,100,0.08);">
                <div style="font-family:'Playfair Display',serif;font-size:1rem;color:#D4C9BC;margin-bottom:0.25rem;">
                    {ing['nota']}
                </div>
                <div style="font-size:0.75rem;color:#B4966A;letter-spacing:0.03em;margin-bottom:0.2rem;">
                    Activo: {ing['activo']}
                </div>
                <div style="font-family:'EB Garamond',serif;font-size:0.88rem;font-style:italic;color:#C9B89A;">
                    ✦ {ing['beneficio']}
                </div>
                <div style="font-size:0.6rem;color:#8A7A6A;letter-spacing:0.15em;margin-top:0.2rem;">
                    {ing['origen']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Crear otro perfume"):
        st.session_state.step = 0
        st.session_state.result = None
        st.session_state.final_name = ""
        st.rerun()

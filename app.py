import streamlit as st
import time

# --- Seite Konfiguration ---
st.set_page_config(page_title="Pro FlipClock Timer", layout="centered")

# --- Custom CSS für das Design & Animation ---
st.markdown("""
    <style>
    /* Hintergrund & Textfarben */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }

    /* Animation für den Flip-Effekt */
    @keyframes flipDown {
        0% { transform: rotateX(0deg); }
        50% { transform: rotateX(-90deg); background-color: #333; }
        100% { transform: rotateX(0deg); }
    }

    .flip-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 50px;
        perspective: 1000px;
    }

    .flip-card {
        background-color: #1a1a1a;
        border-radius: 12px;
        width: 140px;
        height: 180px;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #333;
        animation: flipDown 0.4s ease-in-out;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.8);
    }

    /* Der weiße Trennstrich in der Mitte */
    .flip-card::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 3px;
        background-color: rgba(255, 255, 255, 0.5);
        z-index: 5;
    }

    .time-val {
        font-size: 110px;
        font-weight: 900;
        color: #ffffff;
        font-family: 'Arial Black', sans-serif;
    }

    .time-label {
        text-align: center;
        font-size: 14px;
        color: #666;
        margin-top: 15px;
        letter-spacing: 2px;
        font-weight: bold;
    }

    /* Styling für die Eingabefelder im Setup */
    .stNumberInput div div input {
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }

    /* Button Design */
    .stButton>button {
        background-color: #ffffff;
        color: #000000;
        border-radius: 8px;
        font-weight: bold;
        padding: 15px 30px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #cccccc;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State Management ---
if 'mode' not in st.session_state:
    st.session_state.mode = "setup"

# --- MODUS 1: SETUP ---
if st.session_state.mode == "setup":
    st.markdown("<h1 style='text-align: center; letter-spacing: 5px;'>TIMER</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        h = st.number_input("Stunden", min_value=0, max_value=23, value=None, placeholder="0")
    with col2:
        m = st.number_input("Minuten", min_value=0, max_value=59, value=None, placeholder="0")
    with col3:
        s = st.number_input("Sekunden", min_value=0, max_value=59, value=None, placeholder="0")
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("START"):
        # Umwandlung von None zu 0 für die Berechnung
        h_val = h if h is not None else 0
        m_val = m if m is not None else 0
        s_val = s if s is not None else 0
        
        total_seconds = (h_val * 3600) + (m_val * 60) + s_val
        
        if total_seconds > 0:
            st.session_state.total = total_seconds
            st.session_state.start_time = time.time()
            st.session_state.mode = "timer"
            st.rerun()
        else:
            st.error("Bitte gib eine Zeit ein.")

# --- MODUS 2: TIMER (FLIP CLOCK) ---
elif st.session_state.mode == "timer":
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, int(st.session_state.total - elapsed))
    
    if remaining <= 0:
        st.session_state.mode = "stretch"
        

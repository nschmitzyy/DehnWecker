import streamlit as st
import time

# --- Seite Konfiguration ---
st.set_page_config(page_title="FlipClock Timer", layout="centered")

# --- Custom CSS für FlipClock & Schwarz/Weiß Design ---
st.markdown("""
    <style>
    /* Gesamter Hintergrund Schwarz */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }

    /* Input Felder Styling */
    .stNumberInput div div input {
        background-color: #111;
        color: white !important;
        border: 1px solid #333;
    }

    /* FlipClock Container */
    .flip-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 50px;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Einzelne Zeit-Blöcke */
    .time-block {
        background-color: #222;
        border-radius: 10px;
        padding: 20px;
        min-width: 120px;
        text-align: center;
        border: 1px solid #444;
    }

    .time-val {
        font-size: 80px;
        font-weight: bold;
        color: #ffffff;
        line-height: 1;
    }

    .time-label {
        font-size: 14px;
        text-transform: uppercase;
        color: #888;
        margin-top: 5px;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        background-color: #ffffff;
        color: #000000;
        border-radius: 5px;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #cccccc;
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State Initialisierung ---
if 'mode' not in st.session_state:
    st.session_state.mode = "setup"
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0

# --- MODUS 1: Setup (Zeit auswählen) ---
if st.session_state.mode == "setup":
    st.markdown("<h1 style='text-align: center;'>TIMER SETUP</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        hours = st.number_input("Stunden", min_value=0, max_value=23, value=0)
    with col2:
        minutes = st.number_input("Minuten", min_value=0, max_value=59, value=45)
    with col3:
        seconds = st.number_input("Sekunden", min_value=0, max_value=59, value=0)
    
    if st.button("STARTEN"):
        total = (hours * 3600) + (minutes * 60) + seconds
        if total > 0:
            st.session_state.total_seconds = total
            st.session_state.start_time = time.time()
            st.session_state.mode = "timer"
            st.rerun()
        else:
            st.warning("Bitte stelle eine Zeit ein.")

# --- MODUS 2: FlipClock Timer ---
elif st.session_state.mode == "timer":
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, st.session_state.total_seconds - int(elapsed))
    
    if remaining <= 0:
        st.session_state.mode = "stretch"
        st.rerun()
    
    # Zeit berechnen für Anzeige
    h = remaining // 3600
    m = (remaining % 3600) // 60
    s = remaining % 60

    # FlipClock HTML Rendering
    st.markdown(f"""
        <div class="flip-container">
            <div class="time-block">
                <div class="time-val">{h:02d}</div>
                <div class="time-label">STUNDEN</div>
            </div>
            <div class="time-block">
                <div class="time-val">{m:02d}</div>
                <div class="time-label">MINUTEN</div>
            </div>
            <div class="time-block">
                <div class="time-val">{s:02d}</div>
                <div class="time-label">SEKUNDEN</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("<br><br>", unsafe_allow_html=True)
    if st.button("ABBRECHEN"):
        st.session_state.mode = "setup"
        st.rerun()
    
    time.sleep(1)
    st.rerun()

# --- MODUS 3: Stretching ---
elif st.session_state.mode == "stretch":
    st.markdown("<h1 style='text-align: center; color: red;'>ZEIT ABGELAUFEN</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>Bitte führe jetzt die Vorwärtsbeuge aus.</p>", unsafe_allow_html=True)
    
    # Hier kommt später MediaPipe rein
    st.markdown("<div style='height: 300px; border: 2px dashed #444; display: flex; align-items: center; justify-content: center;'>KAMERA AKTIV...</div>", unsafe_allow_html=True)
    
    if st.button("FERTIG"):
        st.session_state.mode = "setup"
        st.rerun()

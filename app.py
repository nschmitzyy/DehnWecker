import streamlit as st
import time

# --- Seite Konfiguration ---
st.set_page_config(page_title="Pro FlipClock", layout="centered")

# --- Custom CSS für echten Animations-Effekt ---
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }

    /* Flip-Animation Keyframes */
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
        perspective: 1000px; /* Erzeugt 3D-Tiefe für den Flip */
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
        /* Die Animation wird bei jedem Rerender kurz getriggert */
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
        background-color: rgba(255, 255, 255, 0.6);
        z-index: 5;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
    }

    .time-val {
        font-size: 120px;
        font-weight: 900;
        color: #ffffff;
        font-family: 'Arial Black', sans-serif;
    }

    .time-label {
        text-align: center;
        font-size: 14px;
        color: #555;
        margin-top: 15px;
        letter-spacing: 2px;
        font-weight: bold;
    }

    /* Button Design */
    .stButton>button {
        background-color: #ffffff;
        color: #000000;
        border-radius: 8px;
        font-weight: bold;
        padding: 15px 30px;
        border: none;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #4da6ff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- App Logik (Session State) ---
if 'mode' not in st.session_state:
    st.session_state.mode = "setup"

# --- SETUP MODUS ---
if st.session_state.mode == "setup":
    st.markdown("<h1 style='text-align: center;'>TIMER KONFIGURATION</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: h = st.number_input("Std", 0, 23, 0)
    with c2: m = st.number_input("Min", 0, 59, 45)
    with c3: s = st.number_input("Sek", 0, 59, 0)
    
    if st.button("START"):
        st.session_state.total = (h * 3600) + (m * 60) + s
        st.session_state.start_time = time.time()
        st.session_state.mode = "timer"
        st.rerun()

# --- TIMER MODUS ---
elif st.session_state.mode == "timer":
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, int(st.session_state.total - elapsed))
    
    if rem <= 0:
        st.session_state.mode = "stretch"
        st.rerun()
    
    hrs, mins, secs = rem // 3600, (rem % 3600) // 60, rem % 60

    # FlipClock HTML mit Animation
    st.markdown(f"""
        <div class="flip-container">
            <div>
                <div class="flip-card"><div class="time-val">{hrs:02d}</div></div>
                <div class="time-label">STUNDEN</div>
            </div>
            <div>
                <div class="flip-card"><div class="time-val">{mins:02d}</div></div>
                <div class="time-label">MINUTEN</div>
            </div>
            <div>
                <div class="flip-card"><div class="time-val">{secs:02d}</div></div>
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

# --- STRETCH MODUS ---
elif st.session_state.mode == "stretch":
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🚨 ZEIT ZUM DEHNEN!</h1>", unsafe_allow_html=True)
    if st.button("ERLEDIGT"):
        st.session_state.mode = "setup"
        st.rerun()

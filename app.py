import streamlit as st
import time

# --- Seite Konfiguration ---
st.set_page_config(page_title="FlipClock Timer", layout="centered")

# --- Custom CSS für echten Flip-Look ---
st.markdown("""
    <style>
    /* Hintergrund Schwarz */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }

    /* FlipClock Container */
    .flip-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 50px;
        font-family: 'Helvetica', sans-serif;
    }

    /* Der Karten-Block */
    .flip-card {
        background-color: #1a1a1a;
        border-radius: 8px;
        width: 140px;
        height: 160px;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #333;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.5);
    }

    /* Der Flip-Strich in der Mitte */
    .flip-card::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 2px;
        background-color: rgba(255, 255, 255, 0.4); /* Dünner weißer Strich */
        z-index: 2;
    }

    .time-val {
        font-size: 110px;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -2px;
    }

    .time-label {
        text-align: center;
        font-size: 12px;
        color: #666;
        margin-top: 10px;
        font-weight: bold;
    }

    /* Eingabefelder Styling */
    .stNumberInput div div input {
        background-color: #111 !important;
        color: white !important;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #ffffff;
        color: #000000;
        border-radius: 4px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State ---
if 'mode' not in st.session_state:
    st.session_state.mode = "setup"
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0

# --- SETUP MODUS ---
if st.session_state.mode == "setup":
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>ZEIT EINSTELLEN</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        h_in = st.number_input("Stunden", 0, 23, 0)
    with col2:
        m_in = st.number_input("Minuten", 0, 59, 45)
    with col3:
        s_in = st.number_input("Sekunden", 0, 59, 0)
    
    if st.button("START"):
        total = (h_in * 3600) + (m_in * 60) + s_in
        if total > 0:
            st.session_state.total_seconds = total
            st.session_state.start_time = time.time()
            st.session_state.mode = "timer"
            st.rerun()

# --- TIMER MODUS ---
elif st.session_state.mode == "timer":
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, st.session_state.total_seconds - int(elapsed))
    
    if rem <= 0:
        st.session_state.mode = "stretch"
        st.rerun()
    
    hrs = rem // 3600
    mins = (rem % 3600) // 60
    secs = rem % 60

    # FlipClock HTML
    st.markdown(f"""
        <div class="flip-container">
            <div>
                <div class="flip-card"><div class="time-val">{hrs:02d}</div></div>
                <div class="time-label">HOURS</div>
            </div>
            <div>
                <div class="flip-card"><div class="time-val">{mins:02d}</div></div>
                <div class="time-label">MINUTES</div>
            </div>
            <div>
                <div class="flip-card"><div class="time-val">{secs:02d}</div></div>
                <div class="time-label">SECONDS</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("<br><br>", unsafe_allow_html=True)
    if st.button("RESET"):
        st.session_state.mode = "setup"
        st.rerun()
    
    time.sleep(1)
    st.rerun()

# --- STRETCH MODUS ---
elif st.session_state.mode == "stretch":
    st.markdown("<h1 style='text-align: center; color: red;'>DEHNEN!</h1>", unsafe_allow_html=True)
    if st.button("FERTIG"):
        st.session_state.mode = "setup"
        st.rerun()

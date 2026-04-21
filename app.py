import streamlit as st
import time

# --- Konfiguration ---
st.set_page_config(page_title="Dehn-Timer", layout="centered")

# Initialisierung der Zustände
if 'mode' not in st.session_state:
    st.session_state.mode = "setup"  # Modi: setup, timer, stretch
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# --- FUNKTIONEN ---
def start_timer(duration_min):
    st.session_state.duration_sec = duration_min * 60
    st.session_state.start_time = time.time()
    st.session_state.mode = "timer"

def reset_app():
    st.session_state.mode = "setup"
    st.session_state.start_time = None

# --- LAYOUT & LOGIK ---
st.title("🧘 Dein Dehn-Assistent")

# MODUS 1: Setup (Timer einstellen)
if st.session_state.mode == "setup":
    st.write("Wie lange möchtest du am Handy arbeiten, bevor du dich dehnen musst?")
    minutes = st.number_input("Minuten:", min_value=1, max_value=120, value=45)
    if st.button("Timer starten"):
        start_timer(minutes)
        st.rerun()

# MODUS 2: Timer läuft
elif st.session_state.mode == "timer":
    elapsed = time.time() - st.session_state.start_time
    remaining = st.session_state.duration_sec - elapsed
    
    if remaining <= 0:
        st.session_state.mode = "stretch"
        st.rerun()
    else:
        st.subheader("⏳ Fokus-Zeit aktiv")
        st.metric("Verbleibende Zeit", f"{int(remaining // 60):02d}:{int(remaining % 60):02d}")
        st.progress(min(elapsed / st.session_state.duration_sec, 1.0))
        
        if st.button("Abbrechen"):
            reset_app()
            st.rerun()
        
        # Automatische Aktualisierung alle Sekunde
        time.sleep(1)
        st.rerun()

# MODUS 3: Dehnen (Die "Sperre")
elif st.session_state.mode == "stretch":
    st.error("🚨 ZEIT ABGELAUFEN! 🚨")
    st.header("Übung: Vorwärtsbeuge")
    st.write("Bitte dehne dich jetzt, um den Timer zu beenden.")
    
    # Platzhalter für MediaPipe Kamera-Analyse
    st.image("https://via.placeholder.com/640x480.png?text=Kamera+wird+aktiviert...", use_container_width=True)
    
    # In einem späteren Schritt ersetzen wir diesen Button durch die MediaPipe-Logik
    if st.button("Ich habe mich gedehnt (Fertig)"):
        st.balloons()
        reset_app()
        st.rerun()

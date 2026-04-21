import streamlit as st
import time

# --- Seite Konfiguration ---
st.set_page_config(
    page_title="Stretching Timer Layout",
    page_icon="🧘",
    layout="wide"
)

# --- Layout ---
st.title("🧘 AI Stretching Trainer")
st.write("Dies ist ein Layout-Entwurf ohne KI-Logik.")

col_video, col_stats = st.columns([2, 1])

with col_video:
    st.subheader("Kamera-Vorschau")
    # Ein Platzhalter-Bild statt einer echten Kamera
    st.image("https://via.placeholder.com/640x480.png?text=Kamera+Vorschau+Layout", use_container_width=True)
    st.info("Hier wird später dein Video-Feed mit MediaPipe-Analyse zu sehen sein.")

with col_stats:
    st.subheader("Workout Status")
    st.metric(label="Ziel-Winkel", value="< 135°")
    st.metric(label="Zeit", value="00:00")
    
    st.write("Fortschritt:")
    st.progress(0)
    
    if st.button("Simulation starten"):
        st.write("Simuliere Dehnung...")

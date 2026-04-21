import streamlit as st
import time

# --- Seite Konfiguration ---
st.set_page_config(
    page_title="Stretching Timer Layout",
    page_icon="🧘",
    layout="wide" # Nutzt die volle Breite des Bildschirms
)

# --- Sidebar (Einstellungen) ---
with st.sidebar:
    st.title("⚙️ Einstellungen")
    st.write("Konfiguriere dein Workout")
    
    # Übungsauswahl
    exercise = st.selectbox(
        "Wähle eine Übung:",
        ["Vorwärtsbeuge", "Herabschauender Hund", "Kobra"]
    )
    
    # Dauer Slider
    duration = st.slider("Dauer (Sekunden)", 5, 120, 30)
    
    # Schwierigkeit
    threshold = st.slider("Ziel-Winkel (Flexibilität)", 90, 160, 135)
    
    st.divider()
    if st.button("Workout zurücksetzen"):
        st.rerun()

# --- Hauptbereich ---
st.title("🧘 AI Stretching Trainer")
st.markdown(f"### Aktuelle Übung: **{exercise}**")

# Spalten-Layout erstellen
col_video, col_stats = st.columns([2, 1])

with col_video:
    # Platzhalter für den Kamera-Feed
    st.subheader("Kamera-Feed")
    # Ein graues Rechteck als Platzhalter simulieren
    st.image("https://via.placeholder.com/640x480.png?text=Kamera+Vorschau+kommt+hier", use_container_width=True)
    
    st.caption(f"Status: Warte darauf, dass der Winkel kleiner als {threshold}° wird...")

with col_stats:
    st.subheader("Dein Fortschritt")
    
    # Metriken anzeigen
    st.metric(label="Aktueller Winkel", value="175°", delta="-5°")
    st.metric(label="Gehaltene Zeit", value="0s", delta="Startbereit")
    
    # Fortschrittsbalken
    st.write("Fortschritt der Dehnung:")
    progress_bar = st.progress(0)
    
    # Beispielhafter "Start" Button zum Testen des UI-Verhaltens
    if st.button("Simuliere 30s Dehnung"):
        for i in range(100):
            time.sleep(0.1)
            progress_bar.progress(i + 1)
        st.balloons()
        st.success("Übung abgeschlossen!")

# --- Fußzeile ---
st.divider()
st.info("💡 Tipp: Stelle dein Handy so auf, dass dein ganzer Körper von der Seite sichtbar ist.")

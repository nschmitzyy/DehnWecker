Das ist eine fantastische Idee! Ein "Wald-Layout" verleiht der App eine beruhigende, naturverbundene Atmosphäre – perfekt für ein Stretching-Workout.

Da Streamlit von Haus aus eher schlicht ist, nutzen wir Custom CSS, um das Aussehen komplett zu verändern. Wir können Hintergründe anpassen und den Fortschrittsbalken (deinen Fluss) stylen.

Hier ist der komplette Code für dein Wald-Design:
1. Die Datei: app.py
Python

import streamlit as st
import time

# --- Seite Konfiguration ---
st.set_page_config(page_title="Wald-Dehn-Timer", layout="centered")

# --- Custom CSS für das Wald-Design ---
st.markdown("""
    <style>
    /* Hintergrund des Hauptfensters (Wald-Farben) */
    .stApp {
        background: linear-gradient(to bottom, #2d5a27, #1e3a1a);
        color: #f0f2f6;
    }

    /* Styling für den "Fluss" (Fortschrittsbalken) */
    .stProgress > div > div > div > div {
        background-color: #4da6ff; /* Hellblau wie Wasser */
        background-image: linear-gradient(90deg, #4da6ff 0%, #0066cc 100%);
        border-radius: 10px;
    }
    
    /* Container für den Fluss */
    .stProgress {
        height: 25px;
        border-radius: 15px;
        background-color: #3d2b1f; /* Dunkelbraun wie Erde/Ufer */
        border: 2px solid #5d4037;
    }

    /* Überschriften-Styling */
    h1, h2, h3 {
        color: #e8f5e9 !important;
        font-family: 'Trebuchet MS', sans-serif;
    }
    
    /* Buttons wie Moos/Steine */
    .stButton>button {
        background-color: #4caf50;
        color: white;
        border-radius: 20px;
        border: 2px solid #2e7d32;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #81c784;
        border-color: #4caf50;
    }
    </style>
    """, unsafe_allow_stdio=True)

# --- Session State Initialisierung ---
if 'mode' not in st.session_state:
    st.session_state.mode = "setup"
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# --- Layout & Logik ---
st.title("🌲 Der digitale Wald-Pfad")

if st.session_state.mode == "setup":
    st.markdown("### Wie lange möchtest du im Wald verweilen?")
    minutes = st.number_input("Minuten bis zur Dehnung:", min_value=1, value=45)
    
    if st.button("Pfad betreten"):
        st.session_state.duration_sec = minutes * 60
        st.session_state.start_time = time.time()
        st.session_state.mode = "timer"
        st.rerun()

elif st.session_state.mode == "timer":
    elapsed = time.time() - st.session_state.start_time
    remaining = st.session_state.duration_sec - elapsed
    
    if remaining <= 0:
        st.session_state.mode = "stretch"
        st.rerun()
    else:
        st.subheader("💧 Der Fluss der Zeit fließt...")
        
        # Der "Fluss" (Progress Bar)
        progress = min(elapsed / st.session_state.duration_sec, 1.0)
        st.progress(progress)
        
        mins, secs = divmod(int(remaining), 60)
        st.write(f"⏳ Noch **{mins:02d}:{secs:02d}** bis zur Rast (Dehnung).")
        
        if st.button("Wald verlassen (Abbrechen)"):
            st.session_state.mode = "setup"
            st.rerun()
        
        time.sleep(1)
        st.rerun()

elif st.session_state.mode == "stretch":
    st.markdown("## 🛑 Zeit für eine Lichtung!")
    st.write("Der Fluss ist am Meer angekommen. Dehne dich jetzt (Vorwärtsbeuge).")
    
    # Platzhalter für MediaPipe
    st.markdown("""
        <div style="border: 5px solid #4caf50; border-radius: 10px; padding: 20px; text-align: center; background-color: rgba(255,255,255,0.1);">
            <p>📷 Kamera-Aktivierung...</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Dehnung abgeschlossen 🌿"):
        st.balloons()
        st.session_state.mode = "setup"
        st.rerun()

import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import mediapipe as mp
import cv2
import numpy as np
import time

# --- MediaPipe Initialisierung ---
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    """Berechnet den Winkel zwischen drei Punkten (Schulter, Hüfte, Knie)."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# --- Streamlit UI ---
st.set_page_config(page_title="AI Dehn-Trainer", layout="centered")
st.title("🧘 Dein AI Dehn-Workout")
st.subheader("Übung: Vorwärtsbeuge")

# Anleitung & Einstellungen
st.info("Beuge dich nach vorne (Hüftwinkel < 135°), um den Timer zu starten.")
target_time = st.sidebar.slider("Haltezeit (Sekunden)", 5, 60, 20)
threshold_angle = st.sidebar.slider("Start-Winkel (Sensibilität)", 90, 160, 135)

# Session State für den Timer
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'success' not in st.session_state:
    st.session_state.success = False

class YogaTransformer(VideoTransformerBase):
    def __init__(self):
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        h, w, _ = image.shape
        pose_detected = False

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Koordinaten extrahieren (Rechte Seite)
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

            angle = calculate_angle(shoulder, hip, knee)

            # Visualisierung des Winkels
            cv2.putText(image, f"Winkel: {int(angle)} deg", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Logik: Ist der Nutzer tief genug?
            if angle < threshold_angle:
                pose_detected = True
                cv2.rectangle(image, (0, h-50), (w, h), (0, 255, 0), -1)
                cv2.putText(image, "TIMER LAEUFT...", (w//4, h-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
            else:
                cv2.rectangle(image, (0, h-50), (w, h), (0, 0, 255), -1)
                cv2.putText(image, "BITTE WEITER BEUGEN", (w//6, h-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            # Landmarks zeichnen
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Timer-Verarbeitung (Simplifiziert für das Video-Overlay)
        return cv2.flip(image, 1)

# --- WebRTC Streamer ---
webrtc_streamer(
    key="yoga-timer",
    mode=WebRtcMode.SENDRECV,
    video_transformer_factory=YogaTransformer,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
)

st.write("---")
st.write("Sobald du fertig bist, erscheinen hier die Glückwünsche!")

# --- SETUP MODUS (Angepasst) ---
if st.session_state.mode == "setup":
    st.markdown("<h1 style='text-align: center;'>TIMER KONFIGURATION</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # 'value=None' sorgt dafür, dass das Feld leer startet
        # 'placeholder="0"' zeigt eine graue Null, die beim Tippen verschwindet
        h = st.number_input("Std", min_value=0, max_value=23, value=None, placeholder="0")
    
    with c2:
        m = st.number_input("Min", min_value=0, max_value=59, value=None, placeholder="0")
    
    with c3:
        s = st.number_input("Sek", min_value=0, max_value=59, value=None, placeholder="0")
    
    if st.button("START"):
        # Wir müssen sicherstellen, dass None als 0 gezählt wird
        h_val = h if h is not None else 0
        m_val = m if m is not None else 0
        s_val = s if s is not None else 0
        
        total_input = (h_val * 3600) + (m_val * 60) + s_val
        
        if total_input > 0:
            st.session_state.total = total_input
            st.session_state.start_time = time.time()
            st.session_state.mode = "timer"
            st.rerun()
        else:
            st.warning("Bitte gib eine Zeit ein, um den Pfad zu starten.")

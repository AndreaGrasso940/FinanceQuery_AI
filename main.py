import streamlit as st
import pandas as pd
from llm_agent import analizza_dati_con_llm

# Configurazione della pagina
st.set_page_config(page_title="AI Finance Tracker", page_icon="💶", layout="centered")

st.title("💶 Assistente Finanziario AI")
st.markdown("Usa il modello Qwen 2.5 in locale per analizzare il tuo bilancio.")

# Gestione della memoria (Session State) per la cronologia della chat e il dataframe
if "cronologia" not in st.session_state:
    st.session_state.cronologia = []

if "df" not in st.session_state:
    st.session_state.df = None

# --- STEP 1: UPLOAD DEL FILE ---
if st.session_state.df is None:
    st.info("Step 1: Carica il tuo foglio Excel per iniziare.")
    file_caricato = st.file_uploader("Trascina qui il file .xlsx", type=["xlsx"])
    
    if file_caricato is not None:
        # Leggiamo il file e lo salviamo nella sessione
        st.session_state.df = pd.read_excel(file_caricato)
        st.success("File caricato e analizzato correttamente! Clicca il pulsante qui sotto per avviare la chat.")
        if st.button("Inizia ad analizzare"):
            st.rerun()

# --- STEP 2: CHAT CON I DATI ---
else:
    st.success(f"Dati attivi: tabellone da {len(st.session_state.df)} righe.")
    
    # Pulsante per resettare e caricare un nuovo file
    if st.sidebar.button("🔄 Carica un nuovo file"):
        st.session_state.df = None
        st.session_state.cronologia = []
        st.rerun()

    # Mostra i messaggi passati
    for messaggio in st.session_state.cronologia:
        with st.chat_message(messaggio["ruolo"]):
            st.markdown(messaggio["contenuto"])

    # Input dell'utente
    domanda_utente = st.chat_input("Es. Quali sono i costi che incidono maggiormente?")
    
    if domanda_utente:
        # Mostra la domanda dell'utente
        st.chat_message("user").markdown(domanda_utente)
        st.session_state.cronologia.append({"ruolo": "user", "contenuto": domanda_utente})
        
        # Mostra uno spinner di caricamento mentre il modello pensa
        with st.spinner("L'agente sta analizzando i dati in locale..."):
            risposta_ai = analizza_dati_con_llm(st.session_state.df, domanda_utente)
            
        # Mostra la risposta dell'AI
        st.chat_message("assistant").markdown(risposta_ai)
        st.session_state.cronologia.append({"ruolo": "assistant", "contenuto": risposta_ai})

import streamlit as st
import pandas as pd
from llm_agent import analyze_data_with_llm

# Page Configuration
st.set_page_config(page_title="FinanceQuery_AI", layout="centered")

st.title("FinanceQuery_AI")
st.markdown("Use the local llama 3.2 model to analyze your budget.")

# Session State management for chat history and dataframe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "df" not in st.session_state:
    st.session_state.df = None

# --- STEP 1: FILE UPLOAD ---
if st.session_state.df is None:
    st.info("Step 1: Upload your Excel file to start.")
    uploaded_file = st.file_uploader("Drag and drop the .xlsx file here", type=["xlsx", "csv"])

    if uploaded_file is not None:
        # Read the file and save it in the session
        st.session_state.df = pd.read_excel(uploaded_file)
        st.success("File uploaded and analyzed successfully! Click the button below to start the chat.")
        if st.button("Start Analyzing"):
            st.rerun()

# --- STEP 2: CHAT WITH DATA ---
else:
    st.success(f"Active data: board with {len(st.session_state.df)} rows.")

    # Button to reset and upload a new file
    if st.sidebar.button("Upload a new file"):
        st.session_state.df = None
        st.session_state.chat_history = []
        st.rerun()

    # Display past messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_question = st.chat_input("E.g., Calculate the sum of [Column A] where [Column B] is [Value]'")

    if user_question:
        # Display user question
        st.chat_message("user").markdown(user_question)
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        # Display loading spinner while the model thinks
        with st.spinner("The agent is analyzing the data locally..."):
            ai_response = analyze_data_with_llm(st.session_state.df, user_question)

        # Display AI response
        st.chat_message("assistant").markdown(ai_response)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

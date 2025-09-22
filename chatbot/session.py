import streamlit as st

def init_session_state():
    if "step" not in st.session_state:
        st.session_state.step = "greet"
    if "candidate_info" not in st.session_state:
        st.session_state.candidate_info = None
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "current_q_index" not in st.session_state:
        st.session_state.current_q_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []

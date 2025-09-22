import streamlit as st
from chatbot.session import init_session_state
from chatbot.ui import render_ui

def main():
    st.set_page_config(page_title="TalentScout Hiring Assistant")
    init_session_state()
    render_ui()

if __name__ == "__main__":
    main()

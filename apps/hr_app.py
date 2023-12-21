import streamlit as st
from apps.hr import resume_review, landing, chat


def app():
    tab1, tab2, tab3 = st.tabs(["About", "PolicyPal", "IntelliHire"])

    with tab1:
        landing.app()

    with tab2:
        chat.app()

    with tab3:
        resume_review.app()


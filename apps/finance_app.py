import streamlit as st
from apps.finance import chat, landing, invoice


def app():
    tab1, tab2, tab3 = st.tabs(["About", "Finance Genie", "Invoice Analyzer"])

    with tab1:
        landing.app()

    with tab2:
        chat.app()

    with tab3:
        invoice.main()



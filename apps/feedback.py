import streamlit as st


def app():

    st.title('Feedback')

    st.write(
        f'<iframe src = "https://trubrics.streamlit.app/Feedback/?embed=true" \
        width="1000" \
        height = "1000" \
        style = "width:100%;border:none;"> </iframe>',
        unsafe_allow_html=True,
    )


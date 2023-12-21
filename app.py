import streamlit as st
from streamlit_option_menu import option_menu
# from multiapp import MultiApp
from apps import news, feedback, finance_app, legal_app, hr_app
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader


with open('secrets.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login('Accio Login', 'main')

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome to Accio, *{st.session_state["name"]}*')
    # image = Image.open("assets/acciologo.png").resize((680, 120))
    # st.image(image)
    # st.markdown("Uniting Intelligence at your Command!")

    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='Accio',
                options=['Trending News', 'HR', 'Legal', 'Finance', 'Feedback'],
                icons=['house', 'person-circle','trophy-fill', 'bank', 'chat-fill'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": "black"},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"background-color": "#02ab21"}, }

            )

        if app == 'Trending News':
            news.app()

        if app == 'HR':
            hr_app.app()

        if app == 'Legal':
            legal_app.app()

        if app == 'Finance':
            finance_app.app()

        if app == 'Feedback':
            feedback.app()


    run()

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

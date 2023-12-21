import streamlit as st


def app():
    intro = '''
    # Accio HR

    Welcome to Accio HR! 🤖✨

    When using our chatbot for HR document review, you can ask a variety of questions to extract specific information, 
    analyze policies, and learn more.Our IntelliHire helps you find the right talent for the team.

    ## Features

    - 📝 **Ask Questions**: Interact with the chatbot by asking questions related to HR policies
    - 🕵️ **Extract Information**: The chatbot will extract specific details from the policies text to provide insights.
    #IntelliHire

    - 🧐 **Analyze Resume**: Get a detailed analysis of candidate resumes with respect to the Job Description.

    - 🚨 **Assess candidate Skills**: Evaluates the overall candidates relevance  and ranks their skillset.

     ## Get Started Today! 🚀
    '''

    st.markdown(intro)
import streamlit as st


def app():
    intro = '''
    # Accio Legal

    Welcome to  Accio Legal! 🤖✨

    When using a chatbot for legal document review, you can ask a variety of questions to extract specific information, 
    analyze clauses, and assess the overall compliance and risks associated with a legal contract.

    ## Features

    - 📝 **Ask Questions**: Interact with the chatbot by asking questions related to contract review.

    - 🕵️ **Extract Information**: The chatbot will extract specific details from the contract text to provide insights.

    - 🧐 **Analyze Clauses**: Get a detailed analysis of different clauses within the contract.

    - 🚨 **Assess Risks and Compliance**: Evaluate the overall compliance and risks associated with the contract.

    '''
    st.markdown(intro)


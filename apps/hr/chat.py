import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from apps.html_template import css, bot_template, user_template
import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain import SagemakerEndpoint
import json
import random


from trubrics.integrations.streamlit import FeedbackCollector

endpoint_name = "huggingface-pytorch-tgi-inference-2023-12-15-22-42-02-827"
region = 'us-east-1'

collector = FeedbackCollector(
    email=st.secrets.TRUBRICS_EMAIL,
    password=st.secrets.TRUBRICS_PASSWORD,
    project="default"
)


def get_vectorstore():
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    client = chromadb.HttpClient(host='localhost', port=8000)  # settings=Settings(allow_reset=True))

    vectorstore = Chroma(
        client=client,
        collection_name="accio_hr_llama",
        embedding_function=embedding_function,
    )

    return vectorstore


def get_conversation_chain(vectorstore, temperature, max_new_tokens=250):
    class ContentHandler(LLMContentHandler):
        content_type = "application/json"
        accepts = "application/json"

        def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "do_sample": True,
                    "top_p": 0.6,
                    "temperature": temperature,
                    "top_k": 50,
                    "max_new_tokens": max_new_tokens,
                    "repetition_penalty": 1.03,
                    "stop": ["</s>"]
                }
            }
            input_str = json.dumps(
                payload,
            )
            return input_str.encode("utf-8")

        def transform_output(self, output: bytes) -> str:
            response_json = json.loads(output.read().decode("utf-8"))
            content = response_json[0]["generated_text"]
            return content

    llm = SagemakerEndpoint(
        endpoint_name=endpoint_name,
        region_name=region,
        content_handler=ContentHandler(),
        callbacks=[StreamingStdOutCallbackHandler()],
    )

    memory = ConversationBufferMemory(memory_key='chat_history',
                                      return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def process_answer(answer):
    answer_list = answer.split("\n")
    answer_list.pop(0)

    answer = "\n".join(answer_list)

    answer1 = answer.split("Question:")[0]
    answer2 = answer.split("Helpful Answer:")[1].split("Context:")[0]

    return answer2


def handle_userinput(user_question):

    # if st.session_state.vector_store_created == False:
    #     st.error("The PDFs where not loaded properly..... please try reloading them again",  icon="🚨")
    #     return

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in reversed(list(enumerate(st.session_state.chat_history))):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:

            st.write(bot_template.replace(
                "{{MSG}}", process_answer(message.content)), unsafe_allow_html=True)


def app():
    # st.set_page_config(page_title="Chat with multiple documents",
    #                    page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "vector_store_created" not in st.session_state:
        st.session_state.vector_store_created = False

    # st.header("Chat with PolicyPal :briefcase:")
    intro = ''' 
            # Chat with PolicyPal :briefcase:

            Hello there 👋​​ , I am PolicyPal. Welcome to Accio. Feel free to ask me any questions about our HR policies.

            ### Sample Questions that you can ask me:
            - How do I use my floating holidays?
            - How do I raise a formal complaint?
            - What should I do if I recieve a notice for Jury service?
            - What is the leave policy for this company?


    '''
    st.markdown(intro)
    user_question = st.text_input("Ask a HR Policy question: (Model: Llama2-7b)")
    if user_question:
        handle_userinput(user_question)

    user_feedback = collector.st_feedback(
        component="default",
        feedback_type="thumbs",
        open_feedback_label="[Optional] Provide additional feedback",
        model="llama-2-7b",
        prompt_id=None,  # checkout collector.log_prompt() to log your user prompts
        key=f"feedback_legal"
    )

    if user_feedback:
        st.write(user_feedback)

    with st.sidebar:

        temperature = st.slider("Temperature", min_value=0.01, max_value=1.0, step=0.1, key="temperature_chat_hr")
        max_new_tokens = st.slider("Max Tokens", min_value=100, max_value=500, step=50, key="max_new_tokens_chat_hr")

        if st.button("Connect to PolicyPal"):
            with st.spinner("Processing"):

                # create vector store
                vectorstore = get_vectorstore()
                st.session_state.vector_store_created = True

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore, temperature, max_new_tokens)


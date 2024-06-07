import streamlit as st
import dotenv
from langchain.prompts import (
    ChatPromptTemplate,
)
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough

# Load environment variables
dotenv.load_dotenv()

# Define the path for the Chroma data
CHROMA_PATH = "chroma_data/"

# Initialize the Chroma vector database with Google Generative AI embeddings
reviews_vector_db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    ),
)

# Create a retriever from the vector database
reviews_retriever = reviews_vector_db.as_retriever(k=10)

# Define the prompt template for the chatbot
review_prompt_template = ChatPromptTemplate.from_template(
    "You are an assistant for answering questions about Magang MBKM for PENS students. {question}"
)

# Initialize the chat model
chat_model = ChatGoogleGenerativeAI(
    model="gemini-pro"
)

# Create the review chain
review_chain = (
    {"context": reviews_retriever, "question": RunnablePassthrough()}
    | review_prompt_template
    | chat_model
    | StrOutputParser()
)

# Define a function to answer questions using the review chain
def answer_question(question: str) -> str:
    return review_chain.invoke(question)

# Set page config
st.set_page_config(
    page_title="Chatbot Magang MBKM PENS",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for Futuristic Theme
st.markdown("""
    <style>
    body {
        background-color: #0e101c;
        color: #e0e6f1;
        font-family: 'Roboto', sans-serif;
    }
    .stButton>button {
        background-color: #1f4068;
        color: #e0e6f1;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b3b5f;
    }
    .stTextInput>div>div>input {
        background-color: #162447;
        color: #e0e6f1;
        border: none;
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #e0e6f1;
    }
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit interface
st.markdown("""
    <div class="center">
        <img src="https://upload.wikimedia.org/wikipedia/id/4/44/Logo_PENS.png" width="150"/>
    </div>
    """, unsafe_allow_html=True)
st.title("Chatbot Magang MBKM untuk Mahasiswa PENS")

# st.write("""
#     <div style="text-align: center;">
#         <h1 style="color: #e0e6f1;">Chatbot Magang MBKM</h1>
#         <p style="color: #e0e6f1;">Untuk Mahasiswa Politeknik Elektronika Negeri Surabaya</p>
#     </div>
#     """, unsafe_allow_html=True)

st.write("### Masukkan pertanyaan Anda tentang Magang MBKM:")

question = st.text_input("")

if st.button("Tanya"):
    if question:
        with st.spinner("Sedang mencari jawaban..."):
            answer = answer_question(question)
            st.success("Jawaban:")
            st.write(answer)
    else:
        st.error("Harap masukkan pertanyaan.")

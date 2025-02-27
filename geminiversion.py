import streamlit as st
import random
import time
import PyPDF2

st.set_page_config(page_title="ShawnBot", layout="wide")

from google import genai
from google.genai import types

from PyPDF2 import PdfReader

client = genai.Client(api_key="AIzaSyBR4x9HaeWtdkD3u-rqLE47Mb570nOsE_I")

uploaded_files = st.file_uploader("Upload your Data here in PDF or TXT format {IF YOU REMOVE A FILE AFTER UPLOADING YOU MUST REFRESH THE PAGE}", accept_multiple_files=True, type=['pdf', 'txt'])

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
        text = text.replace("\n", "")
    return text

def get_txt_text(txt_files):
    text = ""
    for txt in txt_files:
        try:
            for line in txt:
                decoded_line = line.decode("utf-8")  # Decode bytes to string
                text += decoded_line
                # text = text.replace("\n", "")
        except Exception as e:
            st.error(f"Error reading TXT file: {e}")
    return text

if uploaded_files:
    pdf_docs = [file for file in uploaded_files if file.type == "application/pdf"]
    txt_files = [file for file in uploaded_files if file.type == "text/plain"]

    with st.spinner("Processing"):
        pdf_text = get_pdf_text(pdf_docs) if pdf_docs else ""
        txt_text = get_txt_text(txt_files) if txt_files else ""
        combo_text = pdf_text + txt_text
        raw_text = "You are an expert support agent who has years of experience with Advantage software. You pride yourself on incredible accuracy and attention to detail. You always stick to the facts in the sources provided, and never make up new facts. You only make conclusions based on the following information in the below research information:\n\n" + combo_text
        st.success("Your Data has been processed successfully")
        
    
    st.title("Advantage Software Expert")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is your Advantage Software question or comment?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt], config=types.GenerateContentConfig(max_output_tokens=3000, temperature=0 , system_instruction=raw_text,))
            st.write(response.text)

        st.session_state.messages.append({"role": "assistant", "content": response.text})

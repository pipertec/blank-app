import streamlit as st
import random
import time
import PyPDF2

from google import genai
from google.genai import types

from PyPDF2 import PdfReader

client = genai.Client(api_key="AIzaSyBR4x9HaeWtdkD3u-rqLE47Mb570nOsE_I")

pdf_docs = st.file_uploader("Upload your Data here  in PDF format ", accept_multiple_files=True, type=['pdf'])   
            

   
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
  
    with st.spinner("Processing"):
        raw_text = get_pdf_text(pdf_docs)
        st.success("Your Data has been processed successfully")


  
raw_text = get_pdf_text(pdf_docs)    

# Get user input for filename
# filename = "testjoe.txt"
# stuff = raw_text  
# with open(filename, 'w') as file:
        # file.write(stuff)        
            
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
     
     
      response = client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05",contents=[prompt],config=types.GenerateContentConfig(max_output_tokens=1000,temperature=0.1,system_instruction=raw_text,))
      st.write(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})

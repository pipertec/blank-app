import streamlit as st
import random
import time
import PyPDF2

st.set_page_config(page_title="ShawnBot", layout="wide")

# hide_streamlit_style = """
                # <style>
                # div[data-testid="stToolbar"] {
                # visibility: hidden;
                # height: 0%;
                # position: fixed;
                # }
                # div[data-testid="stDecoration"] {
                # visibility: hidden;
                # height: 0%;
                # position: fixed;
                # }
                # div[data-testid="stStatusWidget"] {
                # visibility: hidden;
                # height: 0%;
                # position: fixed;
                # }
                # #MainMenu {
                # visibility: hidden;
                # height: 0%;
                # }
                # header {
                # visibility: hidden;
                # height: 0%;
                # }
                # footer {
                # visibility: hidden;
                # height: 0%;
                # }
               # </style>
                # """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)





from google import genai
from google.genai import types

from PyPDF2 import PdfReader

client = genai.Client(api_key="AIzaSyBR4x9HaeWtdkD3u-rqLE47Mb570nOsE_I")

pdf_docs = st.file_uploader("Upload your Data here in PDF format {IF YOU REMOVE A FILE AFTER UPLOADING YOU MUST REFRESH THE PAGE}", accept_multiple_files=True, type=['pdf'])   
            

   
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
            
            text_no_lines = text.replace("\n", "") 
            text=text_no_lines

            # print(text) 

            # print("Press Enter to continue...")
            
            # input()  # Wait for user input
            
            # print("Continuing...")
            
          

    
    return text
    
  
  
  
    with st.spinner("Processing"):
        raw_text = get_pdf_text(pdf_docs)
        st.success("Your Data has been processed successfully")
        
        
        

# raw_text =  "Only the information to the right of the 👷 and the left of the 🥷can be used to supply answers in this chat. As a professional agent you may suggest methods  from the facts supplied here to answer user 
# questions 👷" + get_pdf_text(pdf_docs) + "🥷"

# raw_text =  "Only the information to the right of the : and the left of the 🥷can be used to supply answers in this chat. As a professional agent you never veer from the facts supplied here 👷" + get_pdf_text(pdf_docs) + "🥷"

raw_text = "You are an expert support agent who has years of experience with Advantage software. You pride yourself on incredible accuracy and attention to detail. You always stick to the facts in the sources provided, and never make up new facts. You only make conclusions based on the following information in the below research information:\n\n" + get_pdf_text(pdf_docs) 

# raw_text = get_pdf_text(pdf_docs)    


    
            
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
     
     
      # response = client.models.generate_content(model="gemini-2.0-flash-lite-preview-02-05",contents=[prompt],config=types.GenerateContentConfig(max_output_tokens=1000,temperature=0.1,system_instruction=raw_text,))
      response = client.models.generate_content(model="gemini-2.0-flash",contents=[prompt],config=types.GenerateContentConfig(max_output_tokens=3000,temperature=0.1,system_instruction=raw_text,))

      st.write(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})

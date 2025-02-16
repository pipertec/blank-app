import streamlit as st
import random
import time
from google import genai
from google.genai import types


client = genai.Client(api_key="AIzaSyBR4x9HaeWtdkD3u-rqLE47Mb570nOsE_I")
# Streamed response emulator
def response_generator():
    ###response = random.choice(
       ### [
          ###  "Hello there! How can I assist you today?",
            ###"Hi, human! Is there anything I can help you with?",
            ###"Do you need help?",
        ###]
    ###)

     
    response = client.models.generate_content(
    model="gemini-2.0-flash-lite-preview-02-05",
    contents=[prompt],
    config=types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=0.1,
        
    )
 
)


    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Advantage Software Expert")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

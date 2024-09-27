import streamlit as st
from streamlit_chat import message as st_message
from resturant_chatbot import *

st.markdown("""## Crimson Dine Restaurant ChatBot
This is a chat bot that has information about different Fast Food Deals. This can help customers about any Fast Food Deals they want.
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input section
if question := st.chat_input("Say Something"):
    userid = "guest"
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    
    response = restaurant_chatbot(userid,question)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("ai"):
        st.markdown(response)

st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <hr>
        <p>Developed by <strong>Muhammad Afaq Khan</strong></p>
    </div>
""", unsafe_allow_html=True)
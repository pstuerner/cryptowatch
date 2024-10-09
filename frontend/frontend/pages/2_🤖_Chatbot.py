import streamlit as st
from datetime import datetime as dt
from datetime import timedelta as td
from frontend.db.chroma import ChromaDB
from frontend.chat.chat import ChatLLM

chat = ChatLLM()
chroma = ChromaDB()

# Sidebar for date range picker
st.sidebar.title("Filters")
start_date = st.sidebar.date_input("Start Date", dt.now().date()-td(days=7))
start_date = dt(start_date.year, start_date.month, start_date.day)
end_date = st.sidebar.date_input("End Date", dt.today())
end_date = dt(end_date.year, end_date.month, end_date.day, 23, 59, 59)

# Ensure that the end date is after the start date
if start_date > end_date:
    st.sidebar.error("Error: End Date must be after Start Date.")

if "messages" not in st.session_state: # Initialize the chat message history
    st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question !"}
    ]        

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chat.msg_chain += st.session_state.messages[1:]
            response = chat.chat(
                prompt,
                retrieve=True,
                filter={
                    "$and": [
                        {"published": {"$gte": int(start_date.timestamp())}},
                        {"published": {"$lte": int(end_date.timestamp())}},
                    ]
                }
            )
            st.write(response.replace("$","\$"))
            st.session_state.messages += chat.msg_chain[-1:]
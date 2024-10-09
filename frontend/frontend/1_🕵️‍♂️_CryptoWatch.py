import streamlit as st
from datetime import datetime as dt
from datetime import timedelta as td
from concurrent.futures import ThreadPoolExecutor
from frontend.chat.chat import ChatLLM
from frontend.utils.env import TOKENS_BASKET

def get_highlights(crypto, start_date, end_date):
    chat = ChatLLM()
    response = chat.chat(
        prompt=f"Give a brief summary about the latest news for {crypto['name']} ({crypto['ticker']}).",
        retrieve=True,
        filter={
            "$and": [
                {"published": {"$gte": int(start_date.timestamp())}},
                {"published": {"$lte": int(end_date.timestamp())}},
            ]
        }
    )

    return response

st.set_page_config(
    page_title="CryptoWatch",
    page_icon="🕵️‍♂️",
)

st.title("CryptoWatch 🕵️‍♂️")
st.sidebar.title("Filters")
start_date = st.sidebar.date_input("Start Date", dt.now().date()-td(days=7))
start_date = dt(start_date.year, start_date.month, start_date.day)
end_date = st.sidebar.date_input("End Date", dt.today())
end_date = dt(end_date.year, end_date.month, end_date.day, 23, 59, 59)

# Ensure that the end date is after the start date
if start_date > end_date:
    st.sidebar.error("Error: End Date must be after Start Date.")

if st.button('✨ Go ✨'):
    with ThreadPoolExecutor() as executor:
        responses = executor.map(lambda p: get_highlights(*p), ((t, start_date, end_date) for t in TOKENS_BASKET))

    for t, r in zip(TOKENS_BASKET, responses):
        with st.expander(f"{t['name']} ({t['ticker']})"):
            st.write(r.replace("$","\$"))
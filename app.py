import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv
import os

@st.cache_resource
def get_chain():
    # Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are Health Expert, who suggests the steps count each day to be done. Return steps count number only steps for today first and few suggestions on foods to have for daily health as per their age and BMI."),
        ("human", "Provide steps count for {question} ")
    ])

    load_dotenv() # take environment variables from .env.

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2
    )
    chain = prompt | llm 
    return chain

## 1. Create a history session variable to maintain history
# if "history" not in st.session_state:
#     # st.write("History variable not there")
#     st.session_state.history = []

def get_llm_response(user_text: str) -> str:
    chat = get_chain()
    # your “no-config” invoke variant that keeps its own history
    return chat.invoke({"question": user_text})


## 3. Create a Function which writes append to history
def on_send(text):
    response = get_llm_response(text)
    # st.rerun()
    return response



st.title("Deit and Steps Manager")
# Expander for personal details

name = st.text_input("Enter your name:")
age = st.slider("Select your age:", 0, 100, 25)

# Expander for preferences

with st.expander("BMI Details"):
    weight = st.slider("weight:", 0, 150, 50)
    st.subheader("Height")
    height_feet = st.selectbox("Feet:", [1,2,3,4,5,6,7,8,9,10],4)
    height_inches = st.selectbox("Inches:", [1,2,3,4,5,6,7,8,9,10],5)

with st.expander("Food Information"):
    bf = st.text_input("Break fast:")
    lunch = st.text_input("Lunch:")
    dinner = st.text_input("Dinner:")

if st.button("Submit"):
    if name:
        text = f"customer of age {age}, and height of {height_feet} feet {height_inches} inches and would eat {bf}, {lunch}, {dinner} as breakfast, lunch and dinner"
        response = on_send(text)
        st.subheader(f"Hey {name}, Please walk the total steps daily {response.content} Steps today to Stay active.")
    else:
        st.subheader(f"Please enter your name")




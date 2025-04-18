import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))
system_prompt = """you are a search engine. you are going to recieve a specific topic from the user. generate a page of information in the following JSON format:
    {
        "creator": who invented this equation
        "purpose": what is the use of this equation
        "form": what does this equation look like
    }
""" 

user_prompt = ""
topics = ["Quadratic Equations","Linear Equation","Pythagorean Theorem"]

if "wikipedia" not in st.session_state:
    st.session_state["wikipedia"] = {}
    for i in topics:
        user_prompt = "generate a page base on this topic: "+i
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            response_format= {"type":"json_object"},
            messages = [
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_prompt}
            ]
        ) 
        st.session_state["wikipedia"][i]= response.choices[0].message.content

"""
Welcome to the Math Wiki!
"""

selected_topic = st.selectbox("Which page would you like to read?",topics)
st.write(selected_topic)

st.write(st.session_state["wikipedia"])

"""
CREATOR
"""

st.write(st.session_state["wikipedia"][selected_topic]["creator"])
"""
PURPOSE
"""
"""
FORM
"""
import streamlit as st
import json
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
"""
Welcome to the Math Wiki!
"""
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
        st.session_state["wikipedia"][i]= json.loads(response.choices[0].message.content)

with st.form("request"):
    new_topic = st.text_input("Request another topic")
    submit = st.form_submit_button("Submit")
    if submit: 
        user_prompt = "generate a page base on the new topic: "+new_topic
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            response_format= {"type":"json_object"},
            messages = [
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_prompt}
            ]
        ) 
        st.session_state["wikipedia"][new_topic] = json.loads(response.choices[0].message.content)
        topics.append(new_topic)
        st.write(topics)
        


selected_topic = st.selectbox("Which page would you like to read?",topics)
st.write(selected_topic)



"""
CREATOR
"""

st.write(st.session_state["wikipedia"][selected_topic]["creator"])
"""
PURPOSE
"""
st.write(st.session_state["wikipedia"][selected_topic]["purpose"])
"""
FORM
"""
st.write(st.session_state["wikipedia"][selected_topic]["form"])
"""
WANT MORE PAGES?
"""



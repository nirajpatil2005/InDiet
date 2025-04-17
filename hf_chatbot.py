import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

# Custom fitness prompt template
FITNESS_PROMPT = """
You are a certified fitness and nutrition assistant. 
Provide long word, science-backed answers about:
- Workout routines (PPL, HIIT, Strength)
- Diet plans (keto, vegan, macros)
- Exercise techniques
- Calorie calculations

User Question: {user_input}
"""

def query_huggingface(prompt):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "inputs": FITNESS_PROMPT.format(user_input=prompt),
        "parameters": {"max_new_tokens": 20000}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['generated_text']

# Streamlit UI
st.title("🏋️ Fitness AI Assistant")
user_input = st.text_input("Ask about workouts or nutrition:")

if user_input:
    with st.spinner("Getting expert advice..."):
        try:
            answer = query_huggingface(user_input)
            st.success(answer)
        except Exception as e:
            st.error(f"Error: {str(e)}")
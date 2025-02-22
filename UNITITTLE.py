# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:15:21 2025

@author: admin
"""

import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import re
import requests
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part, Content
import json
from dotenv import load_dotenv

load_dotenv()


# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# loading the saved models

diabetes_model = pickle.load(
    open(r'C:\Programs\Learning\techathon_project\diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(
    open(r'C:\Programs\Learning\techathon_project\heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(
    open(r'C:\Programs\Learning\techathon_project\parkinsons_model.sav', 'rb'))

# Function to interact with the Gemini Pro API


def is_health_related(user_input):

    # A simple regex pattern to check for health-related keywords

    health_keywords = [
        "health", "doctor", "medicine", "symptom", "disease", "treatment",
        "diagnosis", "medication", "wellness", "nutrition", "exercise",
        "mental health", "therapy", "healthcare", "patient", "illness"
    ]

    pattern = r'\b(?:' + '|'.join(health_keywords) + r')\b'
    return bool(re.search(pattern, user_input, re.IGNORECASE))


def get_gemini_response(user_input):
    if not is_health_related(user_input):
        f = 0
        return "Please ask a health-related question.", f
    else:
        response = model.generate_content(user_input)
        return response


# Adding stylesheet
st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">' + '<style>' + open(r'C:\Programs\Learning\techathon_project\styles.css', 'r').read() + '</style>', unsafe_allow_html=True)

#main Navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',
                           ['General Assistance',
                            'Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction',
                            'Hypertention Prediction',
                            'Breast Cancer',
                            'Maternal & Child Health',
                            'Neonatal Jaundice Detection',
                            'Malnutrition Detection in Children',
                            'Anemia Detection',
                            'Dengue & Malaria Prediction',
                            'Typhoid & Cholera Detection',
                            'Tuberculosis (TB) Screening',
                            'Leptospirosis Prediction',
                            'Farmer’s Lung Disease Prediction',
                            'Pesticide Poisoning Risk Analysis'

                           ],
                           menu_icon='hospital-fill',
                           icons=['chat-right-heart', 'activity', 'heart', 'person', 'clipboard-pulse'],
                           default_index=0)
# Display a message when a user selects an option
#st.title(f"You selected: {selected}")

# General Assistance Chatbot
if selected == "General Assistance":
    st.title("💬 Healthcare Chatbot")
    st.write("Ask me anything about health!")
# Suggested questions
suggested_questions = [
    "What are the symptoms of diabetes?",
    "How can I prevent heart disease?",
    "What are the early signs of Parkinson's?",
    "How do I manage high blood pressure?",
    "What are the risk factors for breast cancer?",
]

# Display suggested questions as clickable buttons
st.write("### Suggested Questions:")
selected_question = st.radio("", suggested_questions, index=None)

# Input field with autofill when a suggestion is selected
if "user_question" not in st.session_state:
    st.session_state.user_question = ""

if selected_question:
    st.session_state.user_question = selected_question

user_input = st.text_input("Your Question:", st.session_state.user_question)

if st.button("Ask "):
    if user_input:
        st.write(f"🧑‍⚕️ **Chatbot:** Here is the response to your question: _'{user_input}'_")
    else:
        st.warning("Please enter a question before clicking Ask.")
    # Chat UI
    question = st.text_input("Your Question:")
    ask = st.button("Ask")

    if ask and question:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question)
        st.success(response.text)

# Diabetes Prediction
if selected == "Diabetes Prediction":
    st.title("🩸 Diabetes Prediction")
    col1, col2 = st.columns(2)

    with col1:
        Pregnancies = st.slider("Number of Pregnancies", 0, 15, 1)
        Glucose = st.slider("Glucose Level", 50, 200, 100)
        BloodPressure = st.slider("Blood Pressure", 50, 150, 80)

    with col2:
        SkinThickness = st.slider("Skin Thickness", 5, 50, 20)
        Insulin = st.slider("Insulin Level", 0, 300, 100)
        BMI = st.slider("BMI", 10.0, 50.0, 25.0)

    DiabetesPedigreeFunction = st.number_input(
        "Diabetes Pedigree Function", value=0.5, format="%.2f")
    Age = st.number_input("Age", min_value=1, max_value=120, value=30)

    if st.button("Predict Diabetes"):
        user_input = [Pregnancies, Glucose, BloodPressure,
                      SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        result = diabetes_model.predict([user_input])
        st.success("Diabetic" if result[0] == 1 else "Not Diabetic")

# Heart Disease Prediction
if selected == "Heart Disease Prediction":
    st.title("❤️ Heart Disease Prediction")
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        sex = st.selectbox("Sex", ["Male", "Female"])
        cp = st.slider("Chest Pain Type", 0, 3, 1)

    with col2:
        trestbps = st.slider("Resting Blood Pressure", 80, 200, 120)
        chol = st.slider("Cholesterol", 100, 400, 200)
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["Yes", "No"])

    if st.button("Predict Heart Disease"):
        user_input = [age, 1 if sex == "Male" else 0,
                      cp, trestbps, chol, 1 if fbs == "Yes" else 0]
        result = heart_disease_model.predict([user_input])
        st.success(
            "Heart Disease Detected" if result[0] == 1 else "No Heart Disease")

# Parkinson's Prediction
if selected == "Parkinsons Prediction":
    st.title("🧠 Parkinson's Disease Prediction")
    spread1 = st.slider("Spread1", -10.0, 10.0, 0.0)
    spread2 = st.slider("Spread2", -10.0, 10.0, 0.0)
    PPE = st.slider("PPE", 0.0, 1.0, 0.5)

    if st.button("Predict Parkinson's"):
        user_input = [spread1, spread2, PPE]
        result = parkinsons_model.predict([user_input])
        st.success("Has Parkinson's" if result[0] == 1 else "No Parkinson's")


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

# Getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# 🔹 Function to load models safely
def load_model(file_name):
    model_path = os.path.join(working_dir, file_name)
    
    if not os.path.exists(model_path):
        st.error(f"Error: Model file '{file_name}' not found!")
        raise FileNotFoundError(f"Model file '{file_name}' not found in {working_dir}")
    
    with open(model_path, 'rb') as file:
        return pickle.load(file)

# 🔹 Loading models with error handling
try:
    diabetes_model = load_model("diabetes_model.sav")
    heart_disease_model = load_model("heart_disease_model.sav")
    parkinsons_model = load_model("parkinsons_model.sav")
except Exception as e:
    st.error(f"Model loading failed: {e}")

# 🔹 Function to check if the input is health-related
def is_health_related(user_input):
    health_keywords = [
        "health", "doctor", "medicine", "symptom", "disease", "treatment",
        "diagnosis", "medication", "wellness", "nutrition", "exercise",
        "mental health", "therapy", "healthcare", "patient", "illness"
    ]
    pattern = r'\b(?:' + '|'.join(health_keywords) + r')\b'
    return bool(re.search(pattern, user_input, re.IGNORECASE))

# 🔹 Function to get a response from the Gemini Pro API
def get_gemini_response(user_input):
    if not is_health_related(user_input):
        return "Please ask a health-related question."
    
    key = os.getenv("API_KEY")
    
    if not key:
        return "API key not found. Please set up your API key."
    
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-pro")
    
    try:
        key = os.getenv('API_KEY')
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-pro')

        return response.text if hasattr(response, 'text') else "Invalid response format."
    except Exception as e:
        return f"Error in getting response: {e}"

# 🔹 Add custom stylesheet
css_path = os.path.join(working_dir, "styles.css")
if os.path.exists(css_path):
    with open(css_path, 'r') as css_file:
        st.markdown(f'<style>{css_file.read()}</style>', unsafe_allow_html=True)
else:
    st.warning("Warning: styles.css file not found!")

# Sidebar navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',
                           ['General Assistance',
                            'Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction'],
                           menu_icon='hospital-fill',
                           icons=['chat-right-heart', 'activity', 'heart', 'person'],
                           default_index=0)

# 🩺 General Assistance Page (Chatbot)
if selected == 'General Assistance':
    st.title('General Healthcare Chatbot')

    question = st.text_input('Ask a question')
    ask = st.button('Ask')

    if ask and question:
        res = get_gemini_response(question)
        st.success(res)

# 🩸 Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value')

    with col2:
        Insulin = st.text_input('Insulin Level')

    with col3:
        BMI = st.text_input('BMI value')

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

    with col2:
        Age = st.text_input('Age of the Person')

    diab_diagnosis = ""

    if st.button('Diabetes Test Result'):
        try:
            user_input = list(map(float, [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]))
            diab_prediction = diabetes_model.predict([user_input])

            diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
        except ValueError:
            diab_diagnosis = "Invalid input! Please enter numeric values only."
        except Exception as e:
            diab_diagnosis = f"Prediction failed: {e}"

    st.success(diab_diagnosis)

# ❤️ Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')
    with col2:
        sex = st.text_input('Sex')
    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')
    with col2:
        chol = st.text_input('Serum Cholesterol in mg/dl')
    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')
    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')
    with col3:
        exang = st.text_input('Exercise Induced Angina')

    heart_diagnosis = ""

    if st.button('Heart Disease Test Result'):
        try:
            user_input = list(map(float, [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang]))
            heart_prediction = heart_disease_model.predict([user_input])

            heart_diagnosis = 'The person has heart disease' if heart_prediction[0] == 1 else 'The person does not have heart disease'
        except ValueError:
            heart_diagnosis = "Invalid input! Please enter numeric values only."
        except Exception as e:
            heart_diagnosis = f"Prediction failed: {e}"

    st.success(heart_diagnosis)

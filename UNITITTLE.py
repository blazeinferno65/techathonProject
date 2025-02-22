# @@ -1,324 +1,325 @@
# # -*- coding: utf-8 -*-
# """
# Created on Wed Feb 19 13:15:21 2025

# @author: admin
# """

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

base_dir = os.path.dirname(os.path.abspath(__file__))

# relative paths for each 

diabetes_path = os.path.join(base_dir, "diabetes_model.sav")
heart_disease_path = os.path.join(base_dir, "heart_disease_model.sav")
parkinsons_path = os.path.join(base_dir, "parkinsons_model.sav")
css_path = os.path.join(base_dir, "styles.css")

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# loading the saved models

diabetes_model = pickle.load(
    open(f'{diabetes_path}', 'rb'))
heart_disease_model = pickle.load(
    open(f'{heart_disease_path}', 'rb'))
parkinsons_model = pickle.load(

# Function to interact with the Gemini Pro API

    open(f'{parkinsons_path}', 'rb'))

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
        return 0
    else:
        return 1


# Adding stylesheet
st.markdown('<link href=f"{css_path}" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">', unsafe_allow_html=True)

# sidebar for navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',
                           ['General Assistance',
                            'Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction',
                            'Hypertention Prediction',
                            'Breast Cancer',
                            'Maternal & Child Health',
                            'Neonatal Jaundice Detection ',
                            'Malnutrition Detection in Children',
                            'Anemia Detection',
                            'Dengue & Malaria Prediction',
                            'Typhoid & Cholera Detection',
                            'Tuberculosis (TB) Screening ',
                            'Leptospirosis Prediction',
                            'Farmer’s Lung Disease Prediction ',
                            'Pesticide Poisoning Risk Analysis ',

                            ],
                           menu_icon='hospital-fill',
                           icons=['chat-right-heart', 'activity',
                                  'heart', 'person', 'clipboard-pulse'],
                           default_index=0)

# General Assistance Page (Chatbot)
if selected == 'General Assistance':

    # Page Title
    st.title('General Healthcare Chatbot')

    # os.getenv(str(['API_KEY']))
    key = genai.configure(api_key=os.getenv('API_KEY'))
    model = genai.GenerativeModel('gemini-pro')

    question = st.text_input('Ask a question')
    ask = st.button('Ask')

    if ask:
        if get_gemini_response(question):
            response = model.generate_content(question)
            st.success(getattr(response, 'text'))
        else:
            st.error("Please ask a health related question.")

    # Define model with system role

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    # page title
    st.title('Diabetes Prediction using ML')

    # getting the input data from the user
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
        DiabetesPedigreeFunction = st.text_input(
            'Diabetes Pedigree Function value')

    with col2:
        Age = st.text_input('Age of the Person')

    # code for Prediction
    diab_diagnosis = ''

    # creating a button for Prediction
    if st.button('Diabetes Test Result'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                      BMI, DiabetesPedigreeFunction, Age]

        user_input = [float(x) for x in user_input]

        diab_prediction = diabetes_model.predict([user_input])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person is diabetic'
        else:
            diab_diagnosis = 'The person is not diabetic'

    st.success(diab_diagnosis)

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    # page title
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
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina')

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')

    with col1:
        thal = st.text_input(
            'thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    # code for Prediction
    heart_diagnosis = ''

    # creating a button for Prediction
    if st.button('Heart Disease Test Result'):
        user_input = [age, sex, cp, trestbps, chol, fbs,
                      restecg, thalach, exang, oldpeak, slope, ca, thal]

        user_input = [float(x) for x in user_input]

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
        else:
            heart_diagnosis = 'The person does not have any heart disease'

    st.success(heart_diagnosis)

# Parkinson's Prediction Page
if selected == "Parkinsons Prediction":
    # page title
    st.title("Parkinson's Disease Prediction using ML")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')

    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    # code for Prediction
    parkinsons_diagnosis = ''

    # creating a button for Prediction
    if st.button("Parkinson's Test Result"):
        user_input = [float(x) for x in user_input]

        parkinsons_prediction = parkinsons_model.predict([user_input])

        if parkinsons_prediction[0] == 1:
            parkinsons_diagnosis = "The person has Parkinson's disease"
        else:
            parkinsons_diagnosis = "The person does not have Parkinson's disease"

    st.success(parkinsons_diagnosis)

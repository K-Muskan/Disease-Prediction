import streamlit as st
from firebase_config import db, initialize_firebase
import logging
 #from signup import sign_up
import pickle
import datetime
import numpy as np
import pandas as pd
import base64
import io
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load models
diabetes_model = pickle.load(open('C:\Shumail\Project\DiseasePredictionSystemATU-main\saved_models\diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('C:\Shumail\Project\DiseasePredictionSystemATU-main\saved_models\heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('C:\Shumail\Project\DiseasePredictionSystemATU-main\saved_models\parkinsons_model.sav', 'rb'))
anemia_model = pickle.load(open('C:\\Shumail\\Project\\DiseasePredictionSystemATU-main\\saved_models\\fine_tuned_rf_model.pkl', 'rb'))
typhoid_model = pickle.load(open('C:\Shumail\Project\DiseasePredictionSystemATU-main\saved_models\dt_model.pkl', 'rb'))
hiv_model = pickle.load(open('C:\Shumail\Project\DiseasePredictionSystemATU-main\hiv_prediction_model.pkl', 'rb'))

def save_prediction(user_id, prediction_type, input_data, result):
    prediction_ref = db.collection('users').document(user_id).collection('predictions').document()
    prediction_ref.set({
        'type': prediction_type,
        'input_data': input_data,
        'result': result,
        'timestamp': datetime.datetime.now()
    })

def diabetes_prediction():
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
        Age = st.text_input('Age of the person')
            
    if st.button('Diabetes Test Result'):
        if not all([Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]):
            st.error('All fields are required. Please fill in all the information.')
        else:
            try:
                input_data = [
                    float(Pregnancies),
                    float(Glucose),
                    float(BloodPressure),
                    float(SkinThickness),
                    float(Insulin),
                    float(BMI),
                    float(DiabetesPedigreeFunction),
                    float(Age)
                ]
                
                diab_prediction = diabetes_model.predict([input_data])
                diab_diagnosis = 'The person is likely Diabetic' if diab_prediction[0] == 1 else 'The person is not Diabetic'
                
                st.success(diab_diagnosis)
                
                st.write("---")
                st.write("### Next Steps and Resources")
                
                if diab_prediction[0] == 1:
                    st.markdown("""
                    If you've been diagnosed with diabetes, it's important to take proactive steps:
                    
                    1. **Consult a Healthcare Professional**: Schedule an appointment with your doctor for a comprehensive evaluation.
                    2. **Learn About Diabetes Management**: Educate yourself about diabetes and its management.
                    3. **Develop a Treatment Plan**: Work with your healthcare team to create a personalized treatment plan.
                    
                    For more information, check out these reliable resources:
                    - [American Diabetes Association - Living with Diabetes](https://www.diabetes.org/diabetes)
                    - [CDC - Managing Diabetes](https://www.cdc.gov/diabetes/managing/index.html)
                    - [Mayo Clinic - Diabetes Care](https://www.mayoclinic.org/diseases-conditions/diabetes/in-depth/diabetes-management/art-20047963)
                    """)
                else:
                    st.markdown("""
                    While your results suggest you don't have diabetes, it's always good to maintain a healthy lifestyle:
                    
                    1. **Maintain a Healthy Diet**: Focus on a balanced diet rich in fruits, vegetables, and whole grains.
                    2. **Regular Exercise**: Aim for at least 150 minutes of moderate-intensity exercise per week.
                    3. **Regular Check-ups**: Continue to have regular health check-ups with your doctor.
                    
                    To learn more about diabetes prevention, visit:
                    - [National Institute of Diabetes and Digestive and Kidney Diseases - Preventing Type 2 Diabetes](https://www.niddk.nih.gov/health-information/diabetes/overview/preventing-type-2-diabetes)
                    - [American Heart Association - Prevent Diabetes](https://www.heart.org/en/health-topics/diabetes/prevention--treatment-of-diabetes)
                    - [World Health Organization - Diabetes Prevention](https://www.who.int/health-topics/diabetes#tab=tab_2)
                    """)
                
                st.write("*Disclaimer: These resources are for informational purposes only and do not constitute medical advice. Always consult with a qualified healthcare professional for medical concerns.*")
                
                save_prediction(st.session_state.user.uid, 'Diabetes', input_data, diab_diagnosis)
            
            except ValueError as e:
                st.error(f"Invalid input: {e}. Please enter numeric values only.")
            except NameError:
                st.error("Model is not defined. Please load the diabetes_model.")


def heart_disease_prediction():
    st.title('Heart Disease Prediction using ML')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.text_input('Age')
    with col2:
        # Dropdown for sex
        sex_display = st.selectbox('Sex', ['Male', 'Female'])
        sex = 1.0 if sex_display == 'Male' else 0.0  # Convert to float internally
    with col3:
        cp = st.text_input('Chest Pain Types')
    with col1:
        trestbps = st.text_input('Resting Blood Pressure')
    with col2:
        chol = st.text_input('Serum Cholesterol in mg/dl')
    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
    with col1:
        restecg = st.text_input('Resting Electrocardiographic Results')
    with col2:
        thalach = st.text_input('Maximum Heart Rate Achieved')
    with col3:
        exang = st.text_input('Exercise Induced Angina')
    with col1:
        oldpeak = st.text_input('ST Depression Induced by Exercise')
    with col2:
        slope = st.text_input('Slope of the Peak Exercise ST Segment')
    with col3:
        ca = st.text_input('Major Vessels Colored by Fluoroscopy')
    with col1:
        thal = st.text_input('Thal: 0 = normal; 1 = fixed defect; 2 = reversible defect')
        
    if st.button('Heart Disease Test Result'):
        if not all([age, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]):
            st.error('All fields are required. Please fill in all the information.')
        else:
            try:
                input_data = [
                    float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs),
                    float(restecg), float(thalach), float(exang), float(oldpeak), float(slope), float(ca), float(thal)
                ]
                
                heart_prediction = heart_disease_model.predict([input_data])
                heart_diagnosis = 'The person is likely to have a heart disease' if heart_prediction[0] == 1 else 'The person does not have any heart disease'
                
                st.success(heart_diagnosis)
                
                st.write("---")
                st.write("### Next Steps and Resources")
                
                if heart_prediction[0] == 1:
                    st.markdown("""
                    If your results indicate a risk of heart disease, consider these steps:
                    
                    1. **Seek Medical Attention**: Consult a cardiologist or your primary care physician immediately.
                    2. **Understand Your Condition**: Learn about heart disease and its management.
                    3. **Lifestyle Changes**: Be prepared to make necessary changes to your diet, exercise routine, and overall lifestyle.
                    
                    For comprehensive information on heart disease management:
                    - [American Heart Association - Heart Attack Recovery](https://www.heart.org/en/health-topics/heart-attack/life-after-a-heart-attack)
                    - [Mayo Clinic - Heart Disease](https://www.mayoclinic.org/diseases-conditions/heart-disease/diagnosis-treatment/drc-20353118)
                    - [National Heart, Lung, and Blood Institute - Heart Disease](https://www.nhlbi.nih.gov/health-topics/heart-disease)
                    """)
                else:
                    st.markdown("""
                    Your results suggest a lower risk of heart disease, but it's still important to maintain heart health:
                    
                    1. **Heart-Healthy Diet**: Adopt a diet low in saturated fats and rich in fruits, vegetables, and whole grains.
                    2. **Regular Exercise**: Engage in at least 150 minutes of moderate-intensity aerobic activity weekly.
                    3. **Stress Management**: Practice stress-reduction techniques like meditation or yoga.
                    
                    Learn more about preventing heart disease:
                    - [CDC - Prevent Heart Disease](https://www.cdc.gov/heartdisease/prevention.htm)
                    - [Harvard Health - Heart Disease Prevention](https://www.health.harvard.edu/topics/heart-health)
                    - [World Heart Federation - CVD Prevention](https://world-heart-federation.org/cvd-prevention/)
                    """)
                
                st.write("*Disclaimer: These resources are for informational purposes only and do not constitute medical advice. Always consult with a qualified healthcare professional for medical concerns.*")
                
                save_prediction(st.session_state.user.uid, 'Heart Disease', input_data, heart_diagnosis)
            
            except ValueError as e:
                st.error(f"Invalid input: {e}. Please enter numeric values only.")
            except NameError:
                st.error("Model is not defined. Please load the heart_disease_model.")


def parkinsons_prediction():
    st.title('Parkinsons Prediction using ML')
    
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
    
    if st.button('Parkinsons Test Result'):
        # Check if all fields are filled
        if not all([fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]):
            st.error('All fields are required. Please fill in all the information.')
        else:
            try:
                # Convert inputs to floats
                input_data = [
                    float(fo), float(fhi), float(flo), float(Jitter_percent), float(Jitter_Abs), float(RAP),
                    float(PPQ), float(DDP), float(Shimmer), float(Shimmer_dB), float(APQ3), float(APQ5),
                    float(APQ), float(DDA), float(NHR), float(HNR), float(RPDE), float(DFA), float(spread1),
                    float(spread2), float(D2), float(PPE)
                ]
                
                # Predict using the model
                parkinsons_prediction = parkinsons_model.predict([input_data])
                parkinsons_diagnosis = (
                    'The person is likely to have Parkinsons' 
                    if parkinsons_prediction[0] == 1 
                    else 'The person does not have Parkinsons'
                )
                
                # Display diagnosis
                st.success(parkinsons_diagnosis)
                
                # Additional resources
                st.write("---")
                st.write("### Next Steps and Resources")
                
                if parkinsons_prediction[0] == 1:
                    st.markdown("""
                    If your results suggest a possibility of Parkinson's disease:
                    
                    1. **Consult a Neurologist**: Seek an evaluation from a movement disorders specialist or neurologist.
                    2. **Learn About Parkinson's**: Educate yourself about the symptoms, progression, and management of Parkinson's disease.
                    3. **Explore Treatment Options**: Discuss potential treatments and therapies with your healthcare provider.
                    
                    For in-depth information on Parkinson's disease:
                    - [Parkinson's Foundation - Newly Diagnosed](https://www.parkinson.org/understanding-parkinsons/what-is-parkinsons)
                    - [Michael J. Fox Foundation - Living with Parkinson's](https://www.michaeljfox.org/living-parkinsons-disease)
                    - [National Institute on Aging - Parkinson's Disease](https://www.nia.nih.gov/health/parkinsons-disease)
                    """)
                else:
                    st.markdown("""
                    While your results don't indicate Parkinson's disease, it's always beneficial to maintain brain health:
                    
                    1. **Stay Physically Active**: Regular exercise can help maintain brain health.
                    2. **Mental Stimulation**: Engage in activities that challenge your mind, like puzzles or learning new skills.
                    3. **Healthy Diet**: Maintain a balanced diet rich in antioxidants and omega-3 fatty acids.
                    
                    Learn more about maintaining brain health and reducing Parkinson's risk:
                    - [Parkinson's UK - Reducing the Risk](https://www.parkinsons.org.uk/information-and-support/reducing-your-risk-parkinsons)
                    - [Harvard Health - Brain Health](https://www.health.harvard.edu/topics/brain-and-cognitive-health)
                    - [Mayo Clinic - Healthy Lifestyle for Brain Health](https://www.mayoclinic.org/healthy-lifestyle/healthy-aging/in-depth/memory-loss/art-20046518)
                    """)
                
                st.write("*Disclaimer: These resources are for informational purposes only and do not constitute medical advice. Always consult with a qualified healthcare professional for medical concerns.*")
                
                # Save prediction
                save_prediction(st.session_state.user.uid, 'Parkinsons', input_data, parkinsons_diagnosis)
            
            except ValueError as e:
                st.error(f"Invalid input: {e}. Please enter numeric values only.")
            except NameError:
                st.error("Model is not defined. Please load the `parkinsons_model`.")

def anemia_prediction():
    st.title('Anemia Prediction using ML')
    
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox('Gender', ['Male', 'Female'])
    with col2:
        hemoglobin = st.number_input('Hemoglobin (g/dL)', min_value=0.0, max_value=30.0, step=0.1)
    with col1:
        mch = st.number_input('MCH (Mean Corpuscular Hemoglobin) (pg)', min_value=0.0, max_value=50.0, step=0.1)
    with col2:
        mchc = st.number_input('MCHC (Mean Corpuscular Hemoglobin Concentration) (g/dL)', min_value=0.0, max_value=50.0, step=0.1)
    with col1:
        mcv = st.number_input('MCV (Mean Corpuscular Volume) (fL)', min_value=0.0, max_value=150.0, step=0.1)
    
    if st.button('Anemia Test Result'):
        # Ensure all fields are filled
        if not all([hemoglobin, mch, mchc, mcv]):
            st.error('All fields are required. Please fill in all the information.')
        else:
            try:
                # Prepare input data
                input_data = [
                    1 if gender == 'Male' else 0,  # Convert gender to binary
                    float(hemoglobin), float(mch), float(mchc), float(mcv)
                ]
                
                # Predict using the model
                anemia_prediction = anemia_model.predict([input_data])
                anemia_diagnosis = (
                    'The person is likely to have anemia'
                    if anemia_prediction[0] == 1
                    else 'The person is not likely to have anemia'
                )
                
                # Display results
                st.success(anemia_diagnosis)
                
                # Additional resources
                st.write("---")
                st.write("### Next Steps and Resources")
                
                if anemia_prediction[0] == 1:
                    st.markdown("""
                    If your results indicate a likelihood of anemia, consider these steps:
                    
                    1. **Consult a Healthcare Provider**: Schedule an appointment with your doctor for a comprehensive evaluation.
                    2. **Further Testing**: Your doctor may recommend additional blood tests to determine the type and cause of anemia.
                    3. **Dietary Changes**: Be prepared to make necessary changes to your diet to include more iron-rich foods.
                    
                    For comprehensive information on anemia:
                    - [American Society of Hematology - Anemia](https://www.hematology.org/education/patients/anemia)
                    - [Mayo Clinic - Anemia](https://www.mayoclinic.org/diseases-conditions/anemia/symptoms-causes/syc-20351360)
                    - [NIH - Iron-Deficiency Anemia](https://www.nhlbi.nih.gov/health-topics/iron-deficiency-anemia)
                    """)
                else:
                    st.markdown("""
                    Your results suggest a lower likelihood of anemia, but it's still important to maintain good health:
                    
                    1. **Balanced Diet**: Ensure you're eating a variety of nutrient-rich foods, including sources of iron.
                    2. **Regular Check-ups**: Continue with routine health check-ups and blood tests as recommended by your doctor.
                    3. **Stay Informed**: Learn about the symptoms of anemia to catch any future issues early.
                    
                    Learn more about maintaining healthy blood:
                    - [CDC - Iron and Iron Deficiency](https://www.cdc.gov/nutrition/micronutrient-malnutrition/micronutrients/iron.html)
                    - [Harvard Health - Anemia Prevention](https://www.health.harvard.edu/blog/9-ways-to-boost-your-energy-levels-2018032613452)
                    - [World Health Organization - Anaemia](https://www.who.int/health-topics/anaemia)
                    """)
                
                st.write("*Disclaimer: These resources are for informational purposes only and do not constitute medical advice. Always consult with a qualified healthcare professional for medical concerns.*")
                
                # Save prediction
                save_prediction(st.session_state.user.uid, 'Anemia', input_data, anemia_diagnosis)
            
            except ValueError as e:
                st.error(f"Invalid input: {e}. Please ensure all inputs are numbers where applicable.")
            except NameError:
                st.error("Model is not defined. Please load the `anemia_model` before using this function.")
    
    
import pandas as pd
import streamlit as st

def typhoid_prediction():
    st.title('Typhoid Disease Prediction using ML')
    
    col1, col2 = st.columns(2)
    
    with col1:
        patient_id = st.text_input('Patient ID')
    with col2:
        age = st.number_input('Age', min_value=0, max_value=120, step=1)
    with col1:
        gender = st.selectbox('Gender', ['Male', 'Female'])
    with col2:
        symptoms_severity = st.slider('Symptoms Severity', 1, 10, 5)
    with col1:
        hemoglobin = st.number_input('Hemoglobin (g/dL)', min_value=0.0, max_value=30.0, step=0.1)
    with col2:
        platelet_count = st.number_input('Platelet Count', min_value=0, max_value=1000000, step=1000)
    with col1:
        blood_culture = st.selectbox('Blood Culture Bacteria', ['Positive', 'Negative'])
    with col2:
        urine_culture = st.selectbox('Urine Culture Bacteria', ['Positive', 'Negative'])
    with col1:
        calcium = st.number_input('Calcium (mg/dL)', min_value=0.0, max_value=20.0, step=0.1)
    with col2:
        potassium = st.number_input('Potassium (mmol/L)', min_value=0.0, max_value=10.0, step=0.1)
    with col1:
        current_medication = st.text_input('Current Medication')
    with col2:
        treatment_duration = st.number_input('Treatment Duration (days)', min_value=0, max_value=365, step=1)
    with col1:
        treatment = st.text_input('Treatment')
    
    # Validate the inputs
    if st.button('Typhoid Disease Test Result'):
        if not all([patient_id, age, gender, symptoms_severity, hemoglobin, platelet_count, blood_culture, urine_culture, calcium, potassium, current_medication, treatment_duration, treatment]):
            st.error('All fields are required. Please fill in all the information.')
        else:
            try:
                input_data = {
                    'Patient ID': patient_id,
                    'Age': int(age),
                    'Gender': 1 if gender == 'Male' else 0,
                    'Symptoms Severity': int(symptoms_severity),
                    'Hemoglobin (g/dL)': float(hemoglobin),
                    'Platelet Count': int(platelet_count),
                    'Blood Culture Bacteria': 1 if blood_culture == 'Positive' else 0,
                    'Urine Culture Bacteria': 1 if urine_culture == 'Positive' else 0,
                    'Calcium (mg/dL)': float(calcium),
                    'Potassium (mmol/L)': float(potassium),
                    'Current Medication': current_medication,
                    'Treatment Duration': int(treatment_duration),
                    'Treatment': treatment
                }
                
                # Ensure input data is formatted correctly for the model
                model_input = pd.DataFrame([input_data])
                
                # Assuming typhoid_model is already loaded
                typhoid_prediction = typhoid_model.predict(model_input)
                
                if typhoid_prediction[0] == 1:
                    diagnosis = 'The person is likely to have typhoid.'
                else:
                    diagnosis = 'The person is not likely to have typhoid.'

                st.success(diagnosis)

                # Display next steps and resources based on the diagnosis
                st.write("---")
                st.write("### Next Steps and Resources")
                
                if typhoid_prediction[0] == 1:
                    st.markdown("""
                    If your results indicate a likelihood of typhoid, consider these steps:
                    
                    1. **Immediate Medical Attention**: Consult a healthcare provider immediately for proper diagnosis and treatment.
                    2. **Isolation**: To prevent spread, limit contact with others until cleared by a doctor.
                    3. **Hydration**: Maintain proper hydration as typhoid can lead to dehydration.
                    
                    For comprehensive information on typhoid:
                    - [CDC - Typhoid Fever](https://www.cdc.gov/typhoid-fever/index.html)
                    - [WHO - Typhoid](https://www.who.int/news-room/fact-sheets/detail/typhoid)
                    - [Mayo Clinic - Typhoid Fever](https://www.mayoclinic.org/diseases-conditions/typhoid-fever/symptoms-causes/syc-20378661)
                    """)
                else:
                    st.markdown("""
                    Your results suggest a lower likelihood of typhoid, but it's still important to maintain good health:
                    
                    1. **Practice Good Hygiene**: Continue to wash hands frequently and maintain food safety.
                    2. **Stay Vigilant**: Be aware of typhoid symptoms, especially if traveling to high-risk areas.
                    3. **Vaccinations**: Consider typhoid vaccinations if traveling to endemic areas.
                    
                    Learn more about typhoid prevention:
                    - [CDC - Typhoid Prevention](https://www.cdc.gov/typhoid-fever/prevention.html)
                    - [NHS - Typhoid Fever Prevention](https://www.nhs.uk/conditions/typhoid-fever/prevention/)
                    - [WHO - Immunization](https://www.who.int/teams/immunization-vaccines-and-biologicals/diseases/typhoid)
                    """)

                st.write("*Disclaimer: These resources are for informational purposes only and do not constitute medical advice. Always consult with a qualified healthcare professional for medical concerns.*")
                
                # Optionally save the prediction in a database or session
                save_prediction(st.session_state.user.uid, 'Typhoid', input_data, diagnosis)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    
            
        
import pandas as pd
import streamlit as st

def hiv_prediction():
    st.title('HIV Status Prediction using ML')
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input('Age', min_value=18, max_value=100, step=1)
    with col2:
        marital_status = st.selectbox('Marital Status', ['UNMARRIED', 'Married'])
    with col1:
        std = st.selectbox('STD', ['YES', 'NO'])
    with col2:
        education = st.selectbox('Educational Background', ['College Degree', 'High School', 'Graduate Degree', 'Other'])
    with col1:
        hiv_test_past_year = st.selectbox('HIV TEST IN PAST YEAR', ['YES', 'NO'])
    with col2:
        aids_education = st.selectbox('AIDS Education', ['YES', 'NO'])
    with col1:
        seeking_partners = st.selectbox('Places of Seeking Sex Partners', ['Bar', 'None', 'Park', 'Online', 'Other'])
    with col2:
        sexual_orientation = st.selectbox('Sexual Orientation', ['Heterosexual', 'Bisexual', 'Homosexual'])
    with col1:
        drug_taking = st.selectbox('Drug-taking', ['YES', 'NO'])

    if st.button('HIV Status Prediction'):
        # Validate inputs
        if not all([age, marital_status, std, education, hiv_test_past_year, aids_education, seeking_partners, sexual_orientation, drug_taking]):
            st.error('All fields are required. Please fill in all the information.')
        else:
            try:
                # Prepare input data
                input_data = {
                    'Age': int(age),
                    'Marital Status': marital_status,
                    'STD': std,
                    'Educational Background': education,
                    'HIV TEST IN PAST YEAR': hiv_test_past_year,
                    'AIDS Education': aids_education,
                    'Places of Seeking Sex Partners': seeking_partners,
                    'Sexual Orientation': sexual_orientation,
                    'Drug-taking': drug_taking
                }
                
                # Convert input data into a DataFrame for model input
                input_df = pd.DataFrame([input_data])
                
                # Assuming `hiv_model` is already loaded
                hiv_prediction = hiv_model.predict(input_df)
                
                # Determine HIV status based on prediction
                hiv_status = 'POSITIVE' if hiv_prediction[0] == 1 else 'NEGATIVE'
                
                # Show success message
                st.success(f'The predicted HIV status is: {hiv_status}')
                
                # Display next steps and resources based on the prediction
                st.write("---")
                st.write("### Next Steps and Resources")
                
                if hiv_prediction[0] == 1:
                    st.markdown("""
                    If your results indicate a positive HIV status, consider these steps:
                    
                    1. **Confirm the Result**: Get a confirmatory test from a healthcare provider.
                    2. **Seek Medical Care**: Consult with an HIV specialist for proper treatment and care.
                    3. **Learn About HIV**: Educate yourself about living with HIV and available treatments.
                    4. **Support**: Consider joining support groups or counseling services.
                    
                    For comprehensive information on HIV:
                    - [CDC - HIV Basics](https://www.cdc.gov/hiv/basics/index.html)
                    - [WHO - HIV/AIDS](https://www.who.int/health-topics/hiv-aids)
                    - [HIV.gov - Living With HIV](https://www.hiv.gov/hiv-basics/staying-in-hiv-care/other-related-health-issues/taking-care-of-yourself)
                    """)
                else:
                    st.markdown("""
                    Your results suggest a negative HIV status, but it's important to:
                    
                    1. **Regular Testing**: Continue getting tested regularly, especially if you engage in high-risk behaviors.
                    2. **Prevention**: Learn about and practice HIV prevention methods, including safe sex practices and PrEP if appropriate.
                    3. **Stay Informed**: Keep yourself updated on HIV/AIDS information and prevention strategies.
                    
                    Learn more about HIV prevention:
                    - [CDC - HIV Prevention](https://www.cdc.gov/hiv/basics/prevention.html)
                    - [WHO - HIV Prevention](https://www.who.int/news-room/fact-sheets/detail/hiv-aids)
                    - [HIV.gov - HIV Prevention](https://www.hiv.gov/hiv-basics/hiv-prevention/using-hiv-medication-to-reduce-risk/pre-exposure-prophylaxis)
                    """)

                st.write("*Disclaimer: This prediction is based on a machine learning model and should not be considered as a medical diagnosis. Always consult with a qualified healthcare professional for medical concerns and proper HIV testing.*")
                
                # Optionally save the prediction (e.g., to a database or session)
                save_prediction(st.session_state.user.uid, 'HIV', input_data, hiv_status)

            except Exception as e:
                st.error(f"An error occurred: {e}")
            
            



def generate_patient_diagnosis_report():
    st.subheader("Generate Patient Diagnosis Report")

    # Patient Information
    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Patient Age", min_value=0, max_value=120)
    patient_gender = st.selectbox("Patient Gender", ["Male", "Female", "Other"])

    # Disease Prediction
    disease_type = st.selectbox("Select Disease Type", 
                                ['Diabetes', 'Heart Disease', 'Parkinsons', 'HIV', 'Anemia', 'Typhoid'])

    # Call the appropriate prediction function based on the selected disease type
    if disease_type == 'Diabetes':
        prediction_result = diabetes_prediction()
    elif disease_type == 'Heart Disease':
        prediction_result = heart_disease_prediction()
    elif disease_type == 'Parkinsons':
        prediction_result = parkinsons_prediction()
    elif disease_type == 'HIV':
        prediction_result = hiv_prediction()
    elif disease_type == 'Anemia':
        prediction_result = anemia_prediction()
    elif disease_type == 'Typhoid':
        prediction_result = typhoid_prediction()

    # Additional Notes
    additional_notes = st.text_area("Additional Notes")

    if st.button("Generate Diagnosis Report"):
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph("Patient Diagnosis Report", styles['Title']))
        elements.append(Paragraph(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Paragraph("", styles['Normal']))

        # Patient Information Table
        patient_data = [
            ["Patient Name", patient_name],
            ["Age", patient_age],
            ["Gender", patient_gender]
        ]
        patient_table = Table(patient_data)
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (-1, -1), colors.beige),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(patient_table)
        elements.append(Paragraph("", styles['Normal']))

        # Diagnosis Information
        elements.append(Paragraph(f"Disease Type: {disease_type}", styles['Heading2']))
        elements.append(Paragraph(f"Prediction Result: {prediction_result}", styles['Normal']))
        elements.append(Paragraph("", styles['Normal']))

        # Additional Notes
        elements.append(Paragraph("Additional Notes:", styles['Heading2']))
        elements.append(Paragraph(additional_notes, styles['Normal']))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)

        # Offer PDF for download
        b64 = base64.b64encode(buffer.getvalue()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="patient_diagnosis_report.pdf">Download Patient Diagnosis Report</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Save to database
        save_diagnosis_report(st.session_state.user.uid, {
            'patient_name': patient_name,
            'patient_age': patient_age,
            'patient_gender': patient_gender,
            'disease_type': disease_type,
            'prediction_result': prediction_result,
            'additional_notes': additional_notes,
            'timestamp': datetime.datetime.now()
        })

        st.success("Diagnosis report generated and saved successfully!")

def save_diagnosis_report(user_id, report_data):
    db.collection('users').document(user_id).collection('diagnosis_reports').add(report_data)

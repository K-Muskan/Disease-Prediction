import streamlit as st
from prediction_functions import diabetes_prediction, heart_disease_prediction, parkinsons_prediction, anemia_prediction, hiv_prediction, typhoid_prediction, generate_patient_diagnosis_report
from user_functions import view_prediction_history, generate_charts


def staff():
    # Set background color for the main page
    st.markdown(
        """
        <style>
        .css-1d391kg {background-color: #f55523;}
        .css-1p2g6ia {color: #ffffff; background-color: #4CAF50;}
        .css-1r6upfe {background-color: #eeeeee;}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title and sidebar layout
    st.title('Staff Dashboard', anchor="staff_dashboard")

    with st.sidebar:
        # Customize welcome message and style
        st.subheader(f'Welcome {st.session_state.user.display_name or st.session_state.user.email}')
        st.markdown(f"<p style='font-size: 14px; color: #4CAF50;'>Hello, {st.session_state.user.display_name or 'Staff'}! Choose an option below.</p>", unsafe_allow_html=True)

        # Add background color to select box
        selected = st.selectbox(
            'Select Function',
            ['Diabetes Prediction',
             'Heart Disease Prediction',
             'Parkinsons Prediction',
             'HIV Prediction',
             'Anemia Prediction',
            #  'Typhoid Prediction',
             'Patient Diagnosis Report',
             'Prediction History',
             'Prediction Analytics'],
            key="functions"
        )

        # Customize logout button
        if st.button('Logout', key='logout_btn'):
            st.session_state.clear()
            st.rerun()

    # Functionality based on the selected option
    if selected == 'Diabetes Prediction':
        diabetes_prediction()
    elif selected == 'Heart Disease Prediction':
        heart_disease_prediction()
    elif selected == 'Parkinsons Prediction':
        parkinsons_prediction()
    elif selected == 'Anemia Prediction':
        anemia_prediction()
    elif selected == 'HIV Prediction':
        hiv_prediction()
    elif selected == 'Typhoid Prediction':
        typhoid_prediction()
    # elif selected == 'Breast Cancer Prediction':
    #     breast_cancer_prediction()
    elif selected == 'Patient Diagnosis Report':
        generate_patient_diagnosis_report()
    elif selected == 'Prediction History':
        view_prediction_history()
    elif selected == 'Prediction Analytics':
        generate_charts(st.session_state.user.uid)

    # Additional styling
    st.markdown(
        """
        <style>
        .css-1s8ix4j {
            font-size: 16px;
            color: #555555;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

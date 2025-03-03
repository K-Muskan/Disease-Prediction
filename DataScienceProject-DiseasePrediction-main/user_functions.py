import streamlit as st
from firebase_config import db
import pandas as pd
import plotly.express as px
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from firebase_admin import firestore


#def view_prediction_history():
    #st.subheader("Prediction History")
    #predictions = get_user_predictions(st.session_state.user.uid)
    
    #for pred in predictions:
        #with st.expander(f"{pred['type']} - {pred['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
            #st.write(f"Result: {pred['result']}")
            #st.write("Input Data:")
            #or key, value in pred['input_data'].items():
                #st.write(f"- {key}: {value}")

    #if st.button("Generate Report"):
        #report_buffer = generate_report(st.session_state.user, predictions)
        #b64 = base64.b64encode(report_buffer.getvalue()).decode()
        #href = f'<a href="data:application/pdf;base64,{b64}" download="prediction_report.pdf">Download PDF Report</a>'
        #st.markdown(href, unsafe_allow_html=True)
        

def view_prediction_history():
    st.subheader("Prediction and Diagnosis History")
    
    predictions = get_user_predictions(st.session_state.user.uid)
    diagnosis_reports = get_user_diagnosis_reports(st.session_state.user.uid)
    
    st.write("### Predictions")
    for pred in predictions:
        with st.expander(f"{pred['type']} - {pred['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
            st.write(f"Result: {pred['result']}")
            st.write("Input Data:")
            # If input_data is a list, display the list elements directly
            if isinstance(pred['input_data'], list):
                for idx, value in enumerate(pred['input_data']):
                    st.write(f"- Input {idx + 1}: {value}")
            else:
                for key, value in pred['input_data'].items():
                    st.write(f"- {key}: {value}")
    
    st.write("### Diagnosis Reports")
    for report in diagnosis_reports:
        with st.expander(f"{report['disease_type']} - {report['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
            st.write(f"Patient: {report['patient_name']}")
            st.write(f"Age: {report['patient_age']}")
            st.write(f"Gender: {report['patient_gender']}")
            st.write(f"Prediction Result: {report['prediction_result']}")
            st.write(f"Additional Notes: {report['additional_notes']}")



def get_user_diagnosis_reports(user_id):
    reports = db.collection('users').document(user_id).collection('diagnosis_reports').order_by('timestamp', direction=firestore.Query.DESCENDING).get()
    return [report.to_dict() for report in reports]
        
        


def generate_charts(user_id):
    predictions = get_user_predictions(user_id)
    if not predictions:
        st.warning("No prediction data available to generate charts.")
        return

    df = pd.DataFrame(predictions)
    
    # Chart 1: Prediction types over time
    fig1 = px.histogram(df, x='timestamp', color='type', title='Prediction Types Over Time')
    st.plotly_chart(fig1)

    # Chart 2: Prediction results distribution
    result_counts = df['result'].value_counts()
    fig2 = px.pie(values=result_counts.values, names=result_counts.index, title='Distribution of Prediction Results')
    st.plotly_chart(fig2)

    # Chart 3: Prediction types distribution
    type_counts = df['type'].value_counts()
    fig3 = px.bar(x=type_counts.index, y=type_counts.values, title='Distribution of Prediction Types')
    st.plotly_chart(fig3)


# Helper function used by both view_prediction_history and generate_charts
def get_user_predictions(user_id):
    predictions = db.collection('users').document(user_id).collection('predictions').order_by('timestamp', direction=firestore.Query.DESCENDING).get()
    return [pred.to_dict() for pred in predictions]





# Helper function for generating PDF reports
def generate_report(user, predictions):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Disease Prediction Report for {user.display_name or user.email}")
    
    y = 700
    for pred in predictions:
        c.drawString(100, y, f"Date: {pred['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(100, y-20, f"Type: {pred['type']}")
        c.drawString(100, y-40, f"Result: {pred['result']}")
        y -= 60
        if y < 100:
            c.showPage()
            y = 750
    
    c.save()
    buffer.seek(0)
    return buffer


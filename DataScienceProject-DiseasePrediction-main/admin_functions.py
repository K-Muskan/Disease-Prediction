import streamlit as st
from firebase_config import db
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import base64

def manage_database():
    st.subheader("Manage System Database")
    
    # User Management
    st.write("### User Management")
    users = db.collection('users').get()
    for user in users:
        user_data = user.to_dict()
        with st.expander(f"User: {user_data['email']}"):
            st.write(f"Role: {user_data['role']}")
            new_role = st.selectbox("Change Role", ['staff', 'admin'], index=0 if user_data['role'] == 'staff' else 1, key=user.id)
            if st.button("Update Role", key=f"update_{user.id}"):
                db.collection('users').document(user.id).update({'role': new_role})
                st.success("Role updated successfully")

    # Data Cleanup
    st.write("### Data Cleanup")
    if st.button("Remove Old Predictions (>30 days)"):
        # Implement logic to remove old predictions
        st.success("Old predictions removed successfully")

def view_overall_predictions():
    st.subheader("View Overall Predictions")
    
    all_predictions = []
    users = db.collection('users').get()
    for user in users:
        predictions = user.reference.collection('predictions').get()
        for pred in predictions:
            pred_data = pred.to_dict()
            pred_data['user_id'] = user.id
            all_predictions.append(pred_data)
    
    if not all_predictions:
        st.warning("No predictions found in the database.")
        return

    df = pd.DataFrame(all_predictions)
    
    st.write("### Prediction Statistics")
    st.write(f"Total Predictions: {len(df)}")
    
    if 'user_id' in df.columns:
        st.write(f"Unique Users: {df['user_id'].nunique()}")
    else:
        st.warning("User ID information not available in the predictions data.")
    
    if 'type' in df.columns:
        fig = px.pie(df, names='type', title='Distribution of Prediction Types')
        st.plotly_chart(fig)
    else:
        st.warning("Prediction type information not available in the data.")
    
    st.write("### Recent Predictions")
    if 'timestamp' in df.columns:
        st.dataframe(df.sort_values('timestamp', ascending=False).head(10))
    else:
        st.dataframe(df.head(10))
        st.warning("Timestamp information not available. Showing unsorted predictions.")

def generate_admin_reports():
    st.subheader("Generate Admin Reports")
    
    report_type = st.selectbox("Select Report Type", ["User Activity", "Prediction Summary"])
    
    if report_type == "User Activity":
        users = db.collection('users').get()
        user_activity = []
        for user in users:
            predictions = user.reference.collection('predictions').get()
            user_activity.append({
                'user_id': user.id,
                'prediction_count': len(predictions),
                'last_active': max([p.to_dict()['timestamp'] for p in predictions]) if predictions else None
            })
        df = pd.DataFrame(user_activity)
        st.dataframe(df)
    
    elif report_type == "Prediction Summary":
        all_predictions = []
        users = db.collection('users').get()
        for user in users:
            predictions = user.reference.collection('predictions').get()
            all_predictions.extend([p.to_dict() for p in predictions])
        df = pd.DataFrame(all_predictions)
        st.write(f"Total Predictions: {len(df)}")
        if 'type' in df.columns:
            st.write(df['type'].value_counts())
        else:
            st.warning("No 'type' column found in the predictions data.")
    
    if st.button("Generate PDF Report"):
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.drawString(100, 750, f"Admin Report: {report_type}")
        # Add more content to the PDF based on the report type
        c.save()
        pdf_buffer.seek(0)
        b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="admin_report.pdf">Download PDF Report</a>'
        st.markdown(href, unsafe_allow_html=True)
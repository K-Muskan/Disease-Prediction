import streamlit as st
from admin_functions import manage_database, view_overall_predictions, generate_admin_reports
from firebase_admin import auth, firestore
from firebase_config import db
import secrets
from datetime import datetime

def generate_admin_invite_code():
    return secrets.token_urlsafe(16)

def create_admin_invite():
    invite_code = generate_admin_invite_code()
    db.collection('admin_invites').document(invite_code).set({
        'created_at': datetime.now(),
        'used': False
    })
    return invite_code

def manage_users():
    st.subheader("User Management")
    users = db.collection('users').get()
    for user in users:
        user_data = user.to_dict()
        with st.expander(f"User: {user_data['email']}"):
            st.write(f"Current Role: {user_data['role']}")
            new_role = st.selectbox("Change Role", ['staff', 'admin'], 
                                    index=0 if user_data['role'] == 'staff' else 1, 
                                    key=f"role_{user.id}")
            if st.button("Update Role", key=f"update_role_{user.id}"):
                # Update role in Firestore
                db.collection('users').document(user.id).update({'role': new_role})
                # Update custom claims in Firebase Auth
                auth.set_custom_user_claims(user.id, {'role': new_role})
                st.success("Role updated successfully")

def admin_page():
    st.title('Admin Dashboard')
    with st.sidebar:
        st.image("/Users/user/Documents/Tutorials/machineLearning/multiple-disease-prediction-streamlit-app-main/multipleDiseaseProject/addfeatures/atu.png", width=150, use_column_width=True)
        
        st.subheader(f'Welcome Admin {st.session_state.user.display_name or st.session_state.user.email}')
        
        selected = st.selectbox('Select Function',
                                ['Manage Database',
                                 'View Overall Predictions',
                                 'Generate Admin Reports',
                                 'Create Admin Invite'])
        
        if st.button('Logout'):
            st.session_state.clear()
            st.rerun()
    
    if selected == 'Manage Database':
        #manage_database()
        manage_users()
    elif selected == 'View Overall Predictions':
        view_overall_predictions()
    elif selected == 'Generate Admin Reports':
        generate_admin_reports()
    elif selected == 'Create Admin Invite':
        st.subheader("Create Admin Invite")
        if st.button("Generate New Admin Invite Code"):
            try:
                new_invite_code = create_admin_invite()
                st.success(f"New admin invite code generated: {new_invite_code}")
                st.warning("Make sure to save this code securely, as it will not be displayed again!")
            except Exception as e:
                st.error(f"An error occurred while generating the invite code: {str(e)}")





#import streamlit as st
#from admin_functions import manage_database, view_overall_predictions, generate_admin_reports

#def admin_page():
    #st.title('Admin Dashboard')

   # with st.sidebar:
        #st.image("/Users/user/Documents/Tutorials/machineLearning/multiple-disease-prediction-streamlit-app-main/multipleDiseaseProject/addfeatures/atu.png", width=150, use_column_width=True)
        
        #st.subheader(f'Welcome Admin {st.session_state.user.display_name or st.session_state.user.email}')
        
       # selected = st.selectbox('Select Function',
                                #['Manage Database',
                                 #'View Overall Predictions',
                                 #'Generate Admin Reports'])
        
        #if st.button('Logout'):
            #st.session_state.clear()
            #st.rerun()

    #if selected == 'Manage Database':
       # manage_database()
    #elif selected == 'View Overall Predictions':
        #view_overall_predictions()
    #elif selected == 'Generate Admin Reports':
        ##generate_admin_reports()
        
        
        

        
        
        
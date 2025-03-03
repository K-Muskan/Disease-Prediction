import streamlit as st
from firebase_admin import auth
from firebase_config import db
import re
import logging
from firebase_admin import firestore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def validate_password(password):
    pattern = r".{8,}"  # Password length should be at least 8 characters
    return re.match(pattern, password) is not None

def sign_up():
    st.header('Sign Up')
    
    with st.form("signup_form"):
        email = st.text_input('Email', placeholder='Enter Your Email')
        username = st.text_input('Username', placeholder='Enter Your Username')
        password = st.text_input('Password', placeholder='Enter Your Password', type='password')
        confirm_password = st.text_input('Confirm Password', placeholder='Confirm Your Password', type='password')
        role = st.selectbox('Role', ['Staff', 'Admin'])
        admin_invite_code = st.text_input('Admin Invite Code', type='password') if role == 'Admin' else None
        
        submitted = st.form_submit_button("Sign Up")
        
        if submitted:
            if role == 'Admin':
                if not admin_invite_code:
                    st.error('Admin invite code is required for admin sign-up.')
                    return
                # Check if the invite code exists and is valid
                invite_ref = db.collection('admin_invites').document(admin_invite_code)
                try:
                    invite_doc = invite_ref.get()
                    if not invite_doc.exists:
                        st.error('Invalid admin invite code')
                        return
                    if invite_doc.to_dict().get('used', False):
                        st.error('This admin invite code has already been used')
                        return
                except Exception as e:
                    logger.error(f"Error checking admin invite: {str(e)}")
                    st.error('An error occurred while verifying the admin invite code')
                    return
            
            if not email or not username or not password or not confirm_password:
                st.error('All fields are required.')
            elif not validate_email(email):
                st.error('Invalid email format.')
            elif len(username) < 3:
                st.error('Username must be at least 3 characters long.')
            elif not validate_password(password):
                st.error('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
            elif password != confirm_password:
                st.error('Passwords do not match.')
            else:
                try:
                    user = auth.create_user(
                        email=email,
                        password=password,
                        display_name=username
                    )
                    # Set custom claims for user role
                    auth.set_custom_user_claims(user.uid, {'role': role.lower()})
                    
                    # Create a user document in Firestore
                    db.collection('users').document(user.uid).set({
                        'email': email,
                        'username': username,
                        'role': role.lower()
                    })
                    
                    if role == 'Admin':
                        # Mark the invite code as used
                        invite_ref.update({'used': True})
                    
                    logger.info(f"User created successfully: {user.uid}")
                    st.success('Account created successfully')
                    st.balloons()
                    st.session_state['page'] = 'login'
                    st.rerun()
                except auth.EmailAlreadyExistsError:
                    st.error('An account with this email already exists.')
                except Exception as e:
                    logger.error(f"Error during signup: {str(e)}")
                    st.error(f'An error occurred: {str(e)}')
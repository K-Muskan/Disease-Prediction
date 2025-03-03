import streamlit as st
from firebase_admin import auth, credentials
from firebase_config import db
import logging
import requests
import json

# Set the page configuration
# st.set_page_config(
#     page_title="Login Page",
#     page_icon="🔒",
#     layout="centered",  # Options: "centered" or "wide"
#     initial_sidebar_state="collapsed",  # Options: "expanded", "collapsed", or "auto"
# )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Firebase project's web API key
FIREBASE_WEB_API_KEY = "AIzaSyB5w-Rdar-wvXUCtLBNI32jhXeM074HaqI"

def verify_password(email, password):
    request_data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    
    try:
        response = requests.post(rest_api_url, data=json.dumps(request_data))
        if response.ok:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        return False


def send_password_reset_email(email):
    request_data = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"
    
    try:
        response = requests.post(rest_api_url, data=json.dumps(request_data))
        if response.ok:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error sending password reset email: {str(e)}")
        return False


def login():
    st.title("🔒 Disease Prediction App")
    st.markdown("---")

    with st.form("login_form", clear_on_submit=False):
        st.subheader("Welcome Back! Please Log In")
        email = st.text_input("📧 Email", placeholder="Enter Your Email")
        password = st.text_input("🔑 Password", placeholder="Enter Your Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("🔓 Login", type="primary")
        with col2:
            forgot_button = st.form_submit_button("❓ Forgot Password")
        
        if login_button:
            if not email or not password:
                st.error("⚠️ Both email and password are required.")
            else:
                try:
                    if verify_password(email, password):
                        user = auth.get_user_by_email(email)
                        user_doc = db.collection("users").document(user.uid).get()
                        if user_doc.exists:
                            user_data = user_doc.to_dict()
                            role = user_data.get("role")
                            if role not in ["admin", "staff"]:
                                st.error("⚠️ Invalid user role. Contact admin.")
                                return
                            st.session_state["user"] = user
                            st.session_state["role"] = role
                            st.session_state["page"] = "admin" if role == "admin" else "staff"
                            st.success(f"✅ Logged in successfully as **{role.capitalize()}**")
                            st.experimental_rerun()
                        else:
                            st.error("⚠️ User data not found. Contact admin.")
                    else:
                        st.error("❌ Invalid email or password.")
                except Exception as e:
                    logger.error(f"Login error: {str(e)}")
                    st.error("⚠️ Error during login. Try again later.")

        if forgot_button:
            if not email:
                st.error("⚠️ Please enter your email address to reset your password.")
            else:
                if send_password_reset_email(email):
                    st.success("📧 Password reset email sent. Check your inbox.")
                else:
                    st.error("⚠️ Error sending password reset email. Try again later.")

    st.markdown("---")
    st.caption("🔒 Secure Authentication | Powered by Firebase")


if __name__ == "__main__":
    login()

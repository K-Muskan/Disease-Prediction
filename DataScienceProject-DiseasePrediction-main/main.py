import streamlit as st
from login_page import login
from signup import sign_up
from staff_page import staff
from admin_page import admin_page

st.set_page_config(page_title='Disease Prediction App', page_icon="🏥", initial_sidebar_state='expanded')

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    
    if st.session_state['page'] == 'login':
        login()
    elif st.session_state['page'] == 'signup':
        sign_up()
    elif st.session_state['page'] == 'staff':
        staff()
    elif st.session_state['page'] == 'admin':
        admin_page()
    
    if st.session_state['page'] in ['login', 'signup']:
        if st.button('Switch to ' + ('Login' if st.session_state['page'] == 'signup' else 'Sign Up')):
            st.session_state['page'] = 'login' if st.session_state['page'] == 'signup' else 'signup'
            st.rerun()

if __name__ == "__main__":
    main()
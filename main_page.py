import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials
import json
import requests

# Set layout at the beginning to avoid flickering
st.set_page_config(layout="wide")

# Initialize Firebase only if it's not already initialized
if not firebase_admin._apps:
    firebase_config = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

# Sidebar Image - Load Only Once
if "sidebar_image_loaded" not in st.session_state:
    st.session_state["sidebar_image_loaded"] = True
    with st.sidebar:
        st.image("assets/logo/Colorlogo.png", use_column_width=True)

# Sidebar Buttons - Avoid Unnecessary Reruns
with st.sidebar:
    if 'username' in st.session_state and st.session_state['username']:
        if st.button("Log Out"):
            st.session_state['page'] = 'authentication'
            st.rerun()
    else:
        if st.button("Login / Signup"):
            st.session_state['page'] = 'authentication'
            st.rerun()

# Authentication Page
def authentication_page():
    st.title('Welcome to :violet[Craftify] :sunglasses:')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def login():
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']
            st.session_state.signedout = False
        except:
            st.warning('Login Failed')

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = True

    if st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            if st.button('Create my account'):
                sign_up_with_email_and_password(email=email, password=password, username=username)
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
        else:
            st.button('Login', on_click=login)

    else:
        st.text('Name: ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        if st.button('Sign out'):
            st.session_state.signedout = True
            st.session_state.username = ''
            st.session_state.useremail = ''
            st.rerun()

        if st.button('Go to the App →'):
            st.session_state['page'] = 'main_app'
            st.rerun()

# Main Content Routing
if 'page' in st.session_state:
    if st.session_state['page'] == 'authentication':
        authentication_page()
    elif st.session_state['page'] == 'main_app':
        import streamlit_app  # Dynamically load the main app
        streamlit_app.main()
    else:
        st.write("Welcome to Craftify...  Get Noticed, Get Hired!")
else:
    st.markdown("<h1 style='text-align: center; font-size: 50px; text-transform: uppercase;'>UNDERSTAND JOB REQUIREMENTS. TWEAK YOUR RESUME. APPLY!</h1>", unsafe_allow_html=True)
    st.image("assets/logo/karn.jpg", use_column_width=True)



import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials
import json
import requests

# Set page layout at the very beginning
st.set_page_config(layout="wide")

# Hide the Streamlit menu and footer
st.markdown("""
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    </style>
    """, unsafe_allow_html=True)

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

# Authentication Functions
def sign_in_with_email_and_password(email, password):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        payload = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        r = requests.post(rest_api_url, params={"key": st.secrets["firebase_api_key"]}, data=payload)
        return r.json()
    except Exception as e:
        st.warning(f'Sign-in failed: {e}')

# Authentication Page
def authentication_page():
    st.title('Welcome to :violet[Craftify] :sunglasses:')

    if 'signedout' not in st.session_state:
        st.session_state["signedout"] = True

    if st.session_state["signedout"]:
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            user_info = sign_in_with_email_and_password(email, password)
            if 'email' in user_info:
                st.session_state['username'] = user_info.get('displayName', '')
                st.session_state['useremail'] = user_info['email']
                st.session_state['signedout'] = False
                st.rerun()
            else:
                st.warning('Login Failed')

    else:
        st.text('Name: ' + st.session_state.get('username', ''))
        st.text('Email: ' + st.session_state.get('useremail', ''))
        if st.button('Sign out'):
            st.session_state['signedout'] = True
            st.session_state['username'] = ''
            st.session_state['useremail'] = ''
            st.rerun()

# Main Page
def main_page():
    # Sidebar with logo (loads only once)
    if "sidebar_image_loaded" not in st.session_state:
        st.session_state["sidebar_image_loaded"] = True
        with st.sidebar:
            st.image("assets/logo/Colorlogo.png", use_column_width=True)

    # Authentication Control
    if 'page' not in st.session_state:
        st.session_state['page'] = 'main_app'

    if st.session_state['page'] == 'authentication':
        authentication_page()
    elif st.session_state['page'] == 'main_app':
        import streamlit_app
        streamlit_app.main()
    else:
        st.markdown("<h1 style='text-align: center;'>UNDERSTAND JOB REQUIREMENTS. TWEAK YOUR RESUME. APPLY!</h1>", unsafe_allow_html=True)
        st.image("assets/logo/karn.jpg", use_column_width=True)

if __name__ == "__main__":
    main_page()

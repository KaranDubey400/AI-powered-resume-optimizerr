import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials
import json
import requests

# Cache Firebase Initialization
@st.cache_resource
def initialize_firebase():
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
    return firebase_admin.initialize_app(cred)

if not firebase_admin._apps:
    initialize_firebase()

# Sign-In and Sign-Up Functions (Optimized Error Handling)
def sign_in_with_email_and_password(email, password):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    payload = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    r = requests.post(rest_api_url, params={"key": st.secrets["firebase_api_key"]}, data=payload)
    data = r.json()
    if 'error' in data:
        return None, data['error']['message']
    return {'email': data['email'], 'username': data.get('displayName', '')}, None

def authentication_page():
    st.title('Welcome to :violet[Craftify] :sunglasses:')
    
    if 'signedout' not in st.session_state:
        st.session_state['signedout'] = True
    
    if st.session_state['signedout']:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address', key='email_input')
        password = st.text_input('Password', type='password', key='password_input')
        
        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            if st.button('Create my account'):
                sign_up_with_email_and_password(email, password, username)
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
        else:
            if st.button('Login'):
                user_info, error = sign_in_with_email_and_password(email, password)
                if error:
                    st.warning(f'Login Failed: {error}')
                else:
                    st.session_state['username'] = user_info['username']
                    st.session_state['useremail'] = user_info['email']
                    st.session_state['signedout'] = False
    else:
        st.text(f'Name: {st.session_state.username}')
        st.text(f'Email: {st.session_state.useremail}')
        
        if st.button('Sign out'):
            st.session_state.clear()
            st.session_state['signedout'] = True
        
        if st.button('Go to the App →'):
            st.experimental_set_query_params(page='main_app')
            st.session_state['page'] = 'main_app'

# Main Page

def main_page():
    st.set_page_config(layout="wide")
    
    with st.sidebar:
        st.image("assets/logo/Colorlogo.png")
        if 'username' in st.session_state and st.session_state['username']:
            if st.button("Log Out"):
                st.session_state.clear()
                st.experimental_set_query_params(page='authentication')
        else:
            if st.button("Go to Authentication"):
                st.experimental_set_query_params(page='authentication')
    
    query_params = st.experimental_get_query_params()
    current_page = query_params.get("page", ["main"])[0]
    
    if current_page == 'authentication':
        authentication_page()
    elif current_page == 'main_app':
        import streamlit_app
        streamlit_app.main()
    else:
        st.markdown("<h1 style='text-align: center;'>UNDERSTAND JOB REQUIREMENTS. TWEAK YOUR RESUME. APPLY!</h1>", unsafe_allow_html=True)
        st.image("assets/logo/karn.jpg", use_column_width='auto')

if __name__ == "__main__":
    main_page()

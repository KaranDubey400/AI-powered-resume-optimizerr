import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials
import json
import requests

# ✅ Set the page configuration at the very top
st.set_page_config(layout="wide")

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

# --- Firebase Auth REST API Functions ---

def sign_in_with_email_and_password(email, password):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    payload = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    r = requests.post(rest_api_url, params={"key": st.secrets["firebase_api_key"]}, data=payload)
    data = r.json()
    if 'error' in data:
        return None, data['error']['message']
    return {'email': data['email'], 'username': data.get('displayName', '')}, None

def sign_up_with_email_and_password(email, password, username):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
    payload = json.dumps({
        "email": email,
        "password": password,
        "displayName": username,
        "returnSecureToken": True
    })
    r = requests.post(rest_api_url, params={"key": st.secrets["firebase_api_key"]}, data=payload)
    data = r.json()
    if 'error' in data:
        return False, data["error"]["message"]
    return True, None

def send_password_reset_email(email):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
    payload = json.dumps({
        "requestType": "PASSWORD_RESET",
        "email": email
    })
    r = requests.post(rest_api_url, params={"key": st.secrets["firebase_api_key"]}, data=payload)
    data = r.json()
    if 'error' in data:
        return False, data['error']['message']
    return True, None

# --- UI Components ---

def card_container():
    st.markdown(
        """
        <style>
        .auth-card {
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.10);
            padding: 2.5rem 2rem 2rem 2rem;
            max-width: 400px;
            margin: 3rem auto 2rem auto;
        }
        .auth-title {
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            color: #6C63FF;
            margin-bottom: 1.5rem;
        }
        .auth-link {
            color: #6C63FF;
            text-decoration: underline;
            cursor: pointer;
        }
        .auth-link:hover {
            color: #4834d4;
        }
        </style>
        <div class="auth-card">
        """,
        unsafe_allow_html=True
    )

def card_close():
    st.markdown("</div>", unsafe_allow_html=True)

# --- Auth Forms ---

def login_form():
    card_container()
    st.markdown('<div class="auth-title">Login</div>', unsafe_allow_html=True)
    email = st.text_input('Email Address', key='login_email')
    password = st.text_input('Password', type='password', key='login_password')
    col1, col2 = st.columns([1, 1])
    with col1:
        login_btn = st.button('Login', use_container_width=True)
    with col2:
        st.markdown('<span class="auth-link" onclick="window.location.hash=\'reset\'">Forgot Password?</span>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="auth-link" onclick="window.location.hash=\'signup\'">New user? Sign up</span>', unsafe_allow_html=True)
    card_close()
    return login_btn, email, password

def signup_form():
    card_container()
    st.markdown('<div class="auth-title">Sign Up</div>', unsafe_allow_html=True)
    email = st.text_input('Email Address', key='signup_email')
    password = st.text_input('Password', type='password', key='signup_password')
    username = st.text_input('Username', key='signup_username')
    signup_btn = st.button('Create Account', use_container_width=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="auth-link" onclick="window.location.hash=\'login\'">Already have an account? Login</span>', unsafe_allow_html=True)
    card_close()
    return signup_btn, email, password, username

def reset_form():
    card_container()
    st.markdown('<div class="auth-title">Reset Password</div>', unsafe_allow_html=True)
    email = st.text_input('Enter your email address', key='reset_email')
    reset_btn = st.button('Send Reset Email', use_container_width=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<span class="auth-link" onclick="window.location.hash=\'login\'">Back to Login</span>', unsafe_allow_html=True)
    card_close()
    return reset_btn, email

# --- Main Auth Page ---
def authentication_page():
    st.image("assets/logo/Colorlogo.png", width=120)
    st.markdown("<h2 style='text-align:center; color:#6C63FF;'>Welcome to <b>Craftify</b> :sunglasses:</h2>", unsafe_allow_html=True)
    # Routing based on hash
    hash_route = st.experimental_get_query_params().get('auth', ['login'])[0]
    if 'signedout' not in st.session_state:
        st.session_state['signedout'] = True
    if st.session_state['signedout']:
        if hash_route == 'signup':
            signup_btn, email, password, username = signup_form()
            if signup_btn:
                if not email or not password or not username:
                    st.error('Please fill all fields!')
                elif len(password) < 6:
                    st.warning('Password must be at least 6 characters.')
                elif '@' not in email or '.' not in email:
                    st.warning('Please enter a valid email address.')
                else:
                    with st.spinner('Creating your account...'):
                        success, error = sign_up_with_email_and_password(email, password, username)
                    if success:
                        st.success('Account created successfully! Please login.')
                        st.balloons()
                        st.experimental_set_query_params(auth='login')
                    else:
                        if error == 'EMAIL_EXISTS':
                            st.error('This email is already registered. Please login or use another email.')
                        elif error == 'WEAK_PASSWORD : Password should be at least 6 characters':
                            st.error('Password is too weak. Please use at least 6 characters.')
                        else:
                            st.error(f'Sign up failed: {error}')
        elif hash_route == 'reset':
            reset_btn, email = reset_form()
            if reset_btn:
                if not email:
                    st.error('Please enter your email!')
                else:
                    with st.spinner('Sending reset email...'):
                        success, error = send_password_reset_email(email)
                    if success:
                        st.success('Password reset email sent! Check your inbox.')
                    else:
                        st.error(f'Error: {error}')
        else:  # login
            login_btn, email, password = login_form()
            if login_btn:
                if not email or not password:
                    st.error('Please enter both email and password!')
                else:
                    with st.spinner('Logging you in...'):
                        user_info, error = sign_in_with_email_and_password(email, password)
                    if error:
                        if error == 'EMAIL_NOT_FOUND':
                            st.error('No account found with this email. Please sign up first.')
                        elif error == 'INVALID_PASSWORD':
                            st.error('Incorrect password. Please try again.')
                        elif error == 'USER_DISABLED':
                            st.error('This user account has been disabled.')
                        else:
                            st.warning(f'Login Failed: {error}')
                    else:
                        st.session_state['username'] = user_info['username']
                        st.session_state['useremail'] = user_info['email']
                        st.session_state['signedout'] = False
                        st.success('Login successful!')
                        st.experimental_set_query_params(page='main_app')
    else:
        st.markdown(f'<div class="auth-card"><b>Name:</b> {st.session_state.username}<br><b>Email:</b> {st.session_state.useremail}</div>', unsafe_allow_html=True)
        if st.button('Sign out', use_container_width=True):
            st.session_state.clear()
            st.session_state['signedout'] = True
            st.experimental_set_query_params(auth='login')
        if st.button('Go to the App →', use_container_width=True):
            st.experimental_set_query_params(page='main_app')
            st.session_state['page'] = 'main_app'

# Main Page

def main_page():
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

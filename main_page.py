import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
import json
import requests

# Load environment variables
load_dotenv()

# Initialize Firebase only if it's not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("authentication-31d27-090cbf89d0ac.json")
    firebase_admin.initialize_app(cred)

# Sign-Up/Sign-In Functions
def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": return_secure_token
        }
        if username:
            payload["displayName"] = username
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": "AIzaSyALebezYE7_X1heM1sypIeAJmWI8QyModQ"}, data=payload)
        try:
            return r.json()['email']
        except:
            st.warning(r.json())
    except Exception as e:
        st.warning(f'Signup failed: {e}')

def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    try:
        payload = {
            "returnSecureToken": return_secure_token
        }
        if email:
            payload["email"] = email
        if password:
            payload["password"] = password
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": "AIzaSyALebezYE7_X1heM1sypIeAJmWI8QyModQ"}, data=payload)
        try:
            data = r.json()
            user_info = {
                'email': data['email'],
                'username': data.get('displayName')  # Retrieve username if available
            }
            return user_info
        except:
            st.warning(data)
    except Exception as e:
        st.warning(f'Signin failed: {e}')

def reset_password(email):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
        payload = {
            "email": email,
            "requestType": "PASSWORD_RESET"
        }
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": "AIzaSyALebezYE7_X1heM1sypIeAJmWI8QyModQ"}, data=payload)
        if r.status_code == 200:
            return True, "Reset email Sent"
        else:
            # Handle error response
            error_message = r.json().get('error', {}).get('message')
            return False, error_message
    except Exception as e:
        return False, str(e)

def authentication_page():
    st.title('Welcome to :violet[Craftify] :sunglasses:')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f():
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']
            st.session_state.signedout = False
        except:
            st.warning('Login Failed')

    def forget():
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            success, message = reset_password(email)
            if success:
                st.success("Password reset email sent successfully.")
            else:
                st.warning(f"Password reset failed: {message}")

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
            st.button('Login', on_click=f)
            forget()

    else:
        st.text('Name: ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        if st.button('Sign out'):
            st.session_state.signedout = True
            st.session_state.username = ''
            st.session_state.useremail = ''
            st.experimental_rerun()

        # Add a new button to go to the main app
        if st.button('Go to the App →'):
            st.session_state['page'] = 'main_app'
            st.experimental_rerun()



def main_page():
    st.set_page_config(layout="wide")

    # Hide the Streamlit menu and footer
    hide_menu = """
        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        </style>
        """
    st.markdown(hide_menu, unsafe_allow_html=True)

    # Sidebar with Sign Up and Sign Out buttons
    with st.sidebar:
        st.image("assets/logo/Colorlogo.png")

        # Determine which button to show based on session state
        if 'username' in st.session_state and st.session_state['username']:
            if st.button("Log Out || mainpage"):
                st.session_state['page'] = 'authentication'
                st.experimental_rerun()
        else:
            if st.button("main page"):
                st.session_state['page'] = 'authentication'
                st.experimental_rerun()

    # Main content display
    if 'page' in st.session_state:
        if st.session_state['page'] == 'authentication':
            authentication_page()  # Render the authentication page
        elif st.session_state['page'] == 'main_app':
            import streamlit_app  # Dynamically load the main app
            streamlit_app.main()
        else:
            st.write("Welcome to Craftify... Unleash the Power Within: Where Every Choice Shapes Your Fate")
            st.image("assets/logo/karn.jpg", use_column_width='auto')
    else:
        # Display the main page content if no specific page is set
        st.write("Welcome to Craftify... Unleash the Power Within: Where Every Choice Shapes Your Fate")
        st.image("assets/logo/karn.jpg", use_column_width='auto')

if __name__ == "__main__":
    main_page()


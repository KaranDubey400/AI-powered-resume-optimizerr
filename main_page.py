import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json

# ✅ Set the page configuration at the very top
st.set_page_config(layout="wide")

def sign_in_with_email_and_password(email, password):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
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
        return False, data['error']['message']
    return True, None

def authentication_page():
    st.title('Login / Signup')

    if 'signedout' not in st.session_state:
        st.session_state['signedout'] = True

    if st.session_state['signedout']:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            if st.button('Create my account'):
                success, error = sign_up_with_email_and_password(email, password, username)
                if success:
                    st.success('Account created successfully! Please login.')
                else:
                    st.error(f'Sign up failed: {error}')
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
        st.text(f'Name: {st.session_state.get("username", "")}')
        st.text(f'Email: {st.session_state.get("useremail", "")}')
        if st.button('Sign out'):
            st.session_state.clear()
            st.session_state['signedout'] = True

def main_page():
    # Infinite rerun se bachne ke liye ek session flag use karo
    if 'redirected_to_auth' not in st.session_state:
        st.session_state['redirected_to_auth'] = False

    if ('username' not in st.session_state or not st.session_state['username']):
        if st.query_params.get("page", [None])[0] != "authentication" and not st.session_state['redirected_to_auth']:
            st.query_params = {"page": "authentication"}
            st.session_state['redirected_to_auth'] = True
            return
    else:
        st.session_state['redirected_to_auth'] = False

    with st.sidebar:
        st.image("assets/logo/Colorlogo.png")
        if 'username' in st.session_state and st.session_state['username']:
            if st.button("Log Out"):
                st.session_state.clear()
                st.query_params = {"page": "authentication"}
                return
        else:
            if st.button("Login / Signup"):
                st.query_params = {"page": "authentication"}
                return

    query_params = st.query_params
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

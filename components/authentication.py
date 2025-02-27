import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

def load_auth_config():
    config_path = "config/auth_config.yaml"
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            yaml.dump({'credentials': {'usernames': {}}, 
                      'cookie': {'expiry_days': 30, 
                               'key': 'trading_cards_signature_key', 
                               'name': 'trading_cards_auth_cookie'}}, f)

    with open(config_path) as f:
        return yaml.load(f, Loader=SafeLoader)

def save_auth_config(config):
    with open("config/auth_config.yaml", 'w') as f:
        yaml.dump(config, f)

def setup_authentication():
    config = load_auth_config()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    # Initialize session state
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = None
    if 'username' not in st.session_state:
        st.session_state.username = None

    return authenticator, config

def show_auth_ui():
    authenticator, config = setup_authentication()

    # Add login/signup tabs
    auth_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with auth_tab:
        name, authentication_status, username = authenticator.login(
            'Login',
            location='main'
        )

        if authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status == None:
            st.warning('Please enter your username and password')

    with signup_tab:
        if st.session_state.authentication_status != True:
            st.subheader("Create New Account")
            with st.form("signup_form"):
                new_username = st.text_input("Username")
                new_name = st.text_input("Full Name")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")

                if st.form_submit_button("Sign Up"):
                    if new_password != confirm_password:
                        st.error("Passwords do not match!")
                    elif new_username in config['credentials']['usernames']:
                        st.error("Username already exists!")
                    else:
                        # Hash the password and save user
                        hashed_password = stauth.Hasher([new_password]).generate()[0]
                        config['credentials']['usernames'][new_username] = {
                            'name': new_name,
                            'password': hashed_password
                        }
                        save_auth_config(config)
                        st.success("Account created successfully! Please log in.")
                        st.experimental_rerun()

    return authentication_status, username
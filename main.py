import streamlit_authenticator as stauth
import streamlit as st

# https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/
# https://blog.streamlit.io/streamlit-authenticator-part-2-adding-advanced-features-to-your-authentication-component/

authpath = './auth.yaml'

import yaml
from yaml.loader import SafeLoader

def setup():
    with open(authpath) as file:
        config = yaml.load(file, Loader=SafeLoader)


    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    return config, authenticator

def updateConfig():
    with open(authpath, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


config, authenticator = setup()

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    try:
        if authenticator.reset_password(st.session_state["username"], 'Reset password'):
            updateConfig()
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*: username is {username}')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

import streamlit_authenticator as stauth
import streamlit as st
# hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

# print(hashed_passwords)

authpath = './auth.yaml'

import yaml
from yaml.loader import SafeLoader
with open(authpath) as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

def updateConfig():
    with open(authpath, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    try:
        result = authenticator.reset_password(st.session_state["username"], 'Reset password')
        st.write(result)
        st.success('Password modified successfully')
        st.write(st.session_state)
    except Exception as e:
        st.error(e)
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*: username is {username}')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
    try:
        newUser = authenticator.register_user('Register user', preauthorization=False)
        updateConfig()
        st.write(newUser)
    except Exception as e:
        st.error(e)
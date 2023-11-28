import os
os.system('pip install streamlit -q')
os.system('pip install streamlit-authenticator -q')
os.system('pip install plotly -q')
os.system('pip install plotly.express -q')
os.system('pip install plotly -q')
os.system('pip install pandas -q')
os.system('pip install numpy -q')
os.system('pip install sqlalchemy -q')
os.system('pip install pyyaml -q')

import streamlit as st
import streamlit.components.v1 as comp
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from dashboard import Dashboard

# st.set_page_config(    
#     page_title="Fifa Stats - Login",
#     page_icon="🧊",
#     layout="wide"
# )

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    # print(config)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login('Login', 'main')
if st.session_state["authentication_status"]:
    # authenticator.
    st.sidebar.write(f'Bem-Vindo *{st.session_state["name"]}*',True)
    st.sidebar.divider()
    Dashboard()
    
    authenticator.logout('Logout', 'main', key='unique_key')
    st.sidebar.button("Rerun")

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
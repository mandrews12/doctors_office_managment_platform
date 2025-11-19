import streamlit as st

from routes.styles import load_styles

def render():
    
    load_styles()
    
    st.title("Patient Page")
    
    st.divider()


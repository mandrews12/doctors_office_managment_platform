import streamlit as st

from utils.styles import load_styles

def render():
    
    load_styles()
    
    st.title("Doctor — Schedule & Appointments")
    
    st.divider()
    
render()

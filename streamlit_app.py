import streamlit as st
from pages import home, doctor, patient, staff


st.set_page_config(page_title="Doctors Office Dashboard", layout="wide")
    
pg = st.navigation([
    st.Page("pages/home.py", title="Home"),
    st.Page("pages/doctor.py", title="Doctor"),
    st.Page("pages/patient.py", title="Patient"),
    st.Page("pages/staff.py", title="Staff"),
])
pg.run()

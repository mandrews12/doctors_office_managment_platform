import streamlit as st
from utils.db import execute_query


def render():
    st.title("Home — Welcome to the Doctor's Office Management Platform")


    # Perform query to get total number of patients.
    df = execute_query('SELECT count(*) from patient;')
    
    # Peform query to get total number of doctors.
    df2 = execute_query('SELECT count(*) from doctor;')
    
    # Perform query to get all the specializations
    df3 = execute_query('SELECT DISTINCT role from doctor;')

    # Print results.
    for row in df.itertuples():
        st.write(f"Total patients in database: {row[1]}")
        
    for row in df2.itertuples():
        st.write(f"Total doctors in database: {row[1]}")
    
    st.write("Doctor Specializations:")
    for row in df3.itertuples():
        st.write(f"- {row[1]}")
        
        
    
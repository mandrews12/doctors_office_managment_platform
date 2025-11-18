import streamlit as st
from app_pages import home, doctor, patient, staff

def main():
    st.set_page_config(page_title="Doctors Office Dashboard", layout="wide")

    home_tab, doctor_tab, patient_tab, staff_tab = st.tabs(["Home", "Doctor", "Patient", "Staff"])

    with home_tab:
        home.render()
    with doctor_tab:
        doctor.render()
    with patient_tab:
        patient.render()
    with staff_tab:
        staff.render()


if __name__ == "__main__":
    main()

import streamlit as st
from streamlit_pages import home, doctor, patient, staff


def main():
    st.set_page_config(page_title="Doctors Office Dashboard", layout="wide")

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Home", "Doctor", "Patient", "Staff"])

    if page == "Home":
        home.render()
    elif page == "Doctor":
        doctor.render()
    elif page == "Patient":
        patient.render()
    elif page == "Staff":
        staff.render()


if __name__ == "__main__":
    main()

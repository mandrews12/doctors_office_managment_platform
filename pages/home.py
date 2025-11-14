import streamlit as st

from utils.styles import load_styles

from crud.home import get_patient_count
from crud.home import get_doctor_count
from crud.home import get_staff_count
from crud.home import get_specializations
from crud.home import get_appointments

def render():
    load_styles()

    st.title("Welcome to the Doctor's Office Management Platform")
    
    st.divider()

    patients, doctors, staff,roles, appts = get_data()

    # Display number of patients, doctors, and staff as metric cards
    st.subheader("We manage")
    
    c1, c2, c3 = st.columns([1, 1, 1], gap="large")
    with c1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">Total patients</div>
                <div class="stat-value">{patients}</div>
                <div class="stat-sub">All registered patients in the system</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">Total doctors</div>
                <div class="stat-value">{doctors}</div>
                <div class="stat-sub">Active medical staff</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with c3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">Total staff</div>
                <div class="stat-value">{staff}</div>
                <div class="stat-sub">Active clinic personnel</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.divider()
    
    st.subheader("Specializations Offered")
    
    # Show all specializations
    spec_html = '<div class="spec-grid">'
    for r in roles:
        icon = "🩺"
        spec_html += f"<div class='spec-card'><div style='display:flex;align-items:center'><div class='spec-icon'>{icon}</div><div class='spec-name'>{r}</div></div></div>"
    spec_html += '</div>'
    st.markdown(spec_html, unsafe_allow_html=True)

    st.divider()
    
    # Two-column area: main content on the left, contact card on the right
    main_col, side_col = st.columns([3, 1], gap="large")

    # Left: appointments table
    with main_col:
        st.subheader("Upcoming Appointments")
        st.table(appts)
        
    # Right: contact card
    with side_col:
        st.markdown(
            """
            <div class="stat-card" style="padding:18px;">
                <div class="stat-title">Clinic Contact Info:</div>
                <div style="margin-top:6px; font-weight:700; font-size:16px;">The Doctor's Office</div>
                <div class="stat-sub" style="margin-top:6px;">123 Elm Street, Suite 100<br/>Kingston RI, 02881</div>
                <div class="stat-sub" style="margin-top:8px;">Phone: <a href="tel:+1234567890">+1 (555) 123-4567</a></div>
                <div class="stat-sub">Email: <a href="mailto:info@sunrisefamilyclinic.example">info@familyclinic.example</a></div>
                <div class="stat-sub" style="margin-top:8px;">Hours: Mon–Fri 8:00am – 5:00pm</div>
                <div class="stat-sub" style="margin-top:10px; font-size:12px; color:#6b7280;">For appointments, please visit the Appointments page or call the clinic.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        
def get_data():
    # Perform query to get total number of patients.
    patientDF = get_patient_count()
    
    # Peform query to get total number of doctors.
    doctorDF = get_doctor_count()
    
    # Perform query to get all the specializations
    rolesDF = get_specializations()
    
    # Query to get all staff
    staffDF = get_staff_count()
    
    # Perform query to get next 5 appointments for today
    apptsDF = get_appointments()

    patients = None
    for row in patientDF.itertuples():
        patients = row[1]

    doctors = None
    for row in doctorDF.itertuples():
        doctors = row[1]

    staff = None
    for row in staffDF.itertuples():
        staff = row[1]

    # Build roles list
    roles = []
    for row in rolesDF.itertuples():
        roles.append(row[1])
        
    # Build appointments list
    appts = []
    for row in apptsDF.itertuples():
        appts.append({
            "Time": row[1],
            "Patient": row[2],
            "Doctor": row[3],
            "Status": row[4]
        })
        
    return patients, doctors, staff, roles, appts

render()

    

 
        
    
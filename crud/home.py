#File for database operations related to the home page

import streamlit as st
from utils.db import execute_query

def get_patient_count():
    patients = execute_query('SELECT count(*) from patient;')
    return patients

def get_doctor_count():
    doctors = execute_query('SELECT count(*) from doctor;')
    return doctors

def get_staff_count():
    staff = execute_query('SELECT count(*) from staff;')
    return staff

def get_specializations():
    roles = execute_query('SELECT DISTINCT role from doctor;')
    return roles

def get_appointments():
    appts = execute_query('SELECT appointment_date, patient_last_name, doctor_last_name, status FROM doctor_schedule ORDER BY appointment_date ASC LIMIT 5;')
    return appts
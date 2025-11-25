#File for database operations related to the home page
from routes.db import execute_query

def get_patient_count():
    query = """
    SELECT count(*) as patient_count
    FROM patient;
    """
    patients = execute_query(query)
    return patients

def get_doctor_count():
    query = """
    SELECT count(*) as doctor_count
    FROM doctor;
    """
    doctors = execute_query(query)
    return doctors

def get_staff_count():
    query = """
    SELECT count(*) as staff_count
    FROM staff;
    """
    staff = execute_query(query)
    return staff

def get_specializations():
    query = """
    SELECT DISTINCT role
    FROM doctor;
    """
    roles = execute_query(query)
    return roles

def get_appointments():
    query = """
    SELECT appointment_date, patient_last_name, doctor_last_name, status
    FROM doctor_schedule
    ORDER BY appointment_date ASC
    LIMIT 5;
    """
    appts = execute_query(query)
    return appts
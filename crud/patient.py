#File for database operations related to the home page
from routes.db import execute_query

def get_patient_names():
    patients = execute_query('SELECT first_name, last_name from patient;')
    return patients

def get_patient_info(patient_fname, patient_lname):
    patient_info = execute_query('SELECT * FROM')
#File for database operations related to the home page

import streamlit as st
from utils.db import get_connection

def get_patients(get_connection):
    """Fetch all patients from the database."""
    conn = get_connection()
    query = "SELECT * FROM patients"
    cursor = conn.cursor()
    cursor.execute(query)
    patients = cursor.fetchall()
    cursor.close()
    return patients
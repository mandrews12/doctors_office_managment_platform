#File for database operations related to the home page
from routes.db import get_new_connection
from datetime import datetime as _datetime
from mysql.connector import Error

def get_patient_names():
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT fname, lname FROM patient;")
            rows = cursor.fetchall()
            
            # turn rows into a dataframe-like list of dicts
            patients = [dict(row) for row in rows]
            return patients
        except Error as e:
            print(f"Error fetching patient names: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return []

def get_updatable_patient_info(patient_fname, patient_lname):
    conn = get_new_connection()
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT email, allergies, medications, phone_number, address
            FROM patient
            WHERE fname = %s AND lname = %s;
            """
            cursor.execute(query, (patient_fname, patient_lname))
            rows = cursor.fetchall()
            
            # turn rows into a dataframe-like list of dicts
            patient_info = [dict(row) for row in rows]
            return patient_info
        except Error as e:
            print(f"Error fetching patient info: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return []

def update_patient_info(patient_fname, patient_lname, email, allergies, medications, phone_number, address):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            UPDATE patient
            SET email = %s,
                allergies = %s,
                medications = %s,
                phone_number = %s,
                address = %s
            WHERE fname = %s AND lname = %s;
            """
            cursor.execute(query, (email, allergies, medications, phone_number, address, patient_fname, patient_lname))
            conn.commit()
            return True, "Patient information updated successfully."
        except Error as e:
            return False, f"Error updating patient information: {e}"
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return False, "No database connection."
   
    
def get_medical_records(patient_fname, patient_lname):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            select visit_date, visit_reason, visit_notes from past_visits pv
            join patient p on pv.patient_id = p.patient_id
            where p.lname = %s AND p.fname = %s
            order by visit_id desc;
            """
            cursor.execute(query, (patient_lname, patient_fname))
            rows = cursor.fetchall()
            records = [dict(row) for row in rows]
            return records
        except Exception as e:
            print(f"Error fetching medical records: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return []

def schedule_appointment(patient_fname, patient_lname, appointment_date, appointment_time, reason):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)

            # Lookup patient id and doctor id
            cursor.execute(
                "SELECT patient_id, doc_id FROM patient WHERE fname = %s AND lname = %s",
                (patient_fname, patient_lname),
            )
            row = cursor.fetchone()
            if not row:
                return False, "Patient not found"

            p_id = row.get("patient_id")
            d_id = row.get("doc_id")

            appointment_datetime = _datetime.combine(appointment_date, appointment_time)

            query = """
            INSERT INTO appointment (patient_id, appointment_date, reason_for_visit, status, visit_notes, doctor_id)
            VALUES (%s, %s, %s, 'Scheduled', NULL, %s);
            """
            cursor.execute(query, (p_id, appointment_datetime, reason, d_id))
            conn.commit()
            return True, "Appointment scheduled"
        except Error as e:
            return False, f"Error inserting appointment: {e}"
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return False, "No database connection."

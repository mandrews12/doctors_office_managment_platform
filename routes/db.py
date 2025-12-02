
import streamlit as st
import mysql.connector
from mysql.connector import Error

# ---------- Database Connection ----------
def get_new_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["db_host"],
            user=st.secrets["db_user"],
            password=st.secrets["db_pass"],
            database=st.secrets["db_name"]
        )
        return conn
    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# will take in something like: query, (visit_reason, visit_notes, p_id, d_id, visit_date)
def post(query, params):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        except Error as e:
            st.error(f"Database operation failed: {e}")
            return False
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return False

def get(query, params=None):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Error as e:
            st.error(f"Database query failed: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return []

__all__ = ["get_new_connection", "post", "get"]

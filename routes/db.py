
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

__all__ = ["get_new_connection"]


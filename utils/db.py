

from typing import Any, Dict, Iterable, List, Optional

import streamlit as st

try:
	from mysql.connector import Error
except ImportError:
    pass

# Get a database connection using Streamlit's connection management.
def get_connection():
    conn = st.connection('mysql', type='sql')
    return conn

# Execute a query and return the results as a list of dictionaries.
def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    return conn.query(query, params=params)

__all__ = ["get_connection", "execute_query"]


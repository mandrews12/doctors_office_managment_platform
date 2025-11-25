from typing import Any, Dict, List, Optional

import streamlit as st

# Get a database connection using Streamlit's connection management.
def get_connection():
    try:
        conn = st.connection('mysql', type='sql')
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None
    
# Execute updated/insert/delete statements that will not return results.
def execute_non_query(query: str, params: Optional[Dict[str, Any]] = None) -> None:
    conn = get_connection()
    try:
        conn.query(query, params=params)
        return None
    except Exception as e:
        print(f"Non-query executed but could not produce a result object: {e}")
        return None
    
# Execute a query and return the results as a list of dictionaries.
def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    return conn.query(query, params=params)

__all__ = ["get_connection", "execute_query", "execute_non_query"]


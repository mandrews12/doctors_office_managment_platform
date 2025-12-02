# Doctors Office Management Platform

## Overview
A platform to manage a doctor's office, including scheduling, patient records, and staff management.


## Streamlit app — setup and run instructions

This project includes a minimal Streamlit app scaffold at `streamlit_app.py` and page modules under `streamlit_pages/`.

- Home: clinic metrics, office hours, quick links
- Doctor: select doctor, schedule, appointment form
- Patient: schedule, past history, update contact
- Staff: schedule appointments, order supplies, view schedules

Connecting to MySQL Database using Streamlit Secrets:

1. Create a `secrets.toml` file in the `.streamlit/` directory (create it if it doesn't exist).

2. Add your database connection info in the following format:

```toml
# .streamlit/secrets.toml
db_host = "172.20.127.4"
db_user = "XXX"
db_pass = "XXX"
db_name = "doctor_office"
```

Replacing `XXX` with your actual database username and password

Running the Streamlit App:

1. Install requirements:

```powershell
pip install -r requirements.txt
```

2. Run the Streamlit app:

```powershell
streamlit run streamlit_app.py
```

## Notes
- The app uses local placeholder data only. No database connections are made.
- `requirements.txt` already contains `streamlit`.
- To stop the app, press Ctrl+C in the terminal or use the browser UI.

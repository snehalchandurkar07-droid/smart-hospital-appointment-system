# Smart Hospital Appointment Booking System

A student PBL web application built with Python, Flask, HTML, CSS, and SQLite.

## Features
- Patient registration and login with hashed passwords
- Browse doctors and specializations
- Book an appointment on a doctor's available day and working hours
- Prevent duplicate doctor/date/time bookings
- Patient dashboard and appointment cancellation
- Admin dashboard to review bookings and update status
- Demo doctors inserted automatically on first run

## Requirements
- Python 3.10 or newer
- Internet connection is optional for the app itself; Google Fonts are used for styling when online.

## Run on Windows
1. Extract the ZIP file.
2. Open the extracted folder in VS Code.
3. Open Terminal in that folder.
4. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```
5. Activate it:
   ```bash
   venv\\Scripts\\activate
   ```
6. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
7. Run:
   ```bash
   python app.py
   ```
8. Open the local address shown in the terminal, usually `http://127.0.0.1:5000`.

## Run on macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Demo admin login
- Username: `admin`
- Password: `admin123`

The database file `hospital.db` is created automatically when the app starts. The doctor records are also added automatically.

## Important
This is an educational demo, not a production medical system. Change the Flask secret key and admin authentication before deployment. For real use, add CSRF protection, stronger admin accounts, audit logging, privacy controls, and professional security review. Do not enter real patient/medical information into a demo.

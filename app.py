from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
from datetime import date

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"
DB_PATH = "hospital.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        phone TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        available_days TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        fee INTEGER NOT NULL DEFAULT 300
    );
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        reason TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id),
        UNIQUE(doctor_id, appointment_date, appointment_time)
    );
    """)
    count = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
    if count == 0:
        doctors = [
            ("Dr. Asha Patil", "General Physician", "Mon,Tue,Wed,Thu,Fri", "09:00", "13:00", 300),
            ("Dr. Rahul Shah", "Cardiologist", "Mon,Wed,Fri", "10:00", "14:00", 600),
            ("Dr. Neha Joshi", "Dermatologist", "Tue,Thu,Sat", "11:00", "15:00", 500),
            ("Dr. Amit Kulkarni", "Pediatrician", "Mon,Tue,Thu,Sat", "09:30", "12:30", 400),
            ("Dr. Priya Deshmukh", "Orthopedic", "Wed,Thu,Fri", "14:00", "17:00", 500),
        ]
        conn.executemany("""INSERT INTO doctors
            (name, specialization, available_days, start_time, end_time, fee)
            VALUES (?, ?, ?, ?, ?, ?)""", doctors)
    conn.commit()
    conn.close()

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "patient_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Please log in as admin.", "warning")
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped

@app.route("/")
def index():
    conn = get_db()
    doctors = conn.execute("SELECT * FROM doctors ORDER BY name").fetchall()
    conn.close()
    return render_template("index.html", doctors=doctors)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        if not all([name, email, phone, password]):
            flash("Please fill in all fields.", "danger")
            return render_template("register.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html")
        conn = get_db()
        try:
            conn.execute("INSERT INTO patients(name,email,password_hash,phone) VALUES(?,?,?,?)",
                         (name, email, generate_password_hash(password), phone))
            conn.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("This email is already registered.", "danger")
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        conn = get_db()
        patient = conn.execute("SELECT * FROM patients WHERE email=?", (email,)).fetchone()
        conn.close()
        if patient and check_password_hash(patient["password_hash"], password):
            session.clear()
            session["patient_id"] = patient["id"]
            session["patient_name"] = patient["name"]
            flash("Welcome back!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    appointments = conn.execute("""
        SELECT a.*, d.name AS doctor_name, d.specialization
        FROM appointments a JOIN doctors d ON d.id=a.doctor_id
        WHERE a.patient_id=? ORDER BY a.appointment_date DESC, a.appointment_time DESC
    """, (session["patient_id"],)).fetchall()
    conn.close()
    return render_template("dashboard.html", appointments=appointments, today=date.today().isoformat())

@app.route("/book/<int:doctor_id>", methods=["GET", "POST"])
@login_required
def book(doctor_id):
    conn = get_db()
    doctor = conn.execute("SELECT * FROM doctors WHERE id=?", (doctor_id,)).fetchone()
    if not doctor:
        conn.close()
        flash("Doctor not found.", "danger")
        return redirect(url_for("index"))
    if request.method == "POST":
        appt_date = request.form.get("appointment_date", "")
        appt_time = request.form.get("appointment_time", "")
        reason = request.form.get("reason", "").strip()
        if not appt_date or not appt_time or not reason:
            flash("Please complete all appointment fields.", "danger")
        elif appt_date < date.today().isoformat():
            flash("Please select today or a future date.", "danger")
        else:
            day_name = date.fromisoformat(appt_date).strftime("%a")
            allowed_days = [x.strip()[:3] for x in doctor["available_days"].split(",")]
            if day_name not in allowed_days:
                flash("This doctor is not available on the selected day.", "danger")
            elif not (doctor["start_time"] <= appt_time < doctor["end_time"]):
                flash(f"Choose a time between {doctor['start_time']} and {doctor['end_time']}.", "danger")
            else:
                try:
                    conn.execute("""INSERT INTO appointments
                        (patient_id,doctor_id,appointment_date,appointment_time,reason,status)
                        VALUES(?,?,?,?,?,'Pending')""",
                        (session["patient_id"], doctor_id, appt_date, appt_time, reason))
                    conn.commit()
                    flash("Appointment booked successfully. Status: Pending.", "success")
                    conn.close()
                    return redirect(url_for("dashboard"))
                except sqlite3.IntegrityError:
                    flash("That time slot is already booked. Please choose another time.", "danger")
    conn.close()
    return render_template("book.html", doctor=doctor, today=date.today().isoformat())

@app.route("/cancel/<int:appointment_id>", methods=["POST"])
@login_required
def cancel(appointment_id):
    conn = get_db()
    result = conn.execute("""UPDATE appointments SET status='Cancelled'
        WHERE id=? AND patient_id=? AND status IN ('Pending','Confirmed')""",
        (appointment_id, session["patient_id"]))
    conn.commit()
    conn.close()
    flash("Appointment cancelled." if result.rowcount else "Appointment could not be cancelled.", 
          "success" if result.rowcount else "warning")
    return redirect(url_for("dashboard"))

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # Demo credentials only. Change these before any real deployment.
        if username == "admin" and password == "admin123":
            session.clear()
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Invalid admin username or password.", "danger")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Admin logged out.", "info")
    return redirect(url_for("index"))

@app.route("/admin")
@admin_required
def admin_dashboard():
    conn = get_db()
    appointments = conn.execute("""
        SELECT a.*, p.name AS patient_name, p.phone, p.email,
               d.name AS doctor_name, d.specialization
        FROM appointments a
        JOIN patients p ON p.id=a.patient_id
        JOIN doctors d ON d.id=a.doctor_id
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
    """).fetchall()
    stats = {
        "patients": conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0],
        "doctors": conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0],
        "appointments": conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0],
        "pending": conn.execute("SELECT COUNT(*) FROM appointments WHERE status='Pending'").fetchone()[0],
    }
    conn.close()
    return render_template("admin_dashboard.html", appointments=appointments, stats=stats)

@app.route("/admin/status/<int:appointment_id>", methods=["POST"])
@admin_required
def update_status(appointment_id):
    status = request.form.get("status", "")
    if status not in ("Pending", "Confirmed", "Cancelled", "Completed"):
        flash("Invalid status.", "danger")
    else:
        conn = get_db()
        conn.execute("UPDATE appointments SET status=? WHERE id=?", (status, appointment_id))
        conn.commit()
        conn.close()
        flash("Appointment status updated.", "success")
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

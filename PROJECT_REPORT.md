# Smart Hospital Appointment Booking System — PBL Report

## 1. Abstract
The Smart Hospital Appointment Booking System is a web-based application that helps patients view doctors and request appointments online. Patients can register, log in, select a doctor, choose a date and time, and track or cancel eligible appointments. The admin can view all appointment requests and update their status. The project demonstrates web development, database operations, authentication, and validation.

## 2. Introduction
In a traditional appointment process, patients may need to call or visit a hospital to check doctor availability. This can take time and may lead to confusion about available slots. The proposed system provides a simple online interface for managing appointment requests.

## 3. Problem Statement
To develop a user-friendly web application that allows patients to request hospital appointments online and allows hospital staff to manage appointment status while avoiding duplicate bookings for the same doctor, date, and time.

## 4. Objectives
- Provide patient registration and login.
- Display doctors and their specializations.
- Allow patients to book an appointment online.
- Validate date, doctor availability, and time range.
- Prevent duplicate doctor/date/time bookings.
- Allow patients to view and cancel appointments.
- Provide an admin dashboard to update appointment status.

## 5. Existing System
Appointments may be managed through phone calls, paper registers, or manual records. These methods can require additional staff effort and make it harder for patients to check appointment status.

## 6. Proposed System
The proposed web application keeps patient, doctor, and appointment data in a database. Patients use a browser to request appointments, while an admin can review requests and mark them Pending, Confirmed, Cancelled, or Completed.

## 7. Technologies Used
- Frontend: HTML and CSS
- Backend: Python with Flask
- Database: SQLite
- Development tool: Visual Studio Code
- Browser: Chrome, Edge, Firefox, or another modern browser

## 8. Main Modules
1. Patient Registration
2. Patient Login and Logout
3. Doctor Listing
4. Appointment Booking
5. Patient Dashboard
6. Appointment Cancellation
7. Admin Login
8. Admin Dashboard and Status Update

## 9. Database Design
### Patients
- id — Primary Key
- name
- email — Unique
- password_hash
- phone

### Doctors
- id — Primary Key
- name
- specialization
- available_days
- start_time
- end_time
- fee

### Appointments
- id — Primary Key
- patient_id — Foreign Key to Patients
- doctor_id — Foreign Key to Doctors
- appointment_date
- appointment_time
- reason
- status
- created_at

A unique constraint on doctor_id, appointment_date, and appointment_time prevents two appointments from being assigned to the same doctor at the same date and time.

## 10. System Flow
Patient opens website → Registers or logs in → Views doctors → Selects a doctor → Chooses date and time → System validates availability → Appointment is saved as Pending → Admin reviews and updates status → Patient checks status in dashboard.

## 11. Testing
| Test case | Expected result |
|---|---|
| Register with valid details | Account is created |
| Register with an existing email | Error message is displayed |
| Login with correct details | Patient dashboard opens |
| Login with incorrect details | Error message is displayed |
| Book a future appointment during working hours | Appointment is saved as Pending |
| Select a past date | Booking is rejected |
| Select a day the doctor is unavailable | Booking is rejected |
| Book an already occupied slot | Duplicate booking is rejected |
| Admin confirms an appointment | Status changes to Confirmed |
| Patient cancels an eligible appointment | Status changes to Cancelled |

## 12. Advantages
- Convenient appointment requests
- Centralized appointment records
- Less manual scheduling work
- Easier status tracking
- Duplicate booking prevention

## 13. Limitations
- Demo admin account is fixed and must not be used for real deployment.
- Appointment slots are represented in 30-minute increments by the form, but the system stores the submitted time.
- No SMS/email reminders or payment integration.
- This prototype is not connected to a real hospital system.

## 14. Future Scope
- Secure admin account management
- Email or SMS notifications
- Doctor-side portal
- Calendar integration
- Online payment integration
- Improved accessibility and multilingual support
- Deployment with HTTPS and production database

## 15. Conclusion
The Smart Hospital Appointment Booking System provides a simple way for patients to request appointments online and for an admin to manage their status. It demonstrates the use of frontend technologies, a Python web framework, database design, and validation in a practical project.

from app.models import db, Patient
from app.emailer import send_email
from app.config import from_address, to_address


def create_patient():
    patient = Patient(name="Alice", age=30, disease="Flu")
    db.session.add(patient)
    db.session.commit()
    send_email(to_address, "New Patient Created", f"Patient {patient.name} has been created.")
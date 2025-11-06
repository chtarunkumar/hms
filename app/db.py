from app.models import db, Patient


def create_patient():
    patient = Patient(name="Alice", age=30, disease="Flu")
    db.session.add(patient)
    db.session.commit()
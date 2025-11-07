# app/crud.py

from .models import db, Patient
from typing import List, Optional

def create_patient(name: str, age: int, disease: str) -> Patient:
    """Creates a new patient record."""
    patient = Patient(name=name, age=age, disease=disease)
    db.session.add(patient)
    db.session.commit()
    return patient

def get_patient_by_id(patient_id: int) -> Optional[Patient]:
    """Retrieves a patient by their ID."""
    return db.session.get(Patient, patient_id)

def get_all_patients() -> List[Patient]:
    """Retrieves all patient records."""
    return Patient.query.all()

def update_patient(patient_id: int, name: Optional[str] = None, age: Optional[int] = None, disease: Optional[str] = None) -> Optional[Patient]:
    """Updates an existing patient record."""
    patient = get_patient_by_id(patient_id)
    if patient:
        if name is not None:
            patient.name = name
        if age is not None:
            patient.age = age
        if disease is not None:
            patient.disease = disease
        db.session.commit()
    return patient

def delete_patient(patient_id: int) -> bool:
    """Deletes a patient record by ID."""
    patient = get_patient_by_id(patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return True
    return False

def get_patients_in_batches(batch_size: int = 10, offset: int = 0) -> List[Patient]:
    """Retrieves patients in batches for processing."""
    return Patient.query.offset(offset).limit(batch_size).all()

def get_total_patient_count() -> int:
    """Returns the total number of patients."""
    return db.session.query(Patient).count()
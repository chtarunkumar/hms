
from flask import Blueprint, current_app, request, jsonify
import app.logger as logger
from .models import db, Patient
from .emailer import send_gmail, to_address

bp = Blueprint('patients', __name__)

@bp.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([p.to_dict() for p in patients])

@bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    patient = Patient(name=data['name'], age=data['age'], disease=data['disease'])
    db.session.add(patient)
    db.session.commit()
    #recipients = current_app.config.get('MAIL_RECIPIENTS')
    #if recipients:
    subject = f"New Patient Registered: {patient.name}"
    body = (f"A new patient record has been created:\n\n"
            f"ID: {patient.id}\n"
            f"Name: {patient.name}\n"
            f"Age: {patient.age}\n"
            f"Disease: {patient.disease}")
    send_gmail(to_address, subject, body)
    print("")
    logger.info(f"Email notification sent for new patient (ID: {patient.id}).")
    #else:
    #    logger.warning("No email recipients configured. Skipping email notification for new patient.")

    return jsonify(patient.to_dict()), 201
    # except Exception as e:
    # logger.error(f"Error adding patient: {e}", exc_info=True)
    # return jsonify(patient.to_dict()), 201

@bp.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    data = request.json
    patient = db.session.get(Patient, id)
    if not patient:
        return jsonify({'error':'patient not found'}), 404
    

    patient.name = data.get('name', patient.name)
    patient.age = data.get('age', patient.age)
    patient.disease = data.get('disease', patient.disease)
    db.session.commit()
    return jsonify(patient.to_dict())

@bp.route('/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = db.session.get(Patient, id)
    if not patient:
        return jsonify({'error':'patient not found'}), 404
    

    db.session.delete(patient)
    db.session.commit()
    return '',204
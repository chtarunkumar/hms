import pytest
from app import create_app
from app.models import db, Patient

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()

def test_create_patient(client):
    resp = client.post('/patients', json={"name": "Alice", "age": 30, "disease": "Flu"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['name'] == "Alice"
    assert data['age'] == 30
    assert data['disease'] == "Flu"

def test_get_patients(client):
    client.post('/patients', json={"name": "Bob", "age": 25, "disease": "Cold"})
    resp = client.get('/patients')
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_update_patient(client):
    post = client.post('/patients', json={"name": "Charlie", "age": 22, "disease": "Cough"})
    pid = post.get_json()['id']
    resp = client.put(f'/patients/{pid}', json={"name": "Charles"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['name'] == "Charles"

def test_delete_patient(client):
    post = client.post('/patients', json={"name": "David", "age": 40, "disease": "Fever"})
    pid = post.get_json()['id']
    resp = client.delete(f'/patients/{pid}')
    assert resp.status_code == 204
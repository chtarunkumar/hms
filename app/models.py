from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    disease = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"[id={self.id}, name={self.name}, age={self.age}, disease={self.disease}]"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'disease': self.disease
        }
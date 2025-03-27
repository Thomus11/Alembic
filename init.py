from sqlalchemy import create_engine, Column ,Integer, String, ForeignKey, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    contact_info = Column(String(255), nullable=False)
    
    records = relationship('Records', back_populates='patient', cascade='all, delete-orphan')
    billing = relationship('Billing', back_populates='patient', cascade='all, delete-orphan')
    prescriptions = relationship('Pharmaceutical', back_populates='patient', cascade='all, delete-orphan')

class Staff(Base):
    __tablename__ = 'staffs'
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    department = Column(String(100), nullable=False)
    contact_info = Column(String(255), nullable=False)
    
    records = relationship('Records', back_populates='staff', cascade='all, delete-orphan')
    prescriptions = relationship('Pharmaceutical', back_populates='staff', cascade='all, delete-orphan')

class Records(Base):
    __tablename__ = 'records'
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    details = Column(Text, nullable=False)
    
    patient = relationship('Patient', back_populates='records')
    staff = relationship('Staff', back_populates='records')

class Billing(Base):
    __tablename__ = 'billings'
    bill_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    status = Column(String(50), default='Unpaid')
    services = Column(Text, nullable=False)
    
    patient = relationship('Patient', back_populates='billing')

class Pharmaceutical(Base):
    __tablename__ = 'pharmaceuticals'
    prescription_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    medications = Column(Text, nullable=False)
    dosage_instructions = Column(Text, nullable=False)
    
    patient = relationship('Patient', back_populates='prescriptions')
    staff = relationship('Staff', back_populates='prescriptions')

# Database setup
engine = create_engine('sqlite:///hospital.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Example Data
patient1 = Patient(name='John Doe', age=30, gender='Male', contact_info='123-456-7890')
staff1 = Staff(name='Dr. Smith', role='Doctor', department='Cardiology', contact_info='dr.smith@hospital.com')
record1 = Records(patient=patient1, staff=staff1, details='Patient complains of chest pain.')
billing1 = Billing(patient=patient1, amount=200.00, services='Consultation Fee, ECG Test')
prescription1 = Pharmaceutical(patient=patient1, staff=staff1, medications='Aspirin', dosage_instructions='Take one tablet daily after meals.')

# Add to session and commit
session.add_all([patient1, staff1, record1, billing1, prescription1])
session.commit()

print("Database tables created and sample data inserted successfully!")
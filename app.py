from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Doctor(db.Model):
    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(50))
    phone = db.Column(db.String(20))

class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))

class Prescription(db.Model):
    prescription_id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    medicine = db.Column(db.String(50))
    dosage = db.Column(db.String(50))
    date = db.Column(db.String(20))
    doctor = db.relationship('Doctor', backref='prescriptions')
    patient = db.relationship('Patient', backref='prescriptions')

# Home
@app.route('/')
def home():
    return render_template('home.html')

# ----- Doctors CRUD -----
@app.route('/doctors')
def doctors():
    query = request.args.get('query')
    if query:
        all_doctors = Doctor.query.filter(Doctor.name.contains(query)).all()
    else:
        all_doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=all_doctors)

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    db.session.add(Doctor(
        name=request.form['name'],
        specialization=request.form['specialization'],
        phone=request.form['phone']
    ))
    db.session.commit()
    return redirect(url_for('doctors'))

@app.route('/edit_doctor/<int:id>', methods=['GET','POST'])
def edit_doctor(id):
    doc = Doctor.query.get_or_404(id)
    if request.method == 'POST':
        doc.name = request.form['name']
        doc.specialization = request.form['specialization']
        doc.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('doctors'))
    return render_template('edit_doctor.html', doctor=doc)

@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    doc = Doctor.query.get_or_404(id)
    db.session.delete(doc)
    db.session.commit()
    return redirect(url_for('doctors'))

# ----- Patients CRUD -----
@app.route('/patients')
def patients():
    query = request.args.get('query')
    if query:
        all_patients = Patient.query.filter(Patient.name.contains(query)).all()
    else:
        all_patients = Patient.query.all()
    return render_template('patients.html', patients=all_patients)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    db.session.add(Patient(
        name=request.form['name'],
        age=request.form['age'],
        gender=request.form['gender'],
        phone=request.form['phone']
    ))
    db.session.commit()
    return redirect(url_for('patients'))

@app.route('/edit_patient/<int:id>', methods=['GET','POST'])
def edit_patient(id):
    pat = Patient.query.get_or_404(id)
    if request.method == 'POST':
        pat.name = request.form['name']
        pat.age = request.form['age']
        pat.gender = request.form['gender']
        pat.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('patients'))
    return render_template('edit_patient.html', patient=pat)

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    pat = Patient.query.get_or_404(id)
    db.session.delete(pat)
    db.session.commit()
    return redirect(url_for('patients'))

# ----- Prescriptions CRUD -----
@app.route('/prescriptions')
def prescriptions():
    query = request.args.get('query')
    if query:
        all_presc = Prescription.query.join(Doctor).join(Patient).filter(
            Doctor.name.contains(query) | Patient.name.contains(query)
        ).all()
    else:
        all_presc = Prescription.query.all()
    return render_template('prescriptions.html', prescriptions=all_presc)

@app.route('/add_prescription', methods=['POST'])
def add_prescription():
    db.session.add(Prescription(
        doctor_id=request.form['doctor_id'],
        patient_id=request.form['patient_id'],
        medicine=request.form['medicine'],
        dosage=request.form['dosage'],
        date=date.today().isoformat()
    ))
    db.session.commit()
    return redirect(url_for('prescriptions'))

@app.route('/edit_prescription/<int:id>', methods=['GET','POST'])
def edit_prescription(id):
    presc = Prescription.query.get_or_404(id)
    if request.method == 'POST':
        presc.doctor_id = request.form['doctor_id']
        presc.patient_id = request.form['patient_id']
        presc.medicine = request.form['medicine']
        presc.dosage = request.form['dosage']
        db.session.commit()
        return redirect(url_for('prescriptions'))
    return render_template('edit_prescription.html', presc=presc)

@app.route('/delete_prescription/<int:id>')
def delete_prescription(id):
    presc = Prescription.query.get_or_404(id)
    db.session.delete(presc)
    db.session.commit()
    return redirect(url_for('prescriptions'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This ensures the database tables are created correctly
    app.run(debug=True)



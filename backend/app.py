from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///byajkhata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Borrower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrower.id'), nullable=False)
    principal = db.Column(db.Float, nullable=False)  # Loan amount
    rate = db.Column(db.Float, nullable=False)       # Interest rate %
    date = db.Column(db.Date, nullable=False)        # Loan start date
    description = db.Column(db.String(200))
    borrower = db.relationship('Borrower', backref='loans')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)        # Transaction date
    amount = db.Column(db.Float, nullable=False)     # Amount paid/received
    type = db.Column(db.String(10))                   # "payment" or "repayment"
    loan = db.relationship('Loan', backref='transactions')

with app.app_context():
    db.create_all()

# Add new borrower
@app.route('/borrowers', methods=['POST'])
def add_borrower():
    data = request.json
    borrower = Borrower(
        name=data['name'],
        phone=data.get('phone'),
        email=data.get('email')
    )
    db.session.add(borrower)
    db.session.commit()
    return jsonify({'id': borrower.id, 'name': borrower.name}), 201

# Get list of borrowers
@app.route('/borrowers', methods=['GET'])
def list_borrowers():
    borrowers = Borrower.query.all()
    results = [{'id': b.id, 'name': b.name, 'phone': b.phone, 'email': b.email} for b in borrowers]
    return jsonify(results)

# Add new loan
@app.route('/loans', methods=['POST'])
def add_loan():
    data = request.json
    loan = Loan(
        borrower_id=data['borrower_id'],
        principal=float(data['principal']),
        rate=float(data['rate']),
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        description=data.get('description', '')
    )
    db.session.add(loan)
    db.session.commit()
    return jsonify({'id': loan.id}), 201

# Get list of loans
@app.route('/loans', methods=['GET'])
def list_loans():
    loans = Loan.query.all()
    results = []
    for loan in loans:
        results.append({
            'id': loan.id,
            'borrower_id': loan.borrower_id,
            'borrower_name': loan.borrower.name,
            'principal': loan.principal,
            'rate': loan.rate,
            'date': loan.date.strftime('%Y-%m-%d'),
            'description': loan.description
        })
    return jsonify(results)

# Add new transaction
@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    transaction = Transaction(
        loan_id=data['loan_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        amount=float(data['amount']),
        type=data['type']
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'id': transaction.id}), 201

# Get list of transactions
@app.route('/transactions', methods=['GET'])
def list_transactions():
    transactions = Transaction.query.all()
    results = []
    for txn in transactions:
        results.append({
            'id': txn.id,
            'loan_id': txn.loan_id,
            'date': txn.date.strftime('%Y-%m-%d'),
            'amount': txn.amount,
            'type': txn.type
        })
    return jsonify(results)

# Calculate simple interest for a loan
@app.route('/loans/<int:loan_id>/interest', methods=['GET'])
def calculate_interest(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    days = (datetime.utcnow().date() - loan.date).days
    years = days / 365
    interest = (loan.principal * loan.rate * years) / 100
    return jsonify({'interest': round(interest, 2)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

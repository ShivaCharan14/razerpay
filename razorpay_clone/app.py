from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import uuid
import random
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Needed for flash messages
db = SQLAlchemy(app)

class Payment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='INR')
    status = db.Column(db.String(20), default='created')
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    receipt = db.Column(db.String(50))

def generate_receipt():
    return f"RP{random.randint(100000, 999999)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_payment', methods=['POST'])
def create_payment():
    try:
        amount = float(request.form.get('amount'))
        description = request.form.get('description', 'No description provided')
        
        if amount <= 0:
            flash('Amount must be positive', 'error')
            return redirect(url_for('home'))
        
        payment = Payment(
            amount=amount,
            description=description,
            receipt=generate_receipt()
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return redirect(url_for('show_payment', payment_id=payment.id))
    
    except ValueError:
        flash('Invalid amount entered', 'error')
        return redirect(url_for('home'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while creating payment', 'error')
        return redirect(url_for('home'))

@app.route('/payment/<payment_id>')
def show_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return render_template('payment.html', payment=payment)

@app.route('/complete_payment/<payment_id>', methods=['POST'])
def complete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    
    if payment.status in ['success', 'failed']:
        return redirect(url_for('show_status', payment_id=payment.id))
    
    if random.random() < 0.7:
        payment.status = 'success'
        flash('Payment completed successfully!', 'success')
    else:
        payment.status = 'failed'
        flash('Payment failed. Please try again.', 'error')
    
    db.session.commit()
    
    return redirect(url_for('show_status', payment_id=payment.id))

@app.route('/status/<payment_id>')
def show_status(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return render_template('status.html', payment=payment)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
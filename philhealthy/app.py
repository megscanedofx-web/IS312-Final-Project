"""
PhilHealthy - Pharmacy Business Process Management & Innovation System
Main Flask Application
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'philhealthy-secret-key-change-in-production')
app.permanent_session_lifetime = timedelta(hours=2)

# ─── Database Configuration ─────────────────────────────────────────
# To connect with XAMPP/MySQL, install: pip install flask-mysqldb
# Then uncomment and configure:
#
# from flask_mysqldb import MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'philhealthy'
# mysql = MySQL(app)
#
# For now, we use in-memory sample data for demonstration.

# ─── Sample Data (Replace with MySQL queries) ───────────────────────
USERS = {
    'admin@philhealthy.com': {'password': 'admin123', 'role': 'admin', 'name': 'Admin User'},
    'staff@philhealthy.com': {'password': 'staff123', 'role': 'staff', 'name': 'Staff User'},
}

PRODUCTS = [
    {'id': 1, 'name': 'Paracetamol 500mg', 'category': 'Pain Relief', 'price': 5.50, 'stock': 250, 'expiry': '2026-08-15'},
    {'id': 2, 'name': 'Amoxicillin 500mg', 'category': 'Antibiotics', 'price': 12.00, 'stock': 180, 'expiry': '2025-12-01'},
    {'id': 3, 'name': 'Cetirizine 10mg', 'category': 'Allergy', 'price': 8.00, 'stock': 300, 'expiry': '2026-05-20'},
    {'id': 4, 'name': 'Losartan 50mg', 'category': 'Cardiovascular', 'price': 15.00, 'stock': 5, 'expiry': '2025-06-30'},
    {'id': 5, 'name': 'Metformin 500mg', 'category': 'Diabetes', 'price': 10.00, 'stock': 0, 'expiry': '2026-01-10'},
    {'id': 6, 'name': 'Omeprazole 20mg', 'category': 'Gastro', 'price': 9.50, 'stock': 120, 'expiry': '2025-07-15'},
    {'id': 7, 'name': 'Vitamin C 500mg', 'category': 'Vitamins', 'price': 6.00, 'stock': 400, 'expiry': '2027-03-01'},
    {'id': 8, 'name': 'Ibuprofen 200mg', 'category': 'Pain Relief', 'price': 7.00, 'stock': 15, 'expiry': '2025-09-20'},
]

DELIVERIES = [
    {'id': 1, 'supplier': 'MedSupply Co.', 'items': 'Paracetamol x500, Amoxicillin x200', 'status': 'Delivered', 'date': '2026-04-10', 'approved': True},
    {'id': 2, 'supplier': 'PharmaDist Inc.', 'items': 'Cetirizine x300, Losartan x100', 'status': 'In Transit', 'date': '2026-04-14', 'approved': True},
    {'id': 3, 'supplier': 'HealthFirst Ltd.', 'items': 'Metformin x250, Omeprazole x150', 'status': 'Pending', 'date': '2026-04-16', 'approved': False},
]

TRANSACTIONS = [
    {'id': 'TXN-001', 'customer': 'Juan Dela Cruz', 'items': 'Paracetamol x5', 'total': 27.50, 'date': '2026-04-15', 'status': 'Completed'},
    {'id': 'TXN-002', 'customer': 'Maria Santos', 'items': 'Amoxicillin x2, Vitamin C x3', 'total': 42.00, 'date': '2026-04-15', 'status': 'Completed'},
    {'id': 'TXN-003', 'customer': 'Pedro Reyes', 'items': 'Losartan x1', 'total': 15.00, 'date': '2026-04-16', 'status': 'Pending'},
]

# ─── Auth Decorators ────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('role_select'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session or session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('role_select'))
        return f(*args, **kwargs)
    return decorated

def staff_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session or session.get('role') not in ('staff', 'admin'):
            flash('Staff access required.', 'danger')
            return redirect(url_for('role_select'))
        return f(*args, **kwargs)
    return decorated

# ─── Public Routes ──────────────────────────────────────────────────
@app.route('/')
def homepage():
    return render_template('public/homepage.html')

@app.route('/about')
def about():
    return render_template('public/about.html')

@app.route('/products')
def products_page():
    return render_template('public/products.html', products=PRODUCTS)

@app.route('/contact')
def contact():
    return render_template('public/contact.html')

# ─── Auth Routes ────────────────────────────────────────────────────
@app.route('/login')
def role_select():
    return render_template('auth/role_select.html')

@app.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = USERS.get(email)
        if user and user['password'] == password and user['role'] == 'admin':
            session.permanent = True
            session['user'] = email
            session['role'] = 'admin'
            session['name'] = user['name']
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials or not an admin account.', 'danger')
    return render_template('auth/admin_login.html')

@app.route('/login/staff', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = USERS.get(email)
        if user and user['password'] == password and user['role'] == 'staff':
            session.permanent = True
            session['user'] = email
            session['role'] = 'staff'
            session['name'] = user['name']
            flash('Welcome back!', 'success')
            return redirect(url_for('staff_dashboard'))
        flash('Invalid credentials or not a staff account.', 'danger')
    return render_template('auth/staff_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'staff')
        if email in USERS:
            flash('Email already registered.', 'danger')
        else:
            USERS[email] = {'password': password, 'role': role, 'name': name}
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('role_select'))
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('homepage'))

# ─── Staff Routes ───────────────────────────────────────────────────
@app.route('/staff/dashboard')
@staff_required
def staff_dashboard():
    stats = {
        'total_products': len(PRODUCTS),
        'low_stock': sum(1 for p in PRODUCTS if 0 < p['stock'] <= 20),
        'out_of_stock': sum(1 for p in PRODUCTS if p['stock'] == 0),
        'total_sales': sum(t['total'] for t in TRANSACTIONS),
        'pending_deliveries': sum(1 for d in DELIVERIES if d['status'] == 'Pending'),
        'transactions_today': len(TRANSACTIONS),
    }
    return render_template('staff/dashboard.html', stats=stats, products=PRODUCTS[:5], transactions=TRANSACTIONS[:5])

@app.route('/staff/inventory')
@staff_required
def inventory():
    return render_template('staff/inventory.html', products=PRODUCTS)

@app.route('/staff/deliveries')
@staff_required
def deliveries():
    return render_template('staff/deliveries.html', deliveries=DELIVERIES)

@app.route('/staff/sales')
@staff_required
def sales():
    return render_template('staff/sales.html', transactions=TRANSACTIONS, products=PRODUCTS)

@app.route('/staff/transactions')
@staff_required
def transactions():
    return render_template('staff/transactions.html', transactions=TRANSACTIONS)

@app.route('/staff/reports')
@staff_required
def reports():
    stats = {
        'total_revenue': sum(t['total'] for t in TRANSACTIONS),
        'total_transactions': len(TRANSACTIONS),
        'total_products': len(PRODUCTS),
        'low_stock_items': sum(1 for p in PRODUCTS if 0 < p['stock'] <= 20),
    }
    return render_template('staff/reports.html', stats=stats, products=PRODUCTS)

# ─── Admin Routes ───────────────────────────────────────────────────
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    stats = {
        'total_users': len(USERS),
        'total_products': len(PRODUCTS),
        'low_stock': sum(1 for p in PRODUCTS if 0 < p['stock'] <= 20),
        'out_of_stock': sum(1 for p in PRODUCTS if p['stock'] == 0),
        'total_sales': sum(t['total'] for t in TRANSACTIONS),
        'pending_deliveries': sum(1 for d in DELIVERIES if d['status'] == 'Pending'),
        'transactions_today': len(TRANSACTIONS),
        'pending_approvals': sum(1 for d in DELIVERIES if not d['approved']),
    }
    return render_template('admin/dashboard.html', stats=stats, products=PRODUCTS, transactions=TRANSACTIONS, deliveries=DELIVERIES, users=USERS)

@app.route('/admin/users')
@admin_required
def admin_users():
    return render_template('admin/users.html', users=USERS)

@app.route('/admin/inventory')
@admin_required
def admin_inventory():
    return render_template('staff/inventory.html', products=PRODUCTS)

@app.route('/admin/deliveries')
@admin_required
def admin_deliveries():
    return render_template('admin/deliveries.html', deliveries=DELIVERIES)

@app.route('/admin/sales')
@admin_required
def admin_sales():
    return render_template('staff/sales.html', transactions=TRANSACTIONS, products=PRODUCTS)

@app.route('/admin/transactions')
@admin_required
def admin_transactions():
    return render_template('staff/transactions.html', transactions=TRANSACTIONS)

@app.route('/admin/reports')
@admin_required
def admin_reports():
    stats = {
        'total_revenue': sum(t['total'] for t in TRANSACTIONS),
        'total_transactions': len(TRANSACTIONS),
        'total_products': len(PRODUCTS),
        'low_stock_items': sum(1 for p in PRODUCTS if 0 < p['stock'] <= 20),
    }
    return render_template('staff/reports.html', stats=stats, products=PRODUCTS)

# ─── API Routes (for CRUD & Chatbot) ────────────────────────────────
@app.route('/api/products', methods=['GET', 'POST'])
@staff_required
def api_products():
    if request.method == 'POST':
        data = request.get_json()
        new_id = max(p['id'] for p in PRODUCTS) + 1 if PRODUCTS else 1
        product = {
            'id': new_id,
            'name': data['name'],
            'category': data['category'],
            'price': float(data['price']),
            'stock': int(data['stock']),
            'expiry': data['expiry'],
        }
        PRODUCTS.append(product)
        return jsonify({'success': True, 'product': product})
    return jsonify(PRODUCTS)

@app.route('/api/products/<int:pid>', methods=['PUT', 'DELETE'])
@staff_required
def api_product(pid):
    product = next((p for p in PRODUCTS if p['id'] == pid), None)
    if not product:
        return jsonify({'error': 'Not found'}), 404
    if request.method == 'PUT':
        data = request.get_json()
        product.update({k: v for k, v in data.items() if k != 'id'})
        if 'price' in data: product['price'] = float(data['price'])
        if 'stock' in data: product['stock'] = int(data['stock'])
        return jsonify({'success': True, 'product': product})
    if request.method == 'DELETE':
        PRODUCTS.remove(product)
        return jsonify({'success': True})

@app.route('/api/deliveries/<int:did>/approve', methods=['POST'])
@admin_required
def approve_delivery(did):
    delivery = next((d for d in DELIVERIES if d['id'] == did), None)
    if delivery:
        delivery['approved'] = True
        delivery['status'] = 'Approved'
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Simple rule-based chatbot. Replace with OpenAI/GPT integration for AI."""
    message = request.get_json().get('message', '').lower().strip()

    # Knowledge base responses
    responses = {
        'hello': 'Hello! Welcome to PhilHealthy. How can I help you today?',
        'hi': 'Hi there! I\'m the PhilHealthy assistant. Ask me about our products, hours, or services.',
        'hours': 'PhilHealthy is open Monday–Saturday, 8:00 AM to 9:00 PM, and Sundays 9:00 AM to 6:00 PM.',
        'open': 'We\'re open Mon–Sat 8AM–9PM and Sun 9AM–6PM.',
        'location': 'PhilHealthy is located at 123 Health Avenue, Wellness City, Philippines.',
        'address': 'Our address is 123 Health Avenue, Wellness City, Philippines.',
        'delivery': 'Yes! We offer same-day delivery for orders placed before 2 PM within the city.',
        'prescription': 'For prescription medicines, please bring a valid doctor\'s prescription. You can also upload it through our system.',
        'payment': 'We accept cash, credit/debit cards, GCash, and Maya.',
        'return': 'Returns are accepted within 7 days for unopened items with the original receipt.',
        'price': 'You can browse our full product catalog on the Products page. Prices vary by medicine and brand.',
        'product': 'We carry a wide range of medicines including pain relief, antibiotics, vitamins, and more. Visit our Products page!',
        'medicine': 'We have pain relief, antibiotics, allergy medicines, cardiovascular drugs, diabetes medications, vitamins, and more.',
        'discount': 'Senior citizens and PWDs get a 20% discount. We also have regular promos — check our announcements!',
        'senior': 'Senior citizens enjoy a 20% discount on all medicines. Please present a valid senior citizen ID.',
        'contact': 'You can reach us at (02) 8123-4567 or email support@philhealthy.com.',
        'phone': 'Call us at (02) 8123-4567.',
        'email': 'Email us at support@philhealthy.com.',
        'thank': 'You\'re welcome! Is there anything else I can help you with?',
        'thanks': 'You\'re welcome! Feel free to ask if you need anything else.',
        'bye': 'Goodbye! Stay healthy and take care! 💊',
        'help': 'I can help with: product info, store hours, location, delivery, prescriptions, payments, returns, and discounts. Just ask!',
    }

    # Check for keyword matches
    for keyword, response in responses.items():
        if keyword in message:
            return jsonify({'reply': response})

    # Default response
    return jsonify({
        'reply': 'I\'m not sure about that. You can ask me about our products, store hours, delivery, payments, prescriptions, or discounts. Or contact us at (02) 8123-4567 for more help!'
    })

# ─── Error Handlers ─────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template('public/homepage.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)

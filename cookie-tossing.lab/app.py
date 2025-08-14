from flask import Flask, render_template, request, redirect, url_for, make_response, session
import os
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# Simple user storage (in a real app, this would be a database)
users = {
    'admin': {'password': 'password', 'cookie': None, 'credit_card': None}
}

def validate_domain():
    host = request.host.split(':')[0]  # Remove port number
    if host != 'cookie-tossing.lab':
        return False
    return True

@app.route('/')
def login():
    if not validate_domain():
        return "Access Denied", 403
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not validate_domain():
        return "Access Denied", 403
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users:
            return "Username already exists", 400
            
        users[username] = {'password': password, 'cookie': None, 'credit_card': None}
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def process_login():
    if not validate_domain():
        return "Access Denied", 403
        
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in users and users[username]['password'] == password:
        # Generate unique cookie value
        unique_cookie = str(uuid.uuid4())
        users[username]['cookie'] = unique_cookie
        
        response = make_response(redirect(url_for('home')))
        response.set_cookie('session', unique_cookie, domain='cookie-tossing.lab', secure=False, httponly=False)
        return response
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if not validate_domain():
        return "Access Denied", 403
        
    # Clear the cookie
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('session', domain='cookie-tossing.lab')
    return response

@app.route('/home')
def home():
    if not validate_domain():
        return "Access Denied", 403
        
    session_cookie = request.cookies.get('session')
    if not session_cookie:
        return redirect(url_for('login'))
        
    # Find user by cookie
    current_user = None
    for username, data in users.items():
        if data['cookie'] == session_cookie:
            current_user = username
            break
            
    if not current_user:
        return redirect(url_for('login'))
        
    return render_template('home.html', username=current_user)

@app.route('/credit-card')
def credit_card():
    if not validate_domain():
        return "Access Denied", 403
        
    session_cookie = request.cookies.get('session')
    if not session_cookie:
        return redirect(url_for('login'))
        
    # Find user by cookie
    current_user = None
    for username, data in users.items():
        if data['cookie'] == session_cookie:
            current_user = username
            break
            
    if not current_user:
        return redirect(url_for('login'))
        
    # Get the user's credit card data
    credit_card_data = users[current_user]['credit_card']
    return render_template('credit_card.html', username=current_user, credit_card=credit_card_data)

@app.route('/update-card', methods=['POST'])
def update_card():
    if not validate_domain():
        return "Access Denied", 403
        
    session_cookie = request.cookies.get('session')
    if not session_cookie:
        return redirect(url_for('login'))
        
    # Find user by cookie - using the first cookie found (making it vulnerable to cookie tossing)
    current_user = None
    for username, data in users.items():
        if data['cookie'] == session_cookie:
            current_user = username
            break
            
    if not current_user:
        return redirect(url_for('login'))
    
    # Store the credit card data
    credit_card_data = {
        'number': request.form.get('card_number'),
        'name': request.form.get('card_name'),
        'expiry': request.form.get('card_expiry'),
        'cvv': request.form.get('card_cvv')
    }
    users[current_user]['credit_card'] = credit_card_data
    
    return redirect(url_for('credit_card'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
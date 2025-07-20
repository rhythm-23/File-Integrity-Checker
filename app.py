import os
import hashlib
import json
import random
from flask import Flask, render_template, request, redirect, session, url_for, flash
from email_utils import send_otp, mail
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Used for session management

# Mail configuration for OTP emails
app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
)
mail.init_app(app)

# Folder to store uploaded files for integrity checks
UPLOAD_FOLDER = 'monitored_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load user data from users.json
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

# Save updated user data back to users.json
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Load existing users into memory
users = load_users()

# Redirect to login by default
@app.route('/')
def home():
    return redirect('/login')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    global users
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        users[email] = {'password': password, 'otp': None}
        save_users(users)
        flash("Registered. Now log in.")
        return redirect('/login')
    return render_template('register.html')

# Login route with OTP generation
@app.route('/login', methods=['GET', 'POST'])
def login():
    global users
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        if users.get(email) and users[email]['password'] == password:
            otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
            users[email]['otp'] = otp
            save_users(users)
            send_otp(email, otp)  # Send OTP via email
            session['pending_user'] = email
            flash("OTP sent to your email.")
            return redirect('/verify')
        flash("Invalid login.")
    return render_template('login.html')

# OTP verification route
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    global users
    if request.method == 'POST':
        user = session.get('pending_user')
        entered = request.form['otp']
        if user and users.get(user) and users[user]['otp'] == entered:
            session['user'] = user
            users[user]['otp'] = None  # Clear OTP after successful login
            save_users(users)
            return redirect('/dashboard')
        flash("Invalid OTP.")
    return render_template('verify.html')

# Dashboard after successful login
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['user'])

# Upload and check file integrity
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        file = request.files['file']
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Calculate hash of the uploaded file
        hash_value = get_hash(filepath)
        db = load_hash_db()

        # Compare with previously saved hash
        status = 'New File'
        if file.filename in db:
            if db[file.filename] != hash_value:
                status = 'Modified'
            else:
                status = 'Unchanged'

        # Save/Update the hash in database
        db[file.filename] = hash_value
        save_hash_db(db)
        return render_template('result.html', filename=file.filename, status=status, hash=hash_value)
    return render_template('upload.html')

# Calculate SHA-256 hash of a file
def get_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

# Load existing hash database
def load_hash_db():
    if os.path.exists('hash_db.json'):
        with open('hash_db.json') as f:
            return json.load(f)
    return {}

# Save updated hash database
def save_hash_db(data):
    with open('hash_db.json', 'w') as f:
        json.dump(data, f, indent=4)

# Logout and clear session
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_session import Session
from database import get_db_connection, init_db
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'SUPER_SECRET_ENCRYPTED_KEY_123456789') # In production, use env var
app.config['SESSION_TYPE'] = 'filesystem'  # Fix: SESSION_TYPE was never set, which crashed Flask-Session on startup
# Fix: Flask-Session's filesystem backend defaults to a *relative* folder
# ('./flask_session'), which fails under WSGI hosts (PermissionError) since
# the working directory isn't guaranteed to be this project folder. Point
# it at an absolute path next to this file instead.
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
bcrypt = Bcrypt(app)
Session(app)

# Fix: use an absolute path for uploads too, for the same reason as the
# database path below - under WSGI the working directory isn't guaranteed
# to be this project folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB limit
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Fix: folder never existed, would crash on file upload

# Allow the frontend (opened as a file or hosted elsewhere) to call this API
try:
    from flask_cors import CORS
    CORS(app)
except ImportError:
    pass

# INITIAL CONFIG - This is for the first setup
DEFAULT_ADMIN_ID = 'admin'
DEFAULT_PASS_KEY = 'FaraSecure2026!' # The user's pass-key word

# Helper to ensure admin exists
def ensure_admin():
    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM admin_config WHERE admin_id = ?', (DEFAULT_ADMIN_ID,)).fetchone()
    if not admin:
        hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        conn.execute('INSERT INTO admin_config (admin_id, password_hash, pass_key, is_first_login) VALUES (?, ?, ?, ?)', 
                     (DEFAULT_ADMIN_ID, hashed_pw, DEFAULT_PASS_KEY, 1))
        conn.commit()
    conn.close()

# Fix: init_db() used to only run inside `if __name__ == '__main__':`, which
# never executes when the app is loaded by a WSGI server (PythonAnywhere,
# Render, Gunicorn, etc.) importing this file as a module. That's why
# ensure_admin() below was hitting "no such table: admin_config" - the
# tables were never created in that environment. Call it unconditionally
# at import time so it always runs, regardless of how the app is started.
init_db()

_startup_done = False

@app.before_request
def startup():
    # Fix: before_first_request was removed in Flask 2.3+, so this never ran
    # and the default admin account was never created in the database.
    global _startup_done
    if not _startup_done:
        ensure_admin()
        _startup_done = True

# --- PUBLIC API ---

@app.route('/api/visit', methods=['POST'])
def track_visit():
    data = request.json
    page = data.get('page', 'unknown')
    conn = get_db_connection()
    conn.execute('INSERT INTO visits (page) VALUES (?)', (page,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"}), 200

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    name = request.form.get('fullname')
    phone = request.form.get('phone')
    message = request.form.get('project_details')
    file = request.files.get('attachment')
    
    attachment_path = None
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}")
        file.save(attachment_path)

    conn = get_db_connection()
    conn.execute('INSERT INTO submissions (name, phone, message, attachment_path) VALUES (?, ?, ?, ?)', 
                 (name, phone, message, attachment_path))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Message sent successfully"}), 200

# --- ADMIN PANEL ---

@app.route('/admin-portal-secure-access')
def admin_login_page():
    return render_template('login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login():
    admin_id = request.form.get('admin_id')
    password = request.form.get('password')
    
    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM admin_config WHERE admin_id = ?', (admin_id,)).fetchone()
    conn.close()
    
    if admin and bcrypt.check_password_hash(admin['password_hash'], password):
        session['admin_logged_in'] = True
        session['admin_id'] = admin_id
        
        if admin['is_first_login'] == 1:
            return redirect(url_for('admin_first_login'))
        
        return redirect(url_for('admin_dashboard'))
    
    return "Invalid Credentials", 401

@app.route('/admin/first-login', methods=['GET', 'POST'])
def admin_first_login():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login_page'))
    
    if request.method == 'POST':
        pass_key = request.form.get('pass_key')
        new_password = request.form.get('new_password')
        
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admin_config WHERE admin_id = ?', (session['admin_id'],)).fetchone()
        
        if admin['pass_key'] == pass_key:
            hashed_pw = bcrypt.generate_password_hash(new_password).decode('utf-8')
            conn.execute('UPDATE admin_config SET password_hash = ?, is_first_login = 0 WHERE admin_id = ?', 
                         (hashed_pw, session['admin_id']))
            conn.commit()
            conn.close()
            return redirect(url_for('admin_dashboard'))
        else:
            conn.close()
            return "Invalid Pass-key!", 403
            
    return render_template('first_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login_page'))
    
    conn = get_db_connection()
    visit_count = conn.execute('SELECT COUNT(*) as count FROM visits').fetchone()['count']
    submit_count = conn.execute('SELECT COUNT(*) as count FROM submissions').fetchone()['count']
    conn.close()
    
    return render_template('dashboard.html', visit_count=visit_count, submit_count=submit_count)

@app.route('/admin/submissions')
def admin_submissions():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login_page'))
    
    date_filter = request.args.get('date')
    conn = get_db_connection()
    
    if date_filter:
        submissions = conn.execute('SELECT * FROM submissions WHERE date(timestamp) = ? ORDER BY timestamp DESC', (date_filter,)).fetchall()
    else:
        submissions = conn.execute('SELECT * FROM submissions ORDER BY timestamp DESC').fetchall()
        
    conn.close()
    return render_template('submissions.html', submissions=submissions)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login_page'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

from flask import Flask, render_template, redirect, request, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import init_db, get_user, get_user_by_id, create_user
from models import get_all_users

from services.uploads import upload_bp  # if you modularized uploads

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Init DB
init_db()

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class with role
class User(UserMixin):
    def __init__(self, id_, username, password, role):
        self.id = id_
        self.username = username
        self.password = password
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

# Admin-only decorator
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#icons 
def get_icon(filename):
    ext = filename.lower().split('.')[-1]
    if ext in ['jpg', 'jpeg', 'png', 'gif']: return "🖼️"
    if ext in ['pdf']: return "📄"
    if ext in ['css']: return "🎨"
    if ext in ['js']: return "📜"
    if ext in ['zip']: return "🗜️"
    if ext in ['py', 'php']: return "💻"
    return "📁"


# Routes

@app.route('/')
@login_required
def dashboard():
    user = get_user(current_user.username)
    return render_template('dashboard.html', username=user[1], role=user[3], last_login=user[4])

   
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user[2], password):
            user_obj = User(user[0], user[1], user[3])  # ID, username, role
            login_user(user_obj)
            update_last_login(username)  # <== Track login time here
            return redirect('/')
        else:
            flash('Invalid credentials')
            return redirect('/login')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        try:
            create_user(username, hashed_pw)  # default role = user
            flash('Account created! Please log in.')
            return redirect(url_for('login'))
        except:
            flash('Username already exists.')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/admin')
@admin_required
def admin_panel():
    users = get_all_users()
    return render_template('admin.html', users=users)


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        confirm = request.form['confirm']

        if new_password != confirm:
            flash("Passwords do not match.")
            return redirect('/reset-password')

        user = get_user(username)
        if not user:
            flash("User not found.")
            return redirect('/reset-password')

        new_hash = generate_password_hash(new_password)
        update_password(username, new_hash)
        flash("Password updated. You can now log in.")
        return redirect('/login')

    return render_template('reset_password.html')


# Register the upload module
app.register_blueprint(upload_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)



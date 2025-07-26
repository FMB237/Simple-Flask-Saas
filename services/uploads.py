import os
from flask import Blueprint, render_template, request, redirect, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import add_file, get_user_files, get_user_file_count, delete_file_record

upload_bp = Blueprint('upload_bp', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'zip', 'css', 'js', 'php'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_icon(filename):
    ext = filename.lower().split('.')[-1]
    if ext in ['jpg', 'jpeg', 'png', 'gif']: return "🖼️"
    if ext in ['pdf']: return "📄"
    if ext in ['css']: return "🎨"
    if ext in ['js']: return "📜"
    if ext in ['zip']: return "🗜️"
    if ext in ['py', 'php']: return "💻"
    return "📁"

# Dashboard showing uploaded files
@upload_bp.route('/upload')
@login_required
def upload_page():
    files = get_user_files(current_user.id)
    return render_template('upload.html', files=files, get_icon=get_icon)

# Upload handler
@upload_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    # File limit
    if get_user_file_count(current_user.id) >= 10:
        flash('Upload limit reached (10 files max).')
        return redirect('/upload')

    file = request.files.get('file')
    if not file or file.filename == '':
        flash('No file selected.')
        return redirect('/upload')

    if not allowed_file(file.filename):
        flash('File type not allowed.')
        return redirect('/upload')

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    add_file(current_user.id, filename)
    flash('File uploaded successfully.')
    return redirect('/upload')

# Delete a file
@upload_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    files = get_user_files(current_user.id)
    file_to_delete = next((f for f in files if f[0] == file_id), None)
    if file_to_delete:
        filename = file_to_delete[1]
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Remove physical file if exists
        if os.path.exists(filepath):
            os.remove(filepath)

        delete_file_record(current_user.id, file_id)
        flash('File deleted.')
    else:
        flash('File not found or not yours.')

    return redirect('/upload')

# Optional: download files
@upload_bp.route('/uploads/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


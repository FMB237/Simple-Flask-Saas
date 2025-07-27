
# 🧩 Simple SaaS Platform (Flask + SQLite)

A lightweight SaaS (Software-as-a-Service) platform built using Flask and SQLite, running in a virtual machine or Linux host. This application supports user authentication, file uploads, role-based dashboards, password reset, login tracking, and a simple admin interface.

---

## 🚀 Features

- ✅ User Registration & Login
- 🔐 Password Reset (username + new password)
- 🧑‍💻 Role-Based Access (User / Admin)
- 📤 File Uploads (PDFs, images, CSS, JS, etc.)
- 🗂️ Dashboard with download buttons & file icons
- ❌ File Deletion
- 📉 Upload Limit: 10 files/user
- 🕒 Last Login Tracking
- 🔒 Protected Routes & Sessions
- 🐳 Docker + SQLite (no need for external DB)
- 🧩 Modular Codebase (`models.py`, `upload.py`, `services/`, etc.)

---

## 📁 Project Structure

```
simple-saas/
│
├── app.py                # Main Flask entry point
├── models.py             # DB logic: users, login, roles
├── upload.py             # File upload/download logic
├── templates/            # HTML files (login, dashboard, upload, admin)
├── static/               # Custom CSS, JS, icons (optional)
├── users.db              # SQLite DB file
├── Dockerfile            # Optional Docker build
├── docker-compose.yml    # Run Flask + Nginx (optional)
├── requirements.txt      # Python packages
└── README.md             # This file
```

---

## 🛠️ Installation & Setup

### 1. Clone & Navigate
```bash
git clone https://github.com/your-username/simple-saas.git
cd simple-saas
```

### 2. Create a Virtual Environment
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python3 app.py
```

Open in browser:
```
http://127.0.0.1:5002
```

> You can also bind to all interfaces:
```python
app.run(host="0.0.0.0", port=5002)
```

---

## 👨‍🔧 Default Admin Setup

To make yourself admin:

```sql
sqlite3 users.db
UPDATE users SET role = 'admin' WHERE username = 'your-username';
.quit
```

---

## 🔐 Password Reset

- Visit `/reset-password`
- Provide username + new password

---

## 📈 Planned Improvements

Here’s how the project can evolve:

### ✨ Functional Upgrades
- Email-based password reset (with tokens)
- Storage quotas per user (MB/GB)
- Activity logs & audit dashboard
- Pagination of uploaded files
- Multi-file uploads

### 🧩 Technical Enhancements
- MySQL or PostgreSQL support
- Admin file moderation tools
- REST API for uploads/downloads
- Two-Factor Authentication (2FA)

### 🖥 UI/UX Improvements
- Animated dashboards with icons
- User profile settings page
- Mobile-first responsive design

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

Nginx handles reverse proxy. You can add HTTPS with Let's Encrypt + Certbot.

---

## 🤝 Contributing

Feel free to fork, clone, or extend the code. Suggestions and pull requests are welcome!

---

## 📄 License

MIT License

---

**Created by Miguel Bruce — École Nationale Supérieure Polytechnique de Douala (2025)**  
“Coding a better future, one SaaS at a time.”

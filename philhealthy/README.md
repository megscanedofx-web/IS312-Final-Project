# PhilHealthy 💊

**Pharmacy Business Process Management & Innovation System**

## Quick Start

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up the database (XAMPP/MySQL):**
   - Start Apache and MySQL in XAMPP
   - Open phpMyAdmin (http://localhost/phpmyadmin)
   - Import `database_setup.sql` or run it in the SQL tab

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:** http://localhost:5000

## Demo Accounts

| Role  | Email                    | Password  |
|-------|--------------------------|-----------|
| Admin | admin@philhealthy.com    | admin123  |
| Staff | staff@philhealthy.com    | staff123  |

## Project Structure

```
philhealthy/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── database_setup.sql      # MySQL database schema
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/style.css       # Main stylesheet
│   ├── js/main.js          # JavaScript functionality
│   └── img/                # Images
└── templates/
    ├── partials/           # Reusable components
    │   ├── base.html       # Base layout
    │   ├── navbar.html     # Public navigation
    │   ├── sidebar.html    # Dashboard sidebar
    │   └── chatbot.html    # AI Chatbot widget
    ├── public/             # Public pages
    │   ├── homepage.html
    │   ├── about.html
    │   ├── products.html
    │   └── contact.html
    ├── auth/               # Authentication pages
    │   ├── role_select.html
    │   ├── admin_login.html
    │   ├── staff_login.html
    │   └── register.html
    ├── staff/              # Staff dashboard
    │   ├── dashboard.html
    │   ├── inventory.html
    │   ├── deliveries.html
    │   ├── sales.html
    │   ├── transactions.html
    │   └── reports.html
    └── admin/              # Admin dashboard
        ├── dashboard.html
        ├── users.html
        └── deliveries.html
```

## Connecting to MySQL/XAMPP

In `app.py`, uncomment the MySQL configuration section and install flask-mysqldb:
```bash
pip install flask-mysqldb
```

## Deployment

For production deployment:
1. Set `SECRET_KEY` environment variable
2. Use a production WSGI server (gunicorn)
3. Set up a proper MySQL database
4. Configure HTTPS

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

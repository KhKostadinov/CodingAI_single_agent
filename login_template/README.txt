================================================================================
                    SECUREAUTH - FLASK LOGIN SYSTEM
                    Complete Documentation & Guide
================================================================================

OVERVIEW
--------
SecureAuth is a modern, responsive login system built with:
  • Backend:  Flask (Python) + SQLite (via Flask-SQLAlchemy)
  • Frontend: Pure HTML5, CSS3, and Vanilla JavaScript (NO frameworks)
  • Design:   Modern, professional, fully responsive (mobile-first)

FEATURES
--------
✓ User Registration with validation
✓ User Login with session management
✓ Password hashing (Werkzeug security)
✓ Password visibility toggle
✓ Password strength meter
✓ Real-time form validation (client + server)
✓ Flash messages (success/error)
✓ Protected dashboard route
✓ Responsive design (mobile, tablet, desktop)
✓ Accessible (ARIA labels, keyboard navigation)
✓ No external CSS/JS frameworks
✓ Clean, well-documented code

================================================================================
PROJECT STRUCTURE
================================================================================

login_template/
├── app.py                  # Main Flask application & routes
├── database.py             # Database models & initialization
├── requirements.txt        # Python dependencies
├── README.txt              # This file
├── templates/
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   └── dashboard.html      # Protected dashboard
└── static/
    ├── css/
    │   └── style.css       # All styles (responsive, modern)
    └── js/
        └── main.js         # Frontend interactivity

================================================================================
QUICK START
================================================================================

1. CREATE VIRTUAL ENVIRONMENT (recommended)
-------------------------------------------
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate

2. INSTALL DEPENDENCIES
------------------------
   pip install -r requirements.txt

3. RUN THE APPLICATION
-----------------------
   python app.py

   The server will start at: http://localhost:5000

4. OPEN IN BROWSER
-------------------
   Navigate to http://localhost:5000
   You'll be redirected to the login page.

================================================================================
API ROUTES
================================================================================

GET  /              → Redirect to login or dashboard based on session
GET  /login         → Show login form
POST /login         → Authenticate user (username + password)
GET  /register      → Show registration form
POST /register      → Create new user (username, email, password, confirm)
GET  /dashboard     → Protected page (requires login)
GET  /logout        → Clear session and redirect to login
GET  /api/session   → JSON: check if user is authenticated

================================================================================
DATABASE SCHEMA
================================================================================

Table: users
┌─────────────────┬──────────────────────────────────────────────────────────┐
│ Column          │ Type / Constraints                                       │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ id              │ INTEGER, PRIMARY KEY, AUTOINCREMENT                      │
│ username        │ VARCHAR(80), UNIQUE, NOT NULL                            │
│ email           │ VARCHAR(120), UNIQUE, NOT NULL                           │
│ password_hash   │ VARCHAR(256), NOT NULL (Werkzeug hashed)                 │
│ created_at      │ DATETIME, DEFAULT CURRENT_TIMESTAMP                      │
│ last_login      │ DATETIME, NULLABLE                                       │
└─────────────────┴──────────────────────────────────────────────────────────┘

The SQLite database file (app.db) is created automatically in the project
root directory on first run.

================================================================================
EXAMPLE USAGE
================================================================================

EXAMPLE 1: Register a New User
-------------------------------
  1. Navigate to http://localhost:5000/register
  2. Fill in:
     - Username: "johndoe"
     - Email:    "john@example.com"
     - Password: "SecurePass123!"
     - Confirm:  "SecurePass123!"
  3. Click "Create Account"
  4. You'll be redirected to login with a success message.

EXAMPLE 2: Login
-----------------
  1. Navigate to http://localhost:5000/login
  2. Enter username: "johndoe"
  3. Enter password: "SecurePass123!"
  4. Click "Sign In"
  5. You'll be redirected to the dashboard.

EXAMPLE 3: API Session Check
-----------------------------
  $ curl http://localhost:5000/api/session
  # Logged out: {"authenticated": false}
  # Logged in:  {"authenticated": true, "user": {...}}

EXAMPLE 4: Programmatic Access (Python)
----------------------------------------
  from app import app
  from database import db, User

  with app.app_context():
      # Create user
      user = User(username="testuser", email="test@test.com")
      user.set_password("mypassword")
      db.session.add(user)
      db.session.commit()

      # Verify password
      print(user.check_password("mypassword"))  # True
      print(user.check_password("wrongpass"))   # False

      # Query users
      all_users = User.query.all()
      for u in all_users:
          print(u.username, u.email)

================================================================================
SECURITY NOTES
================================================================================

• Passwords are hashed using Werkzeug's generate_password_hash (PBKDF2)
• Sessions use Flask's signed cookies (HMAC-SHA1)
• SQL injection is prevented via SQLAlchemy ORM (parameterized queries)
• XSS is mitigated by Jinja2 auto-escaping
• CSRF protection: For production, add Flask-WTF CSRF tokens
• Rate limiting: For production, add flask-limiter
• HTTPS: Always serve behind a reverse proxy (nginx) with SSL in production

================================================================================
PRODUCTION DEPLOYMENT CHECKLIST
================================================================================

[ ] Set a strong SECRET_KEY via environment variable
[ ] Set FLASK_ENV=production
[ ] Use gunicorn or uWSGI as WSGI server
[ ] Configure nginx/Apache as reverse proxy with SSL
[ ] Add CSRF protection (Flask-WTF)
[ ] Add rate limiting (flask-limiter)
[ ] Add logging (Python logging module)
[ ] Back up the SQLite database regularly
[ ] Consider migrating to PostgreSQL for high-traffic apps
[ ] Add email verification for new accounts
[ ] Add password reset functionality
[ ] Add 2FA (Two-Factor Authentication)

================================================================================
CUSTOMIZATION GUIDE
================================================================================

CHANGING COLORS
----------------
Edit the CSS custom properties at the top of static/css/style.css:

  :root {
      --color-primary: #4f46e5;        /* Main brand color */
      --color-primary-hover: #4338ca;  /* Hover state */
      --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

CHANGING FONT
-------------
Update the --font-family variable:

  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

ADDDING NEW FIELDS
-------------------
1. Add column to User model in database.py
2. Add form field in the relevant template
3. Add validation in app.py route handler
4. Add CSS if needed (usually .form-group handles it)

================================================================================
TROUBLESHOOTING
================================================================================

Q: "ModuleNotFoundError: No module named 'flask'"
A:  Make sure your virtual environment is activated and run:
    pip install -r requirements.txt

Q: "Address already in use"
A:  Port 5000 is occupied. Either stop the other process or change the port:
    python app.py  →  Change port in app.run(port=5000) to e.g. 5001

Q: Database not created
A:  Ensure you're running from the login_template/ directory.
    The app.db file should appear in the same folder as app.py.

Q: Styles not loading
A:  Check that the static/ folder structure is correct and that
    url_for('static', filename='css/style.css') resolves properly.

Q: Flash messages not showing
A:  Ensure the SECRET_KEY is set. Check browser console for JS errors.

================================================================================
LICENSE
================================================================================
MIT License - Free to use, modify, and distribute.

================================================================================
                              END OF DOCUMENTATION
================================================================================

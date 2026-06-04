#!/usr/bin/env python3
"""
IEEENet Flask2 - Simple Directory Serving with Auth
Each route serves its entire directory contents (like http.server but with auth)
"""

import os
from functools import wraps
from flask import Flask, render_template_string, jsonify, request, redirect, url_for, session, send_from_directory

# Configuration
app = Flask(__name__)
app.secret_key = os.urandom(24)
HOST = "0.0.0.0"
PORT = 80

# Credentials (CHANGE THESE FOR PRODUCTION!)
CREDENTIALS = {
    "username": "zlatan",
    "password": "a-vocal-incident-12345"
}

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Route directories - each serves its full content
ROUTE_DIRS = {
    "liapress": os.path.join(BASE_DIR, "liapress"),
    "express": os.path.join(BASE_DIR, "express"),
    "greetings": os.path.join(BASE_DIR, "greetings")
}


# Login HTML
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IEEENet - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex; align-items: center; justify-content: center;
            color: #fff;
        }
        .container { text-align: center; max-width: 800px; padding: 2rem; }
        h1 {
            font-size: 3rem; margin-bottom: 1rem;
            background: linear-gradient(45deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text; color: transparent;
        }
        p { font-size: 1.2rem; color: #a0a0a0; margin-bottom: 2rem; }
        .login-form { background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 10px; max-width: 400px; margin: 0 auto; }
        .form-group { margin-bottom: 1.5rem; text-align: left; }
        .form-group label { display: block; margin-bottom: 0.5rem; color: #a0a0a0; }
        .form-group input {
            width: 100%; padding: 0.75rem; border: none; border-radius: 5px;
            background: rgba(255,255,255,0.1); color: white; font-size: 1rem;
        }
        .form-group input:focus { outline: 2px solid #00d4ff; }
        .button {
            background: linear-gradient(45deg, #00d4ff, #7b2cbf);
            border: none; color: white; padding: 1rem 2rem;
            border-radius: 5px; font-size: 1rem; cursor: pointer;
        }
        .error-message { background: rgba(255,0,0,0.2); color: #ff6b6b; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>IEEENet</h1>
        <p>Authorized Access Only</p>
        {% if error %}<div class="error-message">⚠️ {{ error }}</div>{% endif %}
        <form method="POST" action="/login" class="login-form">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="button">Login</button>
        </form>
    </div>
</body>
</html>
"""


def login_required(f):
    """Decorator to protect routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Public Routes
@app.route("/")
def login():
    """Login route"""
    if 'logged_in' in session:
        return redirect('/liapress')
    return render_template_string(LOGIN_TEMPLATE)


@app.route("/login", methods=["POST"])
def process_login():
    """Process login credentials"""
    username = request.form.get("username")
    password = request.form.get("password")
    
    if username == CREDENTIALS["username"] and password == CREDENTIALS["password"]:
        session.clear()
        session['logged_in'] = True
        session['username'] = username
        return redirect('/liapress')
    else:
        return render_template_string(LOGIN_TEMPLATE, error="Invalid credentials. Access denied.")


@app.route("/logout")
def logout():
    """Clear session"""
    session.clear()
    return redirect(url_for('login'))


@app.route("/dashboard")
def dashboard():
    """Redirect to first route"""
    return redirect('/liapress')


# Protected Routes - Serve entire directory contents
@app.route("/liapress")
@app.route("/liapress/<path:filename>")
def liapress(filename=None):
    """Serve liapress directory contents"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    route_dir = ROUTE_DIRS.get("liapress")
    if not route_dir or not os.path.exists(route_dir):
        return "liapress directory not found", 404
    
    if filename is None:
        filename = "index.html"
    
    file_path = os.path.join(route_dir, filename)
    if not os.path.exists(file_path):
        return f"{filename} not found", 404
    
    return send_from_directory(route_dir, filename)


@app.route("/express")
@app.route("/express/<path:filename>")
def express(filename=None):
    """Serve express directory contents"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    route_dir = ROUTE_DIRS.get("express")
    if not route_dir or not os.path.exists(route_dir):
        return "express directory not found", 404
    
    if filename is None:
        filename = "index.html"
    
    file_path = os.path.join(route_dir, filename)
    if not os.path.exists(file_path):
        return f"{filename} not found", 404
    
    return send_from_directory(route_dir, filename)


@app.route("/greetings")
@app.route("/greetings/<path:filename>")
def greetings(filename=None):
    """Serve greetings directory contents"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    route_dir = ROUTE_DIRS.get("greetings")
    if not route_dir or not os.path.exists(route_dir):
        return "greetings directory not found", 404
    
    if filename is None:
        filename = "index.html"
    
    file_path = os.path.join(route_dir, filename)
    if not os.path.exists(file_path):
        return f"{filename} not found", 404
    
    return send_from_directory(route_dir, filename)


# API Routes (protected)
@app.route("/api/status")
def api_status():
    """API status endpoint"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    return jsonify({
        "status": "online",
        "server": "Flask",
        "version": "2.0.0",
        "authenticated": session.get('logged_in', False),
        "username": session.get('username'),
        "timestamp": os.popen("date -u '+%Y-%m-%d %H:%M:%S UTC'").read().strip()
    })


@app.route("/health")
def health():
    """Health check (no auth)"""
    return jsonify({"healthy": True}), 200


def main():
    """Main server startup"""
    print("=" * 60)
    print("  IEEENet Flask2 Server (Directory Serving)")
    print(f"  http://localhost:{PORT}")
    print("=" * 60)
    print(f"\n🔐 Credentials:")
    print(f"   Username: {CREDENTIALS['username']}")
    print(f"   Password: {CREDENTIALS['password']}")
    print(f"   ⚠️  CHANGE THESE IN CODE!")
    print(f"\n📡 Routes:")
    print(f"   /              - Login page")
    print(f"   /dashboard     - Redirects to /liapress")
    print(f"   /liapress      - Serves liapress/ (auth required)")
    print(f"   /express       - Serves express/ (auth required)")
    print(f"   /greetings     - Serves greetings/ (auth required)")
    print(f"\n📁 Route directories:")
    for route, path in ROUTE_DIRS.items():
        exists = "✅" if os.path.exists(path) else "❌"
        has_index = "✅" if os.path.exists(os.path.join(path, "index.html")) else "❌"
        print(f"   {exists} {route}/ -> {path}")
        print(f"      index.html: {has_index}")
    print(f"\n📡 Server starting on {HOST}:{PORT}")
    print("🚀 Press CTRL+C to stop\n")
    
    app.run(host=HOST, port=PORT, debug=True, threaded=True)


if __name__ == "__main__":
    main()


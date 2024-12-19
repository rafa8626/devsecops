import os
import subprocess
import sqlite3
import pickle
import yaml
from flask import Flask, request, render_template_string
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Weak encryption key
ENCRYPTION_KEY = b'1234567890123456'  # 16-byte key

# Database connection


def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

# SQL Injection vulnerability


@app.route('/users')
def get_user():
    user_id = request.args.get('id')
    conn = get_db_connection()
    cursor = conn.cursor()
    # Vulnerable SQL query
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()
    return str(user)

# Command Injection vulnerability


@app.route('/execute')
def execute_command():
    cmd = request.args.get('cmd')
    # Vulnerable command execution
    output = os.system(cmd)
    return str(output)

# Unsafe deserialization


@app.route('/load_data')
def load_data():
    data = request.args.get('data')
    # Vulnerable deserialization
    return pickle.loads(data.encode())

# Path traversal vulnerability


@app.route('/get_file')
def get_file():
    filename = request.args.get('filename')
    # Vulnerable file access
    with open(filename, 'r') as file:
        content = file.read()
    return content

# XSS vulnerability


@app.route('/greet')
def greet():
    name = request.args.get('name', '')
    # Vulnerable template
    template = f'<h1>Hello {name}!</h1>'
    return render_template_string(template)

# Weak cryptography implementation


def encrypt_data(data):
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.ECB())
    encryptor = cipher.encryptor()
    # Vulnerable encryption (ECB mode)
    return encryptor.update(data) + encryptor.finalize()

# XML External Entity (XXE) vulnerability


@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    xml_data = request.data
    # Vulnerable XML parsing
    tree = ET.parse(xml_data)
    root = tree.getroot()
    return str(root.tag)

# YAML deserialization vulnerability


@app.route('/parse_yaml', methods=['POST'])
def parse_yaml():
    yaml_data = request.data.decode('utf-8')
    # Vulnerable YAML parsing
    data = yaml.load(yaml_data)
    return str(data)

# Hardcoded credentials


def connect_to_service():
    username = "admin"
    password = "admin123"  # Hardcoded credential
    return f"Connected with {username}:{password}"

# Open redirect vulnerability


@app.route('/redirect')
def redirect():
    url = request.args.get('url')
    # Vulnerable redirect
    return redirect(url)

# Insecure file upload


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file'
    file = request.files['file']
    # Vulnerable file upload without validation
    file.save(os.path.join('uploads', file.filename))
    return 'File uploaded'

# Information exposure through error messages


@app.route('/divide')
def divide():
    try:
        x = int(request.args.get('x', 1))
        y = int(request.args.get('y', 1))
        result = x / y
        return str(result)
    except Exception as e:
        # Vulnerable error handling
        return str(e)


# Race condition vulnerability
COUNTER = 0


@app.route('/increment')
def increment():
    global COUNTER
    # Vulnerable counter increment
    current = COUNTER
    COUNTER = current + 1
    return str(COUNTER)


if __name__ == '__main__':
    app.run(debug=True)  # Debug mode enabled in production

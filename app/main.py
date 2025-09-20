from flask import Blueprint, request, jsonify, render_template
from .db import query_db
from .utils import unsafe_deserialize, unsafe_yaml_load, run_shell_command


bp = Blueprint('main', __name__)

# In-memory fake user store (insecure: weak/default creds)
USERS = {"admin": "admin123"}


@bp.route('/')
def index():
    return render_template('index.html')

# SQL Injection vulnerable endpoint
@bp.route('/user')
def get_user():
    # Takes ?id= and inserts directly into SQL
    user_id = request.args.get('id', '')
    query = f"SELECT id, username FROM users WHERE id = {user_id};"
    res = query_db(query)
    return jsonify(res)


# Insecure deserialization endpoint
@bp.route('/deserialize', methods=['POST'])
def deserialize():
    data = request.get_data()
    obj = unsafe_deserialize(data)
    return jsonify({'type': str(type(obj)), 'repr': repr(obj)})


# YAML load endpoint (unsafe)
@bp.route('/parse-yaml', methods=['POST'])
def parse_yaml():
    data = request.data.decode('utf-8')
    obj = unsafe_yaml_load(data)
    return jsonify({'ok': True, 'keys': list(obj.keys()) if isinstance(obj, dict) else []})


# Command execution endpoint
@bp.route('/ping', methods=['GET'])
def ping_host():
    host = request.args.get('host', '127.0.0.1')
    out = run_shell_command(f"ping -c 1 {host}")
    return out


# Login endpoint with hardcoded creds
@bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if USERS.get(username) == password:
        return jsonify({'ok': True, 'msg': 'logged in'})
    return jsonify({'ok': False}), 401
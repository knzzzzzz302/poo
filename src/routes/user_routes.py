from flask import Blueprint, request, jsonify, session, redirect, url_for
from src.services.user_service import UserService

user_bp = Blueprint('user', __name__)
user_service = UserService()

@user_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    try:
        user = user_service.register(data.get('username'), data.get('email'), 
                                    data.get('password'), data.get('user_type', 'regular'))
        return jsonify({'success': True, 'user': {'id': user.id}}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@user_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    user = user_service.authenticate(data.get('email'), data.get('password'))
    if user:
        session['user_id'] = user.id
        return jsonify({'success': True, 'user': {'id': user.id}}), 200
    return jsonify({'success': False}), 401

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('users/login.html')

@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
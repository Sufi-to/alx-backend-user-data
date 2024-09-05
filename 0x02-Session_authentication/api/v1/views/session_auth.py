#!/usr/bin/env python3
""" Module of Authentication views"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def user_login():
    """Authenticate user to login"""
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
   
    try:
        all_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not all_users:
        return jsonify({"error": "no user found for this email"}), 404

    for i in all_users:
        if not i.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    user_id = all_users[0].id
    from api.v1.app import auth

    session_id = auth.create_session(user_id)
    session_name = getenv("SESSION_NAME")
    user_dict = jsonify(i.to_json())
    user_dict.set_cookie(session_name, session_id)
    return user_dict


@app_views.route('auth_session/logout', methods=["DELETE"], strict_slashes=False)
def user_logout():
    """Logout the user"""
    from api.v1.app import auth
    destroy = auth.destroy_session(request)
    return jsonify({}), 200 if destroy else abort(404)
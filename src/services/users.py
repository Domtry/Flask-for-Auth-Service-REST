from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from werkzeug.security import (check_password_hash, generate_password_hash)
import validators

from sqlalchemy import select

from src.domain.model import Users
from src.adpater.sqlite_connexion import db_session
user_bp = Blueprint("Users", __name__, url_prefix="/api/v1/user")

@user_bp.post('/')
@cross_origin()
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(username) == 0 :
        return jsonify({
            'msg': "user value has not found",
            'status': 'faild',
            }), 400

    if not username.isalnum() or " " in username:
        return jsonify({
            'msg': 'Username hould be alphanumeric, also no spaces',
            'status': 'faild',
            }), 400

    if len(password) < 6 :
        return jsonify({
            'msg': 'Password is too short',
            'status': 'faild',
            }), 400

    if not validators.email(email):
        return jsonify({
            'msg': 'Email has not valid please write god email',
            'status': 'faild',
            }), 400
    
    stmt = select(Users).where(Users.username == username)
    if db_session.execute(stmt).first():
        return jsonify({'msg': f'this username <{username}> has used', 'status': 'faild'}), 400
    
    stmt = select(Users).where(Users.email == email)
    if db_session.execute(stmt).first():
        return jsonify({'msg': f'this email <{email}> has used', 'status': 'faild'}), 400

    hash_password = generate_password_hash(password)
    user = Users()
    user.username = username
    user.email = email
    user.password = hash_password

    try:
        db_session.add(user)
        db_session.commit()
        return jsonify({
            'msg': 'user has created',
            'status': 'success',
            'data': {
                'username': username,
                'email': email
            }}), 200
    except Exception as e:
        print(f'error msg :::> {e}')
        return jsonify({
            'error': 'sql server error',
            'status': 'faild',
            }), 400
    finally:
        db_session.close()
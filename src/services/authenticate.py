from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import (check_password_hash, generate_password_hash)

from sqlalchemy import select

from src.domain.model import Authenticates, Tokens, Users
from src.adpater.sqlite_connexion import db_session
auth_bp = Blueprint("Authentication", __name__, url_prefix="/api/v1/auth")

@auth_bp.post('/')
@cross_origin()
def auth():
    username = request.json['username']
    password = request.json['password']

    if len(username) == 0 :
        return jsonify({
            'msg': "user value has not found",
            'status': 'faild',
            }), 400

    stmt = select(Users).where(Users.username == username)
    result = db_session.execute(stmt).first()
    if not result:
        return jsonify({'msg': 'username or password has not valid', 'status': 'faild'}), 401

    user = result[0]
    if check_password_hash(user.password, password):
        access_token = create_access_token(identity=f'{user.id}')
        refresh_token = create_refresh_token(identity=f'{user.id}')
        
        authenticate = Authenticates()
        authenticate.user_id = user.id
        authenticate.status = True
        db_session.add(authenticate)
        db_session.commit()
        
        stmt = select(Authenticates).where(Authenticates.user_id == user.id)
        authenticat_info = db_session.execute(stmt).first()[0]
        
        token = Tokens()
        token.access_key = access_token
        token.auth_id = authenticat_info.id
        db_session.add(token)
        db_session.commit()
        
        auth_email = user.email
        auth_username = user.username
        db_session.close()

        return jsonify({
            'refresh_token': refresh_token,
            'access_token': access_token,
            'username': auth_username,
            'email': auth_email
        })

    return jsonify({'error': 'Wrong credentials'})
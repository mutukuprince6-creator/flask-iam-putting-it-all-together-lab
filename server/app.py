#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe, UserSchema, RecipeSchema

class Signup(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'errors': ['Username and password are required.']}, 422

        user = User(
            username=username,
            image_url=data.get('image_url'),
            bio=data.get('bio'),
        )
        user.password_hash = password

        try:
            db.session.add(user)
            db.session.commit()
        except (IntegrityError, ValueError) as error:
            db.session.rollback()
            return {'errors': [str(error)]}, 422

        session['user_id'] = user.id
        return UserSchema().dump(user), 201

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        user = db.session.get(User, user_id) if user_id else None
        if not user:
            return {'errors': ['Unauthorized']}, 401
        return UserSchema().dump(user), 200

class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        user = User.query.filter(User.username == data.get('username')).first()
        if not user or not data.get('password') or not user.authenticate(data['password']):
            return {'errors': ['Invalid username or password.']}, 401

        session['user_id'] = user.id
        return UserSchema().dump(user), 200

class Logout(Resource):
    def delete(self):
        if not session.get('user_id'):
            return {'errors': ['Unauthorized']}, 401
        session.pop('user_id', None)
        return '', 204

class RecipeIndex(Resource):
    def get(self):
        if not session.get('user_id'):
            return {'errors': ['Unauthorized']}, 401
        return RecipeSchema(many=True).dump(Recipe.query.all()), 200

    def post(self):
        user_id = session.get('user_id')
        user = db.session.get(User, user_id) if user_id else None
        if not user:
            return {'errors': ['Unauthorized']}, 401

        data = request.get_json() or {}

        try:
            recipe = Recipe(
                title=data.get('title'),
                instructions=data.get('instructions'),
                minutes_to_complete=data.get('minutes_to_complete'),
                user=user,
            )
            db.session.add(recipe)
            db.session.commit()
        except (IntegrityError, ValueError) as error:
            db.session.rollback()
            return {'errors': [str(error)]}, 422

        return RecipeSchema().dump(recipe), 201

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
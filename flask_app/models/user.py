from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import magazine
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = "python_belt_exam"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.magazines = []

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user_id = connectToMySQL(cls.db).query_db(query, data)
        return user_id

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        user_id = connectToMySQL(cls.db).query_db(query, data)
        return user_id

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results)<1:
            return False
        row = results[0]
        user = cls(row)
        return user

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if (len(results))<1:
            return False
        row = results[0]
        user = cls(row)
        return user

    @staticmethod
    def validate_register(user):
        is_valid = True

        user_in_db = User.get_user_by_email(user)
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email', 'reg_error')
            is_valid = False
        if user_in_db:
            flash('Email is associated with another account', 'reg_error')
            is_valid = False
        if (len(user['first_name']))<3:
            flash('First Name must be at least 3 characters', 'reg_error')
            is_valid = False
        if (len(user['last_name']))<3:
            flash('Last Name must be at least 3 characters', 'reg_error')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords must match', 'reg_error')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True

        user_in_db = User.get_user_by_email(user)
        if not user_in_db:
            flash('Email is not tied to an account', 'log_error')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email', 'log_error')
            is_valid = False
        if len(user['password']) <8:
            flash('Password must be at least 8', 'log_error')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update(user):
        is_valid = True
        user_in_db = User.get_user_by_email(user)
        if (len(user['first_name'])) <1 and (len(user['last_name']))<1 and (len(user['email']))<1:
            flash('First name, last name, and email are all required', 'update_error')
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email', 'update_error')
            is_valid = False
        if user_in_db and (int(user_in_db.id) != int(user['id'])):
            flash('Email is associated with another account', 'update_error')
            is_valid = False
        if (len(user['first_name']))<3:
            flash('First Name must be at least 3 characters', 'update_error')
            is_valid = False
        if (len(user['last_name']))<3:
            flash('Last Name must be at least 3 characters', 'update_error')
            is_valid = False
        return is_valid
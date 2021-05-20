from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_userInfo(data):
        is_valid = True 
        if len(data['first_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            is_valid= False
            flash("Invalid email address!")
        if len(data['password']) < 8:
            flash("Password must be 8 characters long or longer.")
            is_valid = False
        if not data['password'] == data['conf_password']:
            flash("Password and Confirmation password must be equal.")
            is_valid = False
        return is_valid


    @classmethod
    def save(cls, data):
        query = ' INSERT INTO  user (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL('PyPie_Derby').query_db(query, data)


    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM user WHERE id = %(id)s;'
        user =connectToMySQL('PyPie_Derby').query_db(query, data)
        # print(user)
        # print("-------------")
        return user[0]

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        result = connectToMySQL("PyPie_Derby").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
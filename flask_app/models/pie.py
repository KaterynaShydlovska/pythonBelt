from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Pie:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.vote = data['vote']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_pie(data):
        is_valid = True 
        if len(data['name']) < 3:
            flash("Name must be at least 5 characters long!")
            is_valid = False
        if len(data['filling']) < 2:
            flash("Filling must be at least 2 characters long!")
            is_valid = False                    
        if len(data['crust']) < 3:
            flash("Crust must be at least 3 characters long!")
            is_valid = False
        return is_valid

    @classmethod
    def create(cls, data):
        query = ' INSERT INTO  pie (user_id, name, filling,  crust) VALUES ( %(user_id)s, %(name)s, %(filling)s, %(crust)s);'
        res = connectToMySQL('PyPie_Derby').query_db(query, data)
        return res

    @classmethod
    def getAllpiesForUser(cls, data):
        query = ' SELECT * FROM pie LEFT JOIN user ON user.id = pie.user_id WHERE user.id = %(id)s;'
        res = connectToMySQL('PyPie_Derby').query_db(query, data)
        return res

    @classmethod
    def getOnePie(cls, data):
        query = ' SELECT * FROM pie WHERE id = %(id)s;'
        res = connectToMySQL('PyPie_Derby').query_db(query, data)
        return res

    @classmethod
    def updatePie(cls, data):
        query = 'UPDATE pie SET name=%(name)s, filling=%(filling)s, crust=%(crust)s WHERE id = %(id)s;'
        res = connectToMySQL('PyPie_Derby').query_db(query, data)
        return res

        

    @classmethod
    def deletePie(cls, data):
        query = 'DELETE FROM pie WHERE id = %(id)s;'
        connectToMySQL('PyPie_Derby').query_db(query, data)

    @classmethod
    def getAllpies(cls):
        query = ' SELECT * FROM pie LEFT JOIN user ON user.id = pie.user_id;'
        res = connectToMySQL('PyPie_Derby').query_db(query)
        return res

    @classmethod
    def getPieWithUser(cls, data):
        query = ' SELECT * FROM pie LEFT JOIN user ON user.id = pie.user_id WHERE pie.id = %(id)s;'
        res = connectToMySQL('PyPie_Derby').query_db(query, data)
        return res

    @classmethod
    def updateVotes(cls, data):
        query = 'UPDATE pie SET vote=%(vote)s WHERE id = %(id)s;'
        res = connectToMySQL('PyPie_Derby').query_db(query, data)
        return res

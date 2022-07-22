from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Subscription:
    db = "python_belt_exam"

    def __init__(self,data):
        self.user_id = data['user_id']
        self.magazine_id = data['magazine_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO subscriptions (user_id, magazine_id) VALUES(%(user_id)s, %(magazine_id)s);"
        subscription = connectToMySQL(cls.db).query_db(query, data)
        flash('subscribed successfully', 'subscribed')
        return subscription

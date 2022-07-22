from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Magazine:
    db = "python_belt_exam"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.users_who_subscribed = []
        self.user_ids_who_subscribed = []

    @classmethod
    def create_magazine(cls, data):
        query = "INSERT INTO magazines(title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s);"
        magazine_id = connectToMySQL(cls.db).query_db(query, data)
        data = {
            'id': session['user_id']
        }
        return magazine_id


    @classmethod
    def get_all(cls):
        query = '''SELECT * FROM magazines JOIN users AS subscribers ON magazines.user_id = subscribers.id
            LEFT JOIN subscriptions ON magazines.id = subscriptions.magazine_id
            LEFT JOIN users AS users_who_subscribed ON subscriptions.user_id = users_who_subscribed.id;'''
        results = connectToMySQL(cls.db).query_db(query)
        magazines = []
        for row in results:
            new_magazine = True
            user_who_subscribed_data = {
                'id': row['users_who_subscribed.id'],
                'first_name': row['users_who_subscribed.first_name'],
                'last_name': row['users_who_subscribed.last_name'],
                'email': row['users_who_subscribed.email'],
                'password': row['users_who_subscribed.password'],
                'created_at': row['users_who_subscribed.created_at'],
                'updated_at': row['users_who_subscribed.updated_at']
            }
            number_of_magazines = len(magazines)
            if number_of_magazines > 0:
                last_magazine = magazines[number_of_magazines-1]
                if last_magazine.id == row['id']:
                    last_magazine.user_ids_who_subscribed.append(row['users_who_subscribed.id'])
                    last_magazine.users_who_subscribed.append(user.User(user_who_subscribed_data))
                    new_magazine = False
            if new_magazine:
                magazine = cls(row)
                user_data = {
                    'id': row['subscribers.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['subscribers.created_at'],
                    'updated_at': row['subscribers.updated_at']
                }
                user_fill = user.User(user_data)
                magazine.user = user_fill
                if row['users_who_subscribed.id']:
                    magazine.user_ids_who_subscribed.append(row['users_who_subscribed.id'])
                    magazine.users_who_subscribed.append(user.User(user_who_subscribed_data))
                magazines.append(magazine)
        return magazines


    @classmethod
    def get_all_from_user(cls, data):
        query = "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        magazines = []
        for row in results:
            magazine = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user_fill = user.User(user_data)
            magazine.user = user_fill
            magazines.append(magazine)
        return magazines

    @classmethod
    def get_one(cls, data):
        query = '''SELECT * FROM magazines 
                JOIN users AS subscribers ON reviews.user_id=creators.id
                LEFT JOIN favorited_reviews ON favorited_reviews.review_id=reviews.id
                LEFT JOIN users AS users_who_favorited ON favorited_reviews.user_id = users_who_favorited.id
                WHERE reviews.id = %(id)s;
        '''
        
        "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id WHERE magazines.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results)<1:
            return False
        row = results[0]
        magazine = cls(row)
        user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
        user_fill = user.User(user_data)
        magazine.user = user_fill
        return magazine


        query='''SELECT * FROM reviews 
                JOIN users AS creators ON reviews.user_id=creators.id
                LEFT JOIN favorited_reviews ON favorited_reviews.review_id=reviews.id
                LEFT JOIN users AS users_who_favorited ON favorited_reviews.user_id = users_who_favorited.id
                WHERE reviews.id = %(id)s;'''
        
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False

        new_review = True
        for row in results:
            #if this is the first row being processed
            if new_review:
                review = cls(row)
                #Create a user object
                user_data = {
                    'id': row['creators.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'created_at': row['creators.created_at'],
                    'updated_at': row['creators.updated_at'],
                    'email': row['email'],
                    'password': row['password']  
                }
                creator = User(user_data)
                review.creator = creator
                new_review = False
            
            if row['users_who_favorited.id']:
                user_who_favorited_data = {
                    'id': row['users_who_favorited.id'],
                    'first_name': row['users_who_favorited.first_name'],
                    'last_name': row['users_who_favorited.last_name'],
                    'created_at': row['users_who_favorited.created_at'],
                    'updated_at': row['users_who_favorited.updated_at'],
                    'email': row['users_who_favorited.email'],
                    'password': row['users_who_favorited.password']  
                }
                user_who_favorited = User(user_who_favorited_data)
                review.users_who_favorited.append(user_who_favorited)
                review.user_ids_who_favorited.append(row['users_who_favorited.id'])
                
        return review


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM magazines WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @staticmethod
    def validate_magazine(magazine):
        is_valid = True
        if (len(magazine['title'])) <1 and (len(magazine['description']))<1:
            flash('Title and description are both required', 'mag_error')
            is_valid = False
        if (len(magazine['title']))<2:
            flash('Title must be at least 2 characters', 'mag_error')
            is_valid = False
        if (len(magazine['description']))<10:
            flash('Description must be at least 10 characters', 'mag_error')
            is_valid = False

        return is_valid

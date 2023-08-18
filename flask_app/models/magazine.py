from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Magazine:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.creator_id = data['creator_id']
        self.creator = None
        self.subscribers = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO magazines(title, description,creator_id, created_at,updated_at) VALUES (%(title)s, %(description)s, %(creator_id)s,Now(),Now());"
        return connectToMySQL('subscriptiondb').query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM magazines LEFT JOIN users ON magazines.creator_id = users.id;"
        results = connectToMySQL("subscriptiondb").query_db(query)
        magazines = []
        for magazine in results:
            new_mag = cls(magazine)
            new_mag.creator = user.User.get_by_id({"id": magazine['users.id']})
            magazines.append(new_mag)
        return magazines
    
    @classmethod
    def get_all_w_count(cls,data):
        query = "SELECT magazines.*, COUNT(subscribers.user_id) AS count FROM magazines LEFT JOIN subscribers ON magazines.id = subscribers.magazine_id GROUP BY magazines.id;"
        results = connectToMySQL('subscriptiondb').query_db(query,data)
        magazines = []
        for mag in results:
            new_mag = cls(mag)
            new_mag.count = mag['count']
            magazines.append(new_mag)
        return magazines
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM magazines LEFT JOIN subscribers ON magazines.id = subscribers.magazine_id LEFT JOIN users ON subscribers.user_id = users.id WHERE magazines.id = %(id)s;"
        result = connectToMySQL("subscriptiondb").query_db(query,data)
        magazine = cls(result[0])

        for row in result:
            if row['users.id']:
                subscriber_data = {
                    "id": row['users.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
                }
                magazine.subscribers.append(user.User(subscriber_data))
        magazine.creator = user.User.get_by_id({"id": magazine.creator_id})
        return magazine
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM magazines WHERE id = %(id)s;"
        return connectToMySQL("subscriptiondb").query_db(query,data)
    
    @classmethod
    def subscribe(cls,data):
        query = "INSERT INTO subscribers (user_id,magazine_id) VALUES (%(user_id)s,%(magazine_id)s);"
        return connectToMySQL("subscriptiondb").query_db(query,data)

    @staticmethod
    def validate_mag(mag):
        is_valid = True
        if len(mag['title']) < 2:
            flash("Title must be at least 2 characters.")
            is_valid = False
        if len(mag['description']) < 10:
            flash("Description must be at least 10 characters.")
            is_valid = False
        return is_valid

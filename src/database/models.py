from .db import db
from flask_bcrypt import generate_password_hash,check_password_hash

class Movie(db.Document):
    name = db.StringField(required=True,unique=True)
    cast = db.ListField(db.StringField(),required=True)
    genres = db.ListField(db.StringField(),required=True)
    img_path = db.StringField()
    added_by = db.ReferenceField('User')

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    movies = db.ListField(db.ReferenceField('Movie', reverse_delete_rule=db.PULL))
    
    def hash_password(self):
        self.pasword = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self,password):
        return check_password_hash(self.password,password)

User.register_delete_rule(Movie, 'added_by', db.CASCADE) # all the movies added by this user gets deleted when the user is deleted
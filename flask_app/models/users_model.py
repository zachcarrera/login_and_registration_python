import re

from flask import flash

from flask_app import DATABASE, BCRYPT
from flask_app.config.mysqlconnection import connectToMySQL

# constant EMAIL_REGEX used to validate emails
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# constant NAME_REGEX to validate the names are atleast 2 characters and only letters
NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, form):
        # query db to insert into users

        query = """INSERT INTO users (first_name, last_name, email, password)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"""

        # hash the password and wrap it in a dictionary 
        hashed_pw = BCRYPT.generate_password_hash(form["password"])
        data = {
            **form,
            "password": hashed_pw
        }

        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_one(cls, data):
        # query to db to select one user by id

        query = "SELECT * FROM users WHERE id = %(id)s"

        results = connectToMySQL(DATABASE).query_db(query, data)

        return cls(results[0])


    @classmethod
    def get_one_by_email(cls, data):
        # query the db to select a user by email

        query = "SELECT * FROM users WHERE email = %(email)s"

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])

        return False

    @classmethod
    def validate_login(cls,data):
        # method to validate a login based off the email and hashed password

        # returns false if it failed or an instance of the user if it logged in successfully
        
        found_user = cls.get_one_by_email(data)

        if not found_user:
            flash("Email/Password not valid", "login")
            return False

        if not BCRYPT.check_password_hash(found_user.password,data["password"]):
            flash("Email/Password not valid", "login")
            return False

        return found_user


    @staticmethod
    def validate_new(data):
        # method to validate a new user

        is_valid = True

        # check if first_name matches NAME_REGEX
        if not NAME_REGEX.match(data["first_name"]):
            is_valid = False
            flash("First name must be only letters and atleast 2 characters.", "register")

        # check if last_name matches NAME_REGEX
        if not NAME_REGEX.match(data["last_name"]):
            is_valid = False
            flash("Last name must be only letters and atleast 2 characters.", "register")

        # check if email matches EMAIL_REGEX
        if not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash("Email must be a valid email address.", "register")

        # check if email already exists in the db
        if User.get_one_by_email(data):
            is_valid = False
            flash("This email is already taken.", "register")

        # check that password matches confirm_password
        if data["password"] != data["confirm_password"]:
            is_valid = False
            flash("The password and the comfirmed password must match.", "register")

        return is_valid
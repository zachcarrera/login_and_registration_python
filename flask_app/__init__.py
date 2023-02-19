from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = "password"

# constant for database name
DATABASE = "login_and_reg_schema"

# constant instance of Bcrypt
BCRYPT = Bcrypt(app)
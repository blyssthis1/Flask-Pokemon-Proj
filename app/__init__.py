from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config.from_object(Config)
db =SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

login.login_view= 'signin'
login.login_message= 'Make sure you log in'


from app import routes, models
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cassa.db'
app.config['SECRET_KEY'] = 'd09945c0c13fe1d13346a26a'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from cassa import routes

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mongoalchemy import MongoAlchemy
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mdb = MongoAlchemy(app)
db.Model.metadata.reflect(db.engine)

from app import views, mongo_models, models

from app import app
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

dbName=os.environ.get('DB_NAME')
dbHost=os.environ.get('DB_HOST')
dbUser=os.environ.get('DB_USER')
dbPassword=os.environ.get('DB_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{dbUser}:{dbPassword}@{dbHost}/{dbName}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config['SQLALCHEMY_POOL_PRE_PING'] = True

db = SQLAlchemy(app)
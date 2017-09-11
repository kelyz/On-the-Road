#!venv/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql9187477:WJtv7YWDce@sql9.freemysqlhosting.net/sql9187477'
# db = SQLAlchemy(app)

from app import views, models
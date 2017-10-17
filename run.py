from app import app
import os

app.secret_key = os.environ['app.secret_key']
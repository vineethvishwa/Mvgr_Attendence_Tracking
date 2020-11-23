
import os
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xjvdssytgwcteq:bc260046057550ec187f97fa96658b388508032d1092db9d367b6c955dec636b@ec2-54-221-198-156.compute-1.amazonaws.com:5432/d7qv2gdhp1aaef'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()

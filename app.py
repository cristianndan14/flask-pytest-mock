from datetime import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql_db:3306/db_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "date_posted": self.date_posted,
            "content": self.content,
            "user_id": self.user_id
        }
    

@app.route("/", methods=["GET"])
@app.route("/alive", methods=["GET"])
def alive():
    try:
        return jsonify(
            {
                "message": "api is alive",
                "code": 200,
                "data": [],
            }
        ), 200
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

@app.route("/users", methods=["GET"])
def users_list():
    try:
        users = User.query.all()
        users_data = [user.to_json() for user in users]
        response = {
            "code": 200,
            "data": users_data,
            "message": "datos solicitados exitosamente."
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({ "error": str(e) }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
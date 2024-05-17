from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
 

app = Flask(__name__)

app.config.from_object("config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/", methods=["GET"])
@app.route("/alive", methods=["GET"])
def alive():
    data = {
        "message": "api is alive",
        "code": 200,
        "data": [],
    }
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True)
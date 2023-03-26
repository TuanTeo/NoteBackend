import pymysql

import user_controller
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
# from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/user/add', methods=['POST'])
def add_user():
    return user_controller.add(request)


@app.route('/users')
def users():
    return user_controller.get_all_user()


@app.route('/user/<int:id>')
def user(id):
    return user_controller.get_user_by_id(id)


@app.route('/user/update', methods=['POST'])
def update_user():
    return user_controller.update_user(request)


@app.route('/user/delete/<int:id>')
def delete_user(id):
    return user_controller.delete_user_by_id(id)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


# flask --app main.py --debug run
if __name__ == "__main__":
    app.run()
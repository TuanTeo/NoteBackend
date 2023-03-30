import pymysql
from flask import jsonify, make_response
# from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, timezone

from app import app
import main
from db_config import mysql


def add(request):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                _json = request.json
                _name = _json['user_name']
                _email = _json['user_email']
                _password = _json['user_password']
                # validate the received values
                if _name and _email and _password and request.method == 'POST':
                    # do not save password as a plain text
                    _hashed_password = generate_password_hash(_password)
                    # save edits
                    sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
                    data = (_name, _email, _hashed_password,)
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql, data)
                    conn.commit()
                    resp = jsonify('User added successfully!')
                    resp.status_code = 200
                    return resp
                else:
                    return main.not_found()
            except Exception as e:
                print(e)
                return main.not_found()
            finally:
                cursor.close()
                conn.close()
    except Exception as e:
        return make_response('Invalid token')


def get_all_user(request):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT * FROM tbl_user")
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                return resp
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

        else:
            return make_response('Missing token')
    except Exception as e:
        return make_response('Invalid token')


def get_user_by_id(request, id):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
                row = cursor.fetchone()
                resp = jsonify(row)
                resp.status_code = 200
                return resp
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
    except Exception as e:
        return make_response('Invalid token')


def update_user(request):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                _json = request.json
                _id = _json['user_id']
                _name = _json['user_name']
                _email = _json['user_email']
                _password = _json['user_password']
                # validate the received values
                if _name and _email and _password and _id and request.method == 'POST':
                    # do not save password as a plain text
                    _hashed_password = generate_password_hash(_password)
                    # save edits
                    sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
                    data = (_name, _email, _hashed_password, _id,)
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql, data)
                    conn.commit()
                    resp = jsonify('User updated successfully!')
                    resp.status_code = 200
                    return resp
                else:
                    return main.not_found()
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
    except Exception as e:
        return make_response('Invalid token')


def delete_user_by_id(request, id):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
                conn.commit()
                resp = jsonify('User deleted successfully!')
                resp.status_code = 200
                return resp
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
    except Exception as e:
        return make_response('Invalid token')


def login(request):
    try:
        print('SECRET_KEY = ', app.config['SECRET_KEY'])
        _json = request.json
        _name = _json['user_name']
        _password = _json['user_password']
        # validate the received values
        if _name and _password and request.method == 'POST':
            _hashed_password = generate_password_hash(_password)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM tbl_user WHERE user_name=%s", _name)
            row = cursor.fetchone()
            if check_password_hash(row['user_password'], _password):
                # Sinh token jwt
                token = jwt.encode({'user_name': _name, 'user_id': row['user_id']}, app.config['SECRET_KEY'])
                resp = jsonify({'token': token})
                resp.status_code = 200
                return resp
            else:
                return make_response('Could not verify')
    except Exception as e:
        print(e)
        return make_response('Error when verify')
    finally:
        cursor.close()
        conn.close()

import ast
import random

import pymysql
from flask import jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app
import main
from db_config import mysql
from utils.secretUtils import verifyProof


def add(request):
    # try:
        # _token = request.headers['Token']
        # _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        # if _data:
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
    # except Exception as e:
    #     return make_response('Invalid token')


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
                resp = jsonify({'token': token, 'user_id': row['user_id']})
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

# tạo 1 db tbl_bimetric (user_id, username, sign (mã hash sinh trắc được mã hoá private key), public_key,
# token, token_proved (token đã mã hoá private key, biometric (mã hash của thông tin sinh trắc))
# Nếu token = decode(token_proved, public_key) && biometric == decode(sign, public_key) => Đúng
#
def request_login_biometric(request):
    try:
        _json = request.json
        _user_name = _json['user_name']
        _h = _json['h']
        _u = _json['u']

        # print('_name', _user_name)
        # print('_h', _h)
        # print('_u', _u)
        # validate the received values
        if _user_name and _h and _u and request.method == 'POST':
            # create random token
            c = random.getrandbits(128)
            # print('token', c)
            # update vào bảng tbl_biometric
            sql = "UPDATE tbl_biometric SET c=%s, h=%s, u=%s WHERE user_name=%s"
            data = (c, _h, _u, _user_name,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify(str(c))
            resp.status_code = 200
            return resp
    except Exception as e:
        print(e)
        return make_response('Error when request')
    finally:
        cursor.close()
        conn.close()


def verify_biometric(request):
    try:
        _json = request.json
        _user_name = _json['user_name']
        _z = _json['z']
        # print('_name', _user_name)
        # print('_z', _z)
        # validate the received values
        if _user_name and _z and request.method == 'POST':
            # Query tbl_biometric lấy ra public key, token, sign
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM tbl_biometric WHERE user_name=%s", _user_name)
            row = cursor.fetchone()

            if verifyProof(_z, row['public_key'], row['c'], row['h'], row['u'], row['g']):
                # Sinh token jwt
                cursor.execute("SELECT * FROM tbl_user WHERE user_name=%s", _user_name)
                user_row = cursor.fetchone()
                token = jwt.encode({'user_name': _user_name, 'user_id': user_row['user_id']}, app.config['SECRET_KEY'])
                resp = jsonify({'token': token, 'user_id': user_row['user_id']})
                resp.status_code = 200
                return resp
            else:
                resp = jsonify("Cant verify!")
                resp.status_code = 200
                return resp
    except Exception as e:
        print(e)
        return make_response('Error when request')
    finally:
        cursor.close()
        conn.close()


# Insert public key vào tbl_biometric
def add_public_key(request):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                _json = request.json
                _user_name = _json['user_name']
                # _public_key = _json['public_key']
                # print('_name', _user_name)
                # print('_public_key', _public_key)
                # validate the received values
                if _user_name and request.method == 'POST':
                    # Check neu chua co thi Insert public key vào tbl_biometric
                    # Neu co roi thi update lai public_key moi

                    # Tạo public key và g0
                    _public_key = random.getrandbits(128)
                    _gen = random.getrandbits(64)

                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    cursor.execute("SELECT * FROM tbl_biometric WHERE user_name=%s", _user_name)
                    row = cursor.fetchone()
                    if row is None:
                        # Chua co thong tin
                        sql = "INSERT INTO tbl_biometric(user_name, public_key, g) VALUES(%s, %s)"
                        data = (_user_name, _public_key, _gen)
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sql, data)
                        conn.commit()
                    else:
                        sql = "UPDATE tbl_biometric SET public_key=%s, g=%s WHERE user_name=%s"
                        data = (_public_key, _gen, _user_name,)
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sql, data)
                        conn.commit()
                    resp = jsonify({'public_key': str(_public_key), 'g': str(_gen)})
                    resp.status_code = 200
                    return resp
            except Exception as e:
                print(e)
                return make_response('Failed!')
            finally:
                cursor.close()
                conn.close()
    except Exception as e:
        return make_response('Invalid token')
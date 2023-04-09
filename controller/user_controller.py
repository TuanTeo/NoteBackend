import ast
import random

import pymysql
from flask import jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app
import main
from db_config import mysql
from utils.secretUtils import verifyMessage


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

# tạo 1 db tbl_bimetric (user_id, username, sign (mã hash sinh trắc được mã hoá private key), public_key,
# token, token_proved (token đã mã hoá private key, biometric (mã hash của thông tin sinh trắc))
# Nếu token = decode(token_proved, public_key) && biometric == decode(sign, public_key) => Đúng
#
def request_login_biometric(request):
    try:
        _json = request.json
        _user_name = _json['user_name']
        _sign = _json['sign']
        # print('_name', _user_name)
        # print('_sign', _sign)
        # validate the received values
        if _user_name and request.method == 'POST':
            # create random token
            token = random.getrandbits(128)
            # print('token', token)
            # update vào bảng tbl_biometric
            sql = "UPDATE tbl_biometric SET sign=%s, token=%s WHERE user_name=%s"
            data = (_sign, token, _user_name,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify(token)
            resp.status_code = 200
            return resp
    except Exception as e:
        print(e)
        return make_response('Error when request')
    # finally:
        # cursor.close()
        # conn.close()


def verify_biometric(request):
    public_key = '''-----BEGIN RSA PUBLIC KEY-----
    MIICCgKCAgEAx34PulvPVGweDo1jbaKZ7+NbcpgqX+0spzpkZayPxM71HU70MUVr
    y60fjtkqFwbwASufzqRbHsYNX/DvbuyiYiJRFMx9RZspKXW70trEuygmrMPe8fea
    n68jy/WMRh/Kk4H6z44GnmGpPA24NVRsqAClcxmk5ljsg65vXaqLxWgepdKmK8Fy
    K9FhslShXljxNEAZnhr0GgvrEiqpNn+oLqhMvAiWF3KQI2WEwQ9MjMFYAvLPTSIJ
    EdU0zLUo1pakmLpjRT+OzDUnzZkBqGtgcUVoRmjWQwoVZJpvHBf3yVZgQ99u1JmD
    qG69mnOSRM/ywA58jeZrtT6yPwYCHwFEXIdQ4dnoYUbaAhxNv0WB2jAIUWZyRyp5
    rl5OfE+f6eaG/TSsvM/J47muocyYWi0OjqrYbccLVxvZn8cqNHv5m8rr6wylZVPQ
    bzG4xR2yA9iBxd2MYMDFC2ioATXiaN0LiF5z5MN6SwjXt7fehBzNSwecSAQ8ke1F
    vP0kRoJKBMOqjtwd2cZAjjwuYe+QebpCEo5wSbu8tFGIa+nupfhhO/VDvtDeyQY0
    Ei2uNGJGwP4YXdINepgej08jXeiaHritpYKMqF1ka5VGdZ5SrQP1FgWjWwaCzjsw
    Ixi/xM857G5L1RHJtS3rbklSUxDrWM1ycQ7unQCZBbltPP5oFJxKvzECAwEAAQ==
    -----END RSA PUBLIC KEY-----
    '''
    message = 'df60C2KhhGwaxVRf+DjMy6EopJwRNNpzlOeYNUfu4O1jYkl2Zs97HGHYeGHqMB7t6BMTKl4vPAx2OOAIL6z6zRYXaokQk7k75L96xswCvuDHVo+sS/kSuGX7K4ss6PEzJLC0BBnbVuq5MlkTbg+HKixr5Mxs64yBRI/AJa6hl+UNhXZjirLSLDZIJYA26j4k+BfOX4NPZXFId313nawKzHoldkCcM+nx0g5AVM5vNSeYXF5NNVHtEutHv3aichC3udjQDjcBnTgtNKh++e0prl42/l9hxMK2iZEKonVOlJMUaAQ6XcBB3HcuIlLevhpb64YkS3oZGlkATJ9g9wVX9Q=='

    signature = '''ZyySrT0OC+e9EPx+PFUTlo+rxjCO8siXP5on+sWTlYBwydZiQ73dU/tiOR7bxDECX0iuQm00vwEJ
    5T4uxViSL48qSl/BN/S+oKOrosfYAx6w05y0HXrYY0AkAONK7NbFOBuYRU+gWDF9L7qJg/dlnmUj
    6IoTA3JCN2zbzMTgfy0Ev7vVuM0XRiYU+apClRM2IgEgXhBMSfCc/GaAAyeH5j61DhoG2Dv8X4G6
    g48kOyeLFTbQ6Opj71Nx5f35h5ItYS64Kr6i94XqUjodLCyTMBQlZOANLlqglr9VsEgIvQCmO2ML
    TxPqh3LPv4189SlneKIWgoPdU49p/eGC2Pv0vi0I5MOOyhUJIw/2KwE7t5a34KiVySJgWTlLZQ9l
    IJtLLokfgcZuer+X6wzwWTuBQ6RtP7pP4lRjDfYsVu3kzQbPHyZkWnPAp3GIW2TZ5IIwtJm4eNYw
    KYLgT/1Nio0tp/4GSanbd/ncBHWFuKFgfX5i2uuizHOpF40zwkEM6C6db93FmNANt3VnsCJDPv8Z
    vh5BhWgImlx5t5XzFDplKT8tssvQm6V+lZiwhqtMxPThwzpcX1ioxLI4L8SunFhkUP05iPqc+p8A
    aROdsixJ+AIp1FamF9va58Ald5zIDABuyxjO4Jk9rD+3fJ6W7ER3po6fh2lYNxMuAXGE0WHyNU4='''

    try:
        _json = request.json
        _user_name = _json['user_name']
        _token_proved = _json['token_proved']
        _biometric = _json['biometric']
        print('_name', _user_name)
        print('_token_proved', _token_proved)
        print('_biometric', _biometric)
        # validate the received values
        if _user_name and _token_proved and _biometric and request.method == 'POST':
            # Query tbl_biometric lấy ra public key, token, sign
            # load public key
            if verifyMessage(message, signature, public_key):
                # Check token == token_decode and biometric == sign => trả về token jwt và đăng nhập thành công
                resp = jsonify("Verify Complete!")
                resp.status_code = 200
                return resp
            else:
                # Check token == token_decode and biometric == sign => trả về token jwt và đăng nhập thành công
                resp = jsonify("Cant verify!")
                resp.status_code = 400
                return resp
    except Exception as e:
        print(e)
        return make_response('Error when request')
    # finally:
        # cursor.close()
        # conn.close()


# Insert public key vào tbl_biometric
def add_public_key(request):
    try:
        _json = request.json
        _user_name = _json['user_name']
        _token_proved = _json['token_proved']
        _biometric = _json['biometric']
        print('_name', _name)
        print('_token_proved', _token_proved)
        print('_biometric', _biometric)
        # validate the received values
        if _name and _token_proved and _biometric and request.method == 'POST':
            # Query tbl_biometric lấy ra public key, token, sign


            # decode _biometric và _token_proved bằng public key
            # Chuẩn mã hoá, giải mã public key RSA 4096
            decryptor = PKCS1_OAEP.new(public_key)
            token_decode = decryptor.decrypt(ast.literal_eval(str(_token_proved)))
            biometric = decryptor.decrypt(ast.literal_eval(str(_biometric)))

            # Check token == token_decode and biometric == sign => trả về token jwt và đăng nhập thành công

            resp.status_code = 200
            return resp
    except Exception as e:
        print(e)
        return make_response('Error when request')
    # finally:
        # cursor.close()
        # conn.close()
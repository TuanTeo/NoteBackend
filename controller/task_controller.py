import pymysql

import main
from app import app
from db_config import mysql
from flask import jsonify, make_response
from flask import flash, request
# from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app


# Thêm task mới
def add(request):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                _json = request.json
                _title = _json['title']
                _pin = _json['pin_enable']
                _user_id = _json['user_id']
                # validate the received values
                if _title and _user_id and request.method == 'POST':
                    # save edits
                    sql = "INSERT INTO tbl_task(title, pin_enable, user_id) VALUES(%s, %s, %s)"
                    data = (_title, _pin, _user_id,)
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql, data)
                    conn.commit()
                    resp = jsonify('Task added successfully!')
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


# Danh sách task theo user_id -> Trả về luôn danh sách detail
def get_task_by_user_id(request, id):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT * FROM tbl_task WHERE user_id=%s", id)
                rows = cursor.fetchall()
                resp = jsonify(rows)
                resp.status_code = 200
                return resp
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
    except Exception as e:
        return make_response('Invalid token')

# Cập nhật lại task
def update_task(request):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                _json = request.json
                _id = _json['task_id']
                _title = _json['title']
                _pin = _json['pin_enable']
                _isDelete = _json['is_deleted']
                _isArchive = _json['is_archived']
                # validate the received values
                if (_title or _pin or _isDelete or _isArchive or _id) and request.method == 'POST':
                    # save edits
                    sql = "UPDATE tbl_task SET title=%s, pin_enable=%s, is_deleted=%s, is_archived=%s WHERE task_id=%s"
                    data = (_title, _pin, _isDelete, _isArchive, _id,)
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql, data)
                    conn.commit()
                    resp = jsonify('Task updated successfully!')
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


# Xoá task theo id
def delete_task_by_id(request, id):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tbl_task WHERE task_id=%s", (id,))
                conn.commit()
                resp = jsonify('Task deleted successfully!')
                resp.status_code = 200
                return resp
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
    except Exception as e:
        return make_response('Invalid token')
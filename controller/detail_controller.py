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


# Thêm detail mới
def add(request):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                _json = request.json
                _content = _json['content']
                _files = _json['files']
                _task_id = _json['task_id']
                # validate the received values
                if _content and _task_id and request.method == 'POST':
                    # save edits
                    sql = "INSERT INTO tbl_detail(content, files, task_id) VALUES(%s, %s, %s)"
                    data = (_content, _files, _task_id,)
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql, data)
                    conn.commit()
                    resp = jsonify({'detail_id': cursor.lastrowid})
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


# Danh sách detail
def get_detail_by_task_id(request, id):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT * FROM tbl_detail WHERE task_id=%s", id)
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


# Cập nhật lại detail
def update_detail(request):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                _json = request.json
                _id = _json['detail_id']
                _content = _json['content']
                _isDone = _json['is_done']
                _files = _json['files']
                _isDelete = _json['is_deleted']
                # validate the received values
                if (_content or _isDone or _isDelete or _files or _id) and request.method == 'POST':
                    # save edits
                    sql = "UPDATE tbl_detail SET content=%s, is_done=%s, is_deleted=%s, files=%s WHERE detail_id=%s"
                    data = (_content, _isDone, _isDelete, _files, _id,)
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql, data)
                    conn.commit()
                    resp = jsonify('Detail updated successfully!')
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


# Xoá detail theo id
def delete_detail_by_id(request, id):
    try:
        _token = request.headers['Token']
        _data = jwt.decode(_token, app.config['SECRET_KEY'], "HS256")
        if _data:
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tbl_detail WHERE detail_id=%s", (id,))
                conn.commit()
                resp = jsonify('Detail deleted successfully!')
                resp.status_code = 200
                return resp
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
    except Exception as e:
        return make_response('Invalid token')
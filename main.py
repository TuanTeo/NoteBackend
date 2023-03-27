from controller import user_controller, task_controller, detail_controller
from app import app
from flask import jsonify
from flask import request


# from werkzeug import generate_password_hash, check_password_hash


# ----------------- User API ------------------
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


# ----------------- Task API ------------------
@app.route('/task/add', methods=['POST'])
def add_task():
    return task_controller.add(request)


@app.route('/task/<int:id>')
def get_task_by_user_id(id):
    return task_controller.get_task_by_user_id(id)


@app.route('/task/update', methods=['POST'])
def update_task():
    return task_controller.update_task(request)


@app.route('/task/delete/<int:id>')
def delete_task(id):
    return task_controller.delete_task_by_id(id)


# ----------------- Detail API ------------------
@app.route('/detail/add', methods=['POST'])
def add_detail():
    return detail_controller.add(request)


@app.route('/detail/<int:id>')
def get_detail_by_task_id(id):
    return detail_controller.get_detail_by_task_id(id)


@app.route('/detail/update', methods=['POST'])
def update_detail():
    return detail_controller.update_detail(request)


@app.route('/detail/delete/<int:id>')
def delete_detail(id):
    return detail_controller.delete_detail_by_id(id)


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
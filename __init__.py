from app_config import app, db
from flask import render_template, request
from model.employee import employee
import json


@app.route('/')
def index():
    return


@app.route('/check_login/')
def check_login():
    phone_num = request.args['phone']
    password = request.args['password']
    user = employee.query.filter_by(phone=phone_num).first()
    if user != None and user.check(password):
        dic = user.to_json()
        dic['token'] = user.token
        return json.dumps(dic)
    else:
        return json.dumps({'error_code': '403', 'error_result': '账号不存在或密码错误,请重试'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

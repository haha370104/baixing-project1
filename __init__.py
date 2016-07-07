from app_config import app, db
from flask import render_template, request
from model.employee import employee
import json


@app.route('/')
def index():
    return


@app.route('/check_login/', methods=['GET', 'POST'])
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


@app.route('/add_staff/', methods=['GET', 'POST'])
def add_staff():
    name = request.args['name']
    phone = request.args['phone']
    f_department = request.args['f_department']
    position_title = request.args['position_title']
    authority_level = request.args['authority_level']
    position_level = request.args['position_level']
    emergency_phone = request.args.get('emergency_phone')
    s_department = request.args.get('s_department')
    address = request.args.get('address')
    manager_ID = request.args.get('manager_ID')
    user = employee(name, phone, f_department, position_title, authority_level, position_level, '000000', emergency_phone,
                    s_department, address, manager_ID)
    db.session.add(user)
    db.session.commit()
    return json.dumps({'result': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

from app_config import app, db
from flask import render_template, request, make_response
import json
import time
from controller.filter import *


@app.before_request
def check_authority():
    path = request.path
    if path in filter_list.keys():
        for fun in filter_list[path]:
            response = fun(request)
            if response != None:
                return response
        return None


@app.route('/')
def index():
    return '吼啊'


@app.route('/login/')
def login():
    return '江主席,你说先登陆,吼不吼啊'


@app.route('/check_login/', methods=['GET', 'POST'])
def check_login():
    phone_num = request.args['phone']
    password = request.args['password']
    user = employee.query.filter_by(phone=phone_num).first()
    if user != None and user.check(password):
        dic = user.to_json()
        dic['token'] = user.token
        res = make_response(json.dumps(dic))
        res.set_cookie('token', user.token, expires=time.time() + 24 * 60 * 60)
        session['token'] = user.token
        return res
    else:
        return json.dumps({'error_code': 404, 'error_result': '账号不存在或密码错误,请重试'})


@app.route('/add_staff/', methods=['GET', 'POST'])
def add_staff():
    try:
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
        user = employee(name, phone, f_department, position_title, authority_level, position_level, '000000',
                        emergency_phone,
                        s_department, address, manager_ID)
        db.session.add(user)
        db.session.commit()
    except:
        return json.dumps({'result': 'fail'})
    return json.dumps({'result': 'success'})


@app.route('/show_staff/')
def show_staff():
    staffs = employee.query.filter_by(s_department=request.args['s_department']).all()
    result = []
    for staff in staffs:
        result.append(staff.to_json())
    return json.dumps({'result': result})


@app.route('/show_team_staff/', methods=['GET'])
def show_team_staff():
    staffs = employee.query.filter_by(f_department=request.args['f_department']).all()
    result = []
    for staff in staffs:
        result.append(staff.to_json())
    return json.dumps({'result': result})


@app.route('/show_department_staff/')
def show_department_staff():
    staffs = employee.query.all()
    result = []
    for staff in staffs:
        result.append(staff.to_json())
    return json.dumps({'result': result})


@app.route('/edit_staff/', methods=['POST'])
def edit_staff():
    edited_staff = employee.query.filter_by(ID=request.args['ID']).first()
    if (edited_staff == None):
        return json.dumps({'result': 'No such a staff with posted ID'})
    detail = json.loads(request.args['detail'])
    attrs = list(detail.keys())
    values = list(detail.values())
    for i in range(len(attrs)):
        setattr(edited_staff, attrs[i], values[i])
    db.session.add(edited_staff)
    db.session.commit()
    return json.dumps({'result': 'update success'})


@app.route('/delete_staff/', methods=['POST'])
def delete_staff():
    deleted_staff = employee.query.filter_by(ID=request.args['ID']).first()
    if (deleted_staff == None):
        return json.dumps({'result': 'No such a staff with posted ID'})
    deleted_staff.delete()
    db.session.commit()
    return json.dumps({'result': 'delete success'})


@app.route('/edit_profile/', methods=['POST'])
def edit_profile():
    return edit_staff()


@app.route('/change_password/', methods=['POST'])
def change_password():
    user = employee.query.filter_by(ID=request.args['ID']).first()
    user.paswswd = request.args['password']
    db.session.delete(user)
    db.session.commit()
    return json.dumps({'result': 'change password success'})


@app.route('/logout/')
def logout():
    res = make_response(json.dumps({'result': 'success'}))
    res.set_cookie('token', '')
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

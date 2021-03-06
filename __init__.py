from app_config import app, db
from flask import render_template, request, make_response
import json
from sqlalchemy import and_, not_
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
    return render_template('index.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/check_login/', methods=['GET', 'POST'])
def check_login():
    phone_num = request.values['phone']
    password = request.values['password']
    user = employee.query.filter(and_(employee.phone == phone_num, not_(employee.delete_flag))).first()
    if user != None and user.check(password):
        dic = user.to_json()
        dic['token'] = user.token
        res = make_response(json.dumps(dic))
        res.set_cookie('token', user.token, expires=time.time() + 24 * 60 * 60)
        res.set_cookie('authority_level', str(user.authority_level), expires=time.time() + 24 * 60 * 60)
        session['token'] = user.token
        return res
    else:
        return json.dumps({'error_code': 404, 'error_reason': '账号不存在或密码错误,请重试'})


@app.route('/add_staff/', methods=['GET', 'POST'])
def add_staff():
    try:
        name = request.values['name']
        phone = request.values['phone']
        f_department = request.values['f_department']
        position_title = request.values['position_title']
        authority_level = request.values['authority_level']
        position_level = request.values['position_level']
        emergency_phone = request.values.get('emergency_phone')
        s_department = request.values.get('s_department')
        address = request.values.get('address')
        manager_ID = request.values.get('manager_ID')
        user = employee(name, phone, f_department, position_title, authority_level, position_level, '000000',
                        emergency_phone,
                        s_department, address, manager_ID)
        db.session.add(user)
        db.session.commit()
    except:
        return json.dumps({'result': 'fail'})
    return json.dumps({'result': 'success'})


@app.route('/show_team_staff/', methods=['GET'])
def show_team_staff():
    staffs = employee.query.filter(and_(employee.f_department == request.values['f_department'],
                                        employee.s_department == request.values[
                                            's_department']), not_(employee.delete_flag)).all()
    result = []
    for staff in staffs:
        result.append(staff.to_json())
    return json.dumps({'result': result})


@app.route('/show_staff/')
def show_staff():
    staffs = employee.query.filter(
        and_(employee.f_department == request.values['f_department'], not_(employee.delete_flag))).all()
    result = []
    for staff in staffs:
        result.append(staff.to_json())
    return json.dumps({'result': result})


@app.route('/show_department_staff/<int:start>/<int:size>/')
def show_department_staff(start, size):
    staffs = employee.query.filter_by(delete_flag=False).offset(start - 1).limit(size)
    result = []
    for staff in staffs:
        result.append(staff.to_json())
    return json.dumps({'result': result})


@app.route('/edit_staff/', methods=['POST'])
def edit_staff():
    edited_staff = employee.query.filter_by(ID=request.values['ID']).first()
    if (edited_staff == None):
        return json.dumps({'result': 'No such a staff with posted ID'})
    detail = json.loads(request.values['detail'])
    for key in detail.keys():
        setattr(edited_staff, key, detail[key])
    db.session.commit()
    return json.dumps({'result': 'update success'})


@app.route('/delete_staff/', methods=['POST'])
def delete_staff():
    deleted_staff = employee.query.filter_by(ID=request.values['ID']).first()
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
    user = employee.query.filter_by(ID=request.values['ID']).first()
    if user != None:
        user.change_pwd(request.values['password'])
        db.session.commit()
        return json.dumps({'result': 'change password success'})
    else:
        return json.dumps({'result': 'No such a staff with posted ID'})


@app.route('/logout/')
def logout():
    res = make_response(json.dumps({'result': 'success'}))
    res.set_cookie('token', '')
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

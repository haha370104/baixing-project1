from flask import redirect, session, url_for
from model.employee import employee
from sqlalchemy import and_,not_
import json


def get_staff_by_token(request):
    token = request.cookies.get('token')
    if token != None:
        user = employee.query.filter(and_(employee.token == token, not_(employee.delete_flag))).first()
        return user
    else:
        return None


def login_again_filter(request):
    token = request.cookies.get('token')
    if token != None and token == session.get('token'):
        return redirect(url_for('index'))
    elif token != None:
        user = employee.query.filter(and_(employee.token == token, not_(employee.delete_flag))).first()
        if user != None:
            session['token'] = user.token
            dic = user.to_json()
            dic['token'] = user.token
            return redirect(url_for('index'))


def login_filter(request):
    user = get_staff_by_token(request)
    if user == None:
        return redirect(url_for('login'))


def read_controll(request):
    user = get_staff_by_token(request)
    authority_level = user.authority_level
    if authority_level == 0 and (request.args.get('f_department') != user.f_department or request.args.get(
            's_department') != user.s_department):
        return json.dumps({'error_reason': 'permission denied', 'error_code': 403})
    if authority_level == 1 and request.args.get('f_department') != user.f_department:
        return json.dumps({'error_reason': 'permission denied', 'error_code': 403})


def change_controll(request):
    user = get_staff_by_token(request)
    authority_level = user.authority_level
    if authority_level != 3:
        return json.dumps({'error_reason': 'permission denied', 'error_code': 403})


def change_self(request):
    user = get_staff_by_token(request)
    if user.ID != request.args.get('ID'):
        return json.dumps({'error_reason': 'permission denied', 'error_code': 403})


filter_list = {
    '/': [login_filter],
    '/logout/': [login_filter],
    '/check_login/': [login_again_filter],
    '/login/': [login_again_filter],
    '/show_staff/': [login_filter, read_controll],
    '/show_team_staff/': [login_filter, read_controll],
    '/show_department_staff/': [login_filter, read_controll],
    '/add_staff/': [login_filter, change_controll],
    '/edit_staff/': [login_filter, change_controll],
    '/delete_staff/': [login_filter, change_controll],
    '/change_password/': [login_filter, change_self],
    '/edit_profile/': [login_filter, change_self]
}

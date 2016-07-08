from . import db
import hashlib
from tools.security import get_salt
import time
import json


class employee(db.Model):
    __tablename__ = 'employee'
    ID = db.Column('ID', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    employee_name = db.Column('employee_name', db.String(10), nullable=False)
    phone = db.Column('phone', db.String(11), nullable=False, unique=True)
    emergency_phone = db.Column('emergency_phone', db.String(11), default=None)
    f_department = db.Column('f_department', db.String(40), nullable=False)
    s_department = db.Column('s_department', db.String(40), default=None)
    position_title = db.Column('position_title', db.String(30), nullable=False)
    authority_level = db.Column('authority_level', db.Integer, nullable=False, default=0)
    position_level = db.Column('position_level', db.String(40), nullable=False)
    address = db.Column('address', db.String(200), default=None)
    manager_ID = db.Column('manager_ID', db.Integer)
    entry_date = db.Column('entry_date', db.Date, nullable=False)
    delete_flag = db.Column('delete_flag', db.Boolean, nullable=False, default=False)
    delete_date = db.Column('delete_date', db.Date, default=None)
    passwd = db.Column('passwd', db.String(35), nullable=False)
    salt = db.Column('salt', db.String(16), nullable=False)
    token = db.Column('token', db.String(32), default=None)

    def check(self, password):
        password = hashlib.md5((password + self.salt).encode('ascii')).hexdigest()
        if password == self.passwd and not self.delete_flag:
            self.token = get_salt(32)
            db.session.commit()
            return True
        else:
            return False

    def __init__(self, name, phone, f_department, position_title, authority_level, position_level, passwd,
                 emergency_phone=None, s_department=None, address=None, manager_ID=None):
        self.employee_name = name
        self.phone = phone
        self.f_department = f_department
        self.position_title = position_title
        self.authority_level = authority_level
        self.position_level = position_level
        self.salt = get_salt(16)
        self.passwd = hashlib.md5((passwd + self.salt).encode('ascii')).hexdigest()
        self.emergency_phone = emergency_phone
        self.s_department = s_department
        self.address = address
        self.manager_ID = manager_ID
        self.entry_date = time.localtime()

    def delete(self):
        self.delete_flag = True
        self.delete_date = time.localtime()

    def to_json(self):
        dic = {}
        dic['ID'] = self.ID
        dic['employee_name'] = self.employee_name
        dic['phone'] = self.phone
        dic['emergency_phone'] = self.emergency_phone
        dic['f_department'] = self.f_department
        dic['s_department'] = self.s_department
        dic['position_title'] = self.position_title
        dic['position_level'] = self.position_level
        dic['authority_level'] = self.authority_level
        dic['address'] = self.address
        dic['manager_ID'] = self.manager_ID
        dic['entry_date'] = str(self.entry_date)

        for key in dic.keys():
            if dic[key] == None:
                dic[key] = ''
        return dic

    def change_pwd(self, passwd):
        self.passwd = hashlib.md5((passwd + self.salt).encode('ascii')).hexdigest()

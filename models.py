from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EmployeeModel(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    nik = db.Column(db.String(80))
    address = db.Column(db.String())
    jk = db.Column(db.String())
    hp = db.Column(db.Integer())
    tgl_lahir = db.Column(db.String())

    def __init__(self, employee_id, name, age, nik, address, jk, hp, tgl_lahir):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.nik = nik
        self.address = address
        self.jk = jk
        self.hp = hp
        self.tgl_lahir = tgl_lahir


    # def __repr__(self):
    #     return f"{self.employee_id}"
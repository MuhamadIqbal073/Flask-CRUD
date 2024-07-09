from flask import Flask, render_template, request, redirect, abort
from models import db, EmployeeModel
import os

app = Flask(__name__)

# Menentukan path file database SQLite
file_path = os.path.abspath(os.getcwd()) + "\\data.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

# Menginisialisasi database dengan konfigurasi Flask
db.init_app(app)

# Membuat tabel-tabel di database jika belum ada
with app.app_context():
    db.create_all()


# Route untuk membuat data karyawan baru
@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        # Mengambil data dari form
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        nik = request.form['nik']
        address = request.form['address']
        jk = request.form['jk']
        hp = request.form['hp']
        tgl_lahir = request.form['tgl_lahir']

        # Membuat objek EmployeeModel baru dan menyimpannya ke database
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, nik=nik, address=address, jk=jk, hp=hp, tgl_lahir=tgl_lahir)
        db.session.add(employee)
        db.session.commit()

        # Redirect ke halaman daftar karyawan
        return redirect('/data')


# Route untuk menampilkan daftar karyawan
@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    print(employees)  # Debugging: mencetak daftar karyawan di console
    return render_template('datalist.html', employees=employees)


# Route untuk menampilkan data detail seorang karyawan berdasarkan ID
@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee=employee)
    return f"Employee with id = {id} doesn't exist"


# Route untuk memperbarui data karyawan
@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            # Menghapus data karyawan yang lama
            db.session.delete(employee)
            db.session.commit()

            # Mengambil data baru dari form
            name = request.form['name']
            age = request.form['age']
            nik = request.form['nik']
            address = request.form['address']
            jk = request.form['jk']
            hp = request.form['hp']
            tgl_lahir = request.form['tgl_lahir']

            # Membuat objek EmployeeModel baru dengan data yang diperbarui
            employee = EmployeeModel(employee_id=id, name=name, age=age, nik=nik, address=address, jk=jk, hp=hp, tgl_lahir=tgl_lahir)
            db.session.add(employee)
            db.session.commit()

            # Redirect ke halaman detail karyawan yang diperbarui
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} doesn't exist"

    return render_template('update.html', employee=employee)


# Route untuk menghapus data karyawan
@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            # Menghapus data karyawan dari database
            db.session.delete(employee)
            db.session.commit()

            # Redirect ke halaman daftar karyawan
            return redirect('/data')
        abort(404)

    return render_template('delete.html')


if __name__ == "__main__":
    app.run(debug=True)

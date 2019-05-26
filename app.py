from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'flash_message'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bmsingh'
app.config['MYSQL_DB'] = 'student'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', student=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Inserted Successfully!")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student (name,email,phone) values (%s,%s,%s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        id_data = request.form['id']
        name_data = request.form['name']
        email_data = request.form['email']
        phone_data = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE student SET name=%s, email=%s, phone=%s WHERE id=%s",
                    (name_data, email_data, phone_data, id_data))

        flash("Updated Successfully!")

        mysql.connection.commit()
        return redirect(url_for("index"))


@app.route("/delete/<string:id_data>", methods=['GET', 'POST'])
def delete(id_data):
    flash("Deleted Successfully!")

    cur = mysql.connection.cursor()
    cur.execute("DELETE from student where id = %s", (id_data))
    mysql.connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

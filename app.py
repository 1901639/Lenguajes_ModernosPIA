from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1a.2b.3c,'
app.config['MYSQL_DB'] = 'to_do_app'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tasks SET title = %s, description = %s WHERE id = %s", (title, description, id))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('index'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    task = cur.fetchone()
    cur.close()
    return render_template('edit.html', task=task)

if __name__ == "__main__":
    app.run()
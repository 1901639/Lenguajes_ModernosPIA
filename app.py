from flask import Flask, render_template, request, redirect, url_for, jsonify
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
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'due_date')  # Orden por defecto: fecha límite

    cur = mysql.connection.cursor()

    # Construcción de la consulta SQL con filtro y ordenamiento
    query = "SELECT * FROM tasks WHERE title LIKE %s"
    params = [f"%{search_query}%"]

    if sort_by == 'priority':
        query += " ORDER BY FIELD(priority, 'Alta', 'Media', 'Baja')"
    else:
        query += " ORDER BY due_date"

    cur.execute(query, params)
    tasks = cur.fetchall()
    cur.close()

    return render_template('index.html', tasks=tasks, search_query=search_query, sort_by=sort_by)


@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    priority = request.form['priority']
    
    # Verificar si se ingresó una fecha límite
    due_date = due_date if due_date else None

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (title, description, due_date, priority) VALUES (%s, %s, %s, %s)", 
                (title, description, due_date, priority))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

@app.route('/complete/<int:id>', methods=['POST'])
def complete_task(id):
    data = request.get_json()
    completed = data.get('completed', False)  # Obtiene el estado de completado

    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET completed = %s WHERE id = %s", (completed, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'success': True})

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
        due_date = request.form['due_date']
        priority = request.form['priority']
        
        # Verificar si se ingresó una fecha límite
        due_date = due_date if due_date else None

        cur = mysql.connection.cursor()
        cur.execute("UPDATE tasks SET title = %s, description = %s, due_date = %s, priority = %s WHERE id = %s", 
                    (title, description, due_date, priority, id))
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
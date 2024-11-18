from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos MySQL
mydb = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', '1a.2b.3c,'),
    database=os.getenv('MYSQL_DATABASE', 'to_do_app')
    # host='localhost',
    # user='root',
    # password='1a.2b.3c,',
    # database='to_do_app'
)

table_created = False

@app.route('/')
def index():
    sort_by = request.args.get('sort', 'due_date')  # Por defecto, ordenar por fecha límite

    # Construir la consulta SQL según la opción de ordenamiento seleccionada
    if sort_by == 'due_date':
        # Ordenar por fecha límite, con las tareas sin fecha al final
        query = """
            SELECT * FROM tasks 
            ORDER BY 
                CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, 
                due_date ASC
        """
    elif sort_by == 'priority':
        # Ordenar por prioridad, y luego por fecha límite (las tareas sin fecha aparecen al final)
        query = """
            SELECT * FROM tasks 
            ORDER BY 
                CASE priority 
                    WHEN 'Alta' THEN 1 
                    WHEN 'Media' THEN 2 
                    WHEN 'Baja' THEN 3 
                END,
                CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, 
                due_date ASC
        """
    elif sort_by == 'alphabetical':
        # Ordenar alfabéticamente por el título de la tarea
        query = "SELECT * FROM tasks ORDER BY title ASC"
    else:
        # Valor predeterminado: ordenar por fecha límite
        query = """
            SELECT * FROM tasks 
            ORDER BY 
                CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, 
                due_date ASC
        """

    cur = mydb.cursor()
    cur.execute(query)
    tasks = cur.fetchall()
    cur.close()

    return render_template('index.html', tasks=tasks, sort_by=sort_by)


@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    priority = request.form['priority']
    
    # Verificar si se ingresó una fecha límite
    due_date = due_date if due_date else None

    cur = mydb.cursor()
    cur.execute("INSERT INTO tasks (title, description, due_date, priority) VALUES (%s, %s, %s, %s)", 
                (title, description, due_date, priority))
    mydb.commit()
    cur.close()

    return redirect(url_for('index'))

@app.route('/complete/<int:id>', methods=['POST'])
def complete_task(id):
    data = request.get_json()
    completed = data.get('completed', False)  # Obtiene el estado de completado

    cur = mydb.cursor()
    cur.execute("UPDATE tasks SET completed = %s WHERE id = %s", (completed, id))
    mydb.commit()
    cur.close()

    return jsonify({'success': True})

@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mydb.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    mydb.commit()
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

        cur = mydb.cursor()
        cur.execute("UPDATE tasks SET title = %s, description = %s, due_date = %s, priority = %s WHERE id = %s", 
                    (title, description, due_date, priority, id))
        mydb.commit()
        cur.close()

        return redirect(url_for('index'))
    
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    task = cur.fetchone()
    cur.close()
    return render_template('edit.html', task=task)

@app.before_request
def create_tables():
    global table_created
    if not table_created:
        with mydb.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    due_date DATE,
                    priority ENUM('Baja', 'Media', 'Alta') DEFAULT 'Media',
                    completed BOOLEAN DEFAULT FALSE
                );
            """)
            mydb.commit()
        table_created = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
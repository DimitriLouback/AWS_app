from flask import Flask, request, jsonify, render_template, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv


load_dotenv('config.env')

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host="db",
        port="5432"
    )
    return conn

# Rota principal 
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM mytable ORDER BY id;')
    pessoas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', pessoas=pessoas)

# adicionar uma nova pessoa
@app.route('/add', methods=['POST'])
def add_pessoa():
    nome = request.form['nome']
    idade = request.form['idade']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO mytable (name, age) VALUES (%s, %s)', (nome, idade))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index'))

#  editar uma pessoa
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_pessoa(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        cur.execute('UPDATE mytable SET name = %s, age = %s WHERE id = %s', (nome, idade, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    cur.execute('SELECT * FROM mytable WHERE id = %s', (id,))
    pessoa = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('edit.html', pessoa=pessoa)

# deletar uma pessoa
@app.route('/delete/<int:id>')
def delete_pessoa(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM mytable WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
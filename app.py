import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_unico TEXT,
            nombre_mascota TEXT,
            especie TEXT,
            nombre_dueno TEXT,
            telefono TEXT,
            direccion TEXT,
            observaciones TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        codigo_unico = request.form.get('codigo_unico')
        nombre_mascota = request.form.get('nombre_mascota')
        especie = request.form.get('especie')
        nombre_dueno = request.form.get('nombre_dueno')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        observaciones = request.form.get('observaciones')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mascotas (codigo_unico, nombre_mascota, especie, nombre_dueno, telefono, direccion, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (codigo_unico, nombre_mascota, especie, nombre_dueno, telefono, direccion, observaciones))
        conn.commit()
        conn.close()

        return redirect(url_for('exito', codigo=codigo_unico))

    return render_template('registrar.html')

@app.route('/exito/<code>')
def exito(codigo):
    return render_template('exito.html', codigo=codigo)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
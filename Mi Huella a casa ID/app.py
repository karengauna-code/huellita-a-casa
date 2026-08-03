from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random
import string
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_unico TEXT UNIQUE NOT NULL,
            nombre_mascota TEXT NOT NULL,
            especie TEXT NOT NULL,
            nombre_dueno TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT NOT NULL,
            info_medica TEXT,
            foto TEXT
        )
    ''')
    conn.commit()
    conn.close()

def generar_codigo():
    numeros = ''.join(random.choices(string.digits, k=4))
    return f"HCA-{numeros}"

# Ruta de la página de bienvenida (Explicación para el público)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta del formulario de registro
@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre_mascota = request.form['nombre_mascota']
    especie = request.form['especie']
    nombre_dueno = request.form['nombre_dueno']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    info_medica = request.form['info_medica']
    
    foto = request.files['foto']
    nombre_foto = ""
    if foto and foto.filename != '':
        nombre_foto = foto.filename
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_foto))

    codigo_unico = generar_codigo()
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO mascotas (codigo_unico, nombre_mascota, especie, nombre_dueno, telefono, direccion, info_medica, foto)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo_unico, nombre_mascota, especie, nombre_dueno, telefono, direccion, info_medica, nombre_foto))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()
        
    return render_template('exito.html', codigo=codigo_unico, mascota=nombre_mascota)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
# Versão que possibilita votar pela rede local, digitando o IP do computador que está rodando o 
# servidor Flask + a porta 5000 (exemplo: 192.168.0.7:5000) no smatphone ou outro computador da 
# mesma rede local. ou no computador mesmo, digitando localhost:5000
from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'segredo-super-seguro'

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL,
            turno TEXT NOT NULL,
            alunos TEXT NOT NULL,
            descricao TEXT NOT NULL,
            votos INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        turma = request.form['turma'].strip()
        turno = request.form['turno'].strip()
        descricao = request.form['descricao'].strip()
        alunos = [request.form.get(f'aluno{i}', '').strip() for i in range(1, 7)]

        if not nome or not turma or not descricao:
            flash('Nome, turma e descrição são obrigatórios.')
            return redirect('/cadastro')
        if any(aluno == '' for aluno in alunos[:4]):
            flash('Os 4 primeiros alunos são obrigatórios.')
            return redirect('/cadastro')

        alunos_str = ', '.join([aluno if aluno else '—' for aluno in alunos])

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projetos (nome, turma, turno, alunos, descricao)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, turma, turno, alunos_str, descricao))
        conn.commit()
        conn.close()
        flash('Projeto cadastrado com sucesso!')
        return redirect('/')
    return render_template('cadastro.html')

@app.route('/votar', methods=['GET', 'POST'])
def votar():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos')
    projetos = cursor.fetchall()

    if request.method == 'POST':
        nome_votante = request.form.get('nome_votante', '').strip()
        email_votante = request.form.get('email_votante', '').strip()
        projeto_id_raw = request.form.get('projeto_id', '').strip()

        if not nome_votante or not email_votante or not projeto_id_raw:
            flash('Por favor, preencha todos os campos.')
            conn.close()
            return redirect('/votar')

        try:
            projeto_id = int(projeto_id_raw)
        except ValueError:
            flash('Projeto inválido.')
            conn.close()
            return redirect('/votar')

        cursor.execute('SELECT * FROM votantes WHERE email = ?', (email_votante,))
        if cursor.fetchone():
            flash('Este e-mail já votou.')
            conn.close()
            return redirect('/votar')

        cursor.execute('UPDATE projetos SET votos = votos + 1 WHERE id = ?', (projeto_id,))
        cursor.execute('INSERT INTO votantes (nome, email) VALUES (?, ?)', (nome_votante, email_votante))
        conn.commit()
        conn.close()
        flash('Voto registrado com sucesso!')
        return redirect('/resultados')

    conn.close()
    return render_template('votar.html', projetos=projetos)

@app.route('/resultados')
def resultados():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos ORDER BY votos DESC')
    projetos = cursor.fetchall()
    conn.close()
    return render_template('resultados.html', projetos=projetos)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)


# Use o mesmo IP com e-mails diferentes → ✅ voto permitido
# Use o mesmo IP e o mesmo e-mail → ❌ voto bloqueado
# registrando a data do voto e do cadastro do projeto

# ❌ Mesmo e-mail + mesmo IP → bloqueia

# ❌ Mesmo e-mail + IP diferente → também bloqueia

# ✅ IP igual + e-mail diferente → permite

# ✅ IP diferente + e-mail diferente → permite

from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'segredo-super-seguro'

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tabela de projetos com data de cadastro
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL,
            turno TEXT NOT NULL,
            alunos TEXT NOT NULL,
            descricao TEXT NOT NULL,
            votos INTEGER DEFAULT 0,
            data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela de votantes com e-mail único e data de voto
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            ip TEXT NOT NULL,
            data_voto TEXT DEFAULT CURRENT_TIMESTAMP
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
        ip_votante = request.remote_addr

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

        # Verifica se o e-mail já votou, independentemente do IP
        cursor.execute('SELECT * FROM votantes WHERE email = ?', (email_votante,))
        if cursor.fetchone():
            flash('Este e-mail já foi utilizado para votar.')
            conn.close()
            return redirect('/votar')

        # Registra o voto
        cursor.execute('UPDATE projetos SET votos = votos + 1 WHERE id = ?', (projeto_id,))
        cursor.execute('INSERT INTO votantes (nome, email, ip) VALUES (?, ?, ?)', (nome_votante, email_votante, ip_votante))
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
    cursor.execute('SELECT nome, turma, turno, alunos, descricao, votos, data_cadastro FROM projetos ORDER BY votos DESC')
    projetos = cursor.fetchall()
    conn.close()
    return render_template('resultados.html', projetos=projetos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import database

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


database.criar_tabela()


@app.route('/')
def guarita():
    return render_template('guarita.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/api/cadastrar', methods=['POST'])
def api_cadastrar():
    nome = request.form.get('nome')
    materia = request.form.get('materia')
    placa = request.form.get('placa').upper().replace("-", "").strip()
    foto = request.files.get('foto')

    foto_url = ""
    if foto and foto.filename != '':
        filename = secure_filename(foto.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(filepath)
        foto_url = f"/static/uploads/{filename}"

    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO professores (nome, materia, placa, foto_url) VALUES (%s, %s, %s, %s)",
            (nome, materia, placa, foto_url)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "sucesso", "mensagem": "Professor cadastrado com sucesso!"})
    except Exception as e:
        print(f"\n============== ERRO AO CADASTRAR ==============")
        print(e)
        print("===============================================\n")
        return jsonify({"status": "erro", "mensagem": f"Erro interno: {str(e)}"})

@app.route('/api/verificar_placa', methods=['POST'])
def api_verificar_placa():
    data = request.get_json()
    placa = data.get('placa', '').upper().replace("-", "").strip()

    try:
        conn = database.get_connection()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM professores WHERE placa = %s", (placa,))
        professor = cursor.fetchone()
        cursor.close()
        conn.close()

        if professor:
            return jsonify({
                "status": "autorizado",
                "acao": "abrir_cancela",
                "dados": {
                    "nome": professor["nome"],
                    "materia": professor["materia"],
                    "foto_url": professor["foto_url"]
                }
            })
        else:
            return jsonify({
                "status": "negado",
                "acao": "manter_fechada",
                "mensagem": "Placa não localizada no sistema."
            })
            
    except Exception as e:
        print(f"\n============== ERRO AO VERIFICAR PLACA ==============")
        print(e)
        print("=====================================================\n")
        return jsonify({"status": "erro", "mensagem": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
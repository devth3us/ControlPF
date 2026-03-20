from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulando um banco de dados de professores autorizados.
# Em um projeto real, isso viria de um banco SQL (como o do sistema da escola).
professores_db = {
    "ABC1234": {"nome": "Prof. Wilhelm Klaus", "departamento": "TI"},
    "XYZ9876": {"nome": "Profa. Ana", "departamento": "Web Design"},
    "GHT5555": {"nome": "Prof. Roberto", "departamento": "Games"}
}

@app.route('/')
def index():
    # Renderiza a interface da guarita
    return render_template('index.html')

@app.route('/verificar_placa', methods=['POST'])
def verificar_placa():
    # Recebe os dados em JSON do Frontend (simulando a leitura da câmera LPR)
    data = request.get_json()
    placa = data.get('placa', '').upper().replace("-", "") # Padroniza a string

    # Verifica se a placa existe no banco de dados
    if placa in professores_db:
        prof = professores_db[placa]
        return jsonify({
            "status": "autorizado",
            "mensagem": f"Acesso Liberado. Bem-vindo(a), {prof['nome']}!",
            "acao": "abrir_cancela"
        })
    else:
        return jsonify({
            "status": "negado",
            "mensagem": "Placa não cadastrada. Acesso bloqueado.",
            "acao": "manter_fechada"
        })

if __name__ == '__main__':
    app.run(debug=True)
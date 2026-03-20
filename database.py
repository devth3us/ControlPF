import mysql.connector

def get_connection():
   
    return mysql.connector.connect(
        host="srv2037.hstgr.io",
        user="u586690765_SealHealth",
        ", 
        database="u586690765_SealHealthHs",
        port=3306
    )

def criar_tabela():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS professores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                materia VARCHAR(50) NOT NULL,
                placa VARCHAR(10) NOT NULL UNIQUE,
                foto_url VARCHAR(255)
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabela verificada/criada com sucesso no banco da Hostinger.")
    except Exception as e:
        print(f"ERRO DE BANCO DE DADOS: {e}")
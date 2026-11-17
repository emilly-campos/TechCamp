import mysql.connector


def conectar():
    # Diferente do SQLite da apostila, este conector acessa o MySQL existente.
    # Ajuste usuário, senha e porta conforme a instalação do seu computador.
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",  # Padrão local do XAMPP; altere se você definiu uma senha.
        database="loja_virtual",
        charset="utf8mb4",  # Permite nomes com acentos.
        connection_timeout=5  # Limita a espera se o MySQL estiver desligado.
    )

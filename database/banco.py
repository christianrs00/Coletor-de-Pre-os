import sqlite3

DB = "produtos.db"

def conectar():
    return sqlite3.conect(DB)

def criar_tabelas():

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS precos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            loja TEXT,
            preco REAL,
            link TEXT,
            data_coleta DATETIME DEFAULT CURRENT_TIMESTAMP
        )           
    """)

    conn.commit()
    conn.close()

def salvar_produtos(nome, loja, preco, link):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO produtos (nome, loja, preco, link)
        VALUE (?, ?, ?)
    """, (nome, loja, preco, link))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
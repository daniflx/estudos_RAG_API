import sqlite3
import os
from datetime import datetime

# Nome do Database
DB_NAME = "documentos_estado.db"

def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Criamos uma tabela relacional clássica.
    # O 'status' é crucial: ele começa 'pendente' e depois a IA muda para 'processado'.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_arquivo TEXT NOT NULL,
            data_upload TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def salvar_registro_documento(nome_arquivo: str):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    data_agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_inicial = "pendente" # Sempre começa como pendente
    
    cursor.execute('''
        INSERT INTO documentos (nome_arquivo, data_upload, status)
        VALUES (?, ?, ?)
    ''', (nome_arquivo, data_agora, status_inicial))
    
    conn.commit()
    conn.close()

def listar_todos_documentos():
   
    # Busca todas as linhas da tabela para mostrarmos no GET.

    conn = sqlite3.connect(DB_NAME)
    # Row factory permite acessar as colunas pelo nome (ex: row['nome_arquivo'])
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nome_arquivo, data_upload, status FROM documentos ORDER BY id DESC")
    linhas = cursor.fetchall()
    conn.close()
    
    # Converte as linhas do banco para uma lista de dicionários Python
    return [dict(linha) for linha in linhas]
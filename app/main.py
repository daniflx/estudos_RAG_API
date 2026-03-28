from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
# Importando as ferramentas que criamos no database.py
from app.database import init_db, salvar_registro_documento, listar_todos_documentos

# Criando API
app = FastAPI(
    title="API de Processamento de Documentos",
    description="API para upload e gerenciamento de PDFs (Estudo RAG)",
    version="1.0.0"
)

# Criando a pasta 'uploads' no computador, se ela ainda não existir
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Rodadando a função para garantir que a tabela SQL exista quando a API ligar
init_db()

@app.get("/")
def home():
    #Rota de boas-vindas para testar se a API está online (Health Check)
    return {"status": "online", "mensagem": "API rodando perfeitamente!"}

@app.post("/documentos")
async def upload_pdf(file: UploadFile = File(...)):
   
   # Recebe um PDF via POST, salva na pasta 'uploads' e registra no banco de dados.
    try:
        # 1. Validação de segurança básica (Só aceitamos PDF)
        if not file.filename.endswith(".pdf"):
            # Lançamos o Status Code 400 (Bad Request - Erro do usuário)
            raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

        # 2. Limpamos o nome do arquivo para não dar erro no Windows/Linux
        nome_limpo = file.filename.replace(" ", "_")
        caminho_arquivo = os.path.join(UPLOAD_DIR, nome_limpo)

        # 3. Salvamos o arquivo fisicamente na pasta 'uploads'
        with open(caminho_arquivo, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 4. Anotamos no nosso Banco de Dados que o arquivo chegou!
        salvar_registro_documento(nome_limpo)

        # 5. Retornamos Status 200 (OK) implícito pelo FastAPI
        return {
            "status": "sucesso",
            "arquivo": nome_limpo,
            "mensagem": "Arquivo recebido e registrado com status 'pendente'."
        }

    except HTTPException:
        raise
    except Exception as e:
        # Se algo quebrar no código, retornamos Status 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

@app.get("/documentos")
def listar_documentos():
  
    #Retorna a lista de todos os documentos que já passaram pela API.

    try:
        # Buscamos a lista lá no SQLite
        documentos = listar_todos_documentos()
        return {"total": len(documentos), "dados": documentos}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao buscar o banco de dados.")
# E-Commerce na Azure — Cadastro de Produtos (Streamlit + Azure Blob + Azure SQL)

Aplicação simples de **cadastro e listagem de produtos** (estilo e-commerce) construída com **Python + Streamlit**, armazenando:

- **Imagens** no **Azure Blob Storage**
- **Dados de produto** no **Azure SQL Database** (SQL Server)

A interface permite cadastrar um produto com **nome, preço, descrição e imagem**, salvando a URL pública da imagem no banco.

---

## 🧱 Arquitetura

**Streamlit (UI)**  
➡️ Upload da imagem  
➡️ Grava no **Azure Blob Storage** (container)  
➡️ Gera `imagem_url`  
➡️ Insere `nome, preço, descrição, imagem_url` no **Azure SQL Database**  
➡️ Lista produtos consultando o banco e exibindo cards com a imagem

---

## ✅ Requisitos

- Python 3.10+ (recomendado)
- Conta Azure com:
  - **Storage Account** + **Container** (para imagens)
  - **Azure SQL Server** + **Azure SQL Database**

Dependências Python (arquivo `requirements.txt`):

- `streamlit`
- `azure-storage-blob`
- `pymssql`
- `python-dotenv`

---

## 🚀 Como executar localmente

### 1) Clonar o repositório

```bash
git clone <seu-repo>
cd <seu-repo>
````

### 2) Instalar dependências

```bash
pip install -r .\requirements.txt
```

### 3) Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
BLOB_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=SEU_ACCOUNT;AccountKey=SUA_CHAVE;EndpointSuffix=core.windows.net"
BLOB_CONTAINER_NAME="fotos"
BLOB_ACCOUNT_NAME="SEU_ACCOUNT"

SQL_SERVER="SEU_SERVER.database.windows.net"
SQL_DATABASE="SEU_DATABASE"
SQL_USER="SEU_USUARIO"
SQL_PASSWORD="SUA_SENHA"
```


### 4) Executar a aplicação

```bash
streamlit.exe run .\main.py
```

Abra no navegador o endereço exibido no terminal (normalmente `http://localhost:8501`).

---

## 🗄️ Estrutura da tabela (Azure SQL)

Crie a tabela `produtos` no seu banco (Azure SQL Database):

```sql
create table produtos (
    id int identity(1,1) primary key,
    nome nvarchar(255),
    descricao nvarchar(max),
    preco decimal(18,2),
    imagem_url nvarchar(2083)
);
```

---

## 🔐 Segurança e boas práticas (recomendado)

Este projeto é didático/lab. Para produção, considere:

1. **Evita SQL Injection**
   Usando **queries parametrizadas**.

2. **Segredos**

* Nunca versionar `.env`
* Use **Azure Key Vault** ou variáveis do ambiente (CI/CD)
* Faça **rotação** de chaves caso alguma tenha sido exposta

3. **Permissões no Blob**
   Se o container for público, as imagens ficam acessíveis por URL.
   Em produção, prefira:

* Container privado + **SAS Token** para acesso controlado

---

## 🧪 Funcionalidades

* [x] Cadastro de produto com imagem
* [x] Upload da imagem para Azure Blob Storage
* [x] Persistência do produto no Azure SQL Database
* [x] Listagem em cards (3 por linha) com imagem via URL

---

## 🧾 Serviços Azure utilizados (lab)

* **Resource Group:** `dio-azure-lab-001`
* **Região:** `West US 2`
* **Azure SQL Server:** `sql-server-dio-lab-001`
* **Azure SQL Database:** (ex.: `free-sql-db-4222663`)
* **Storage Account:** (ex.: `stoaccdiolab001`)
* **Blob Container:** `fotos`

---

## 📁 Arquivos

* `main.py` — aplicação Streamlit
* `requirements.txt` — dependências
* `.env` — variáveis de ambiente (NÃO versionar)
* `infos.txt` — anotações do lab (tabela e dados Azure)

---

## 📌 Observações

* A URL da imagem é montada assim:
  `https://{BLOB_ACCOUNT_NAME}.blob.core.windows.net/{BLOB_CONTAINER_NAME}/{blob_name}`

* O nome do blob é gerado com `uuid` + nome original do arquivo para evitar colisões.

---

## 📄 Licença

Projeto de estudo/laboratório (DIO / Azure). 

import streamlit as st 
from azure.storage.blob import BlobServiceClient
import os 
import pymssql
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

blobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
blobContainerName = os.getenv("BLOB_CONTAINER_NAME")
blobAccountNAme = os.getenv("BLOB_ACCOUNT_NAME")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

st.title('Cadastro de Produtos')

product_name = st.text_input("Nome do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_description = st.text_area("Descrição do Produto")
product_image = st.file_uploader("Imagem do Produto", type=["jpg","png","jpeg"])

def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    safe_name = file.name.replace(" ", "_")
    blob_name = str(uuid.uuid4())+file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite=True)
    image_url = f"https://{blobAccountNAme}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    return image_url

def insert_product(product_name, product_price, product_description, product_image):
    if not product_name or not product_name.strip():
        st.warning("Informe o nome do produto.")
        return False

    if product_price is None or float(product_price) <= 0:
        st.warning("Informe um preço maior que zero.")
        return False

    if not product_description or not product_description.strip():
        st.warning("Informe a descrição do produto.")
        return False

    if product_image is None:
        st.warning("Envie uma imagem do produto (jpg/png/jpeg).")
        return False
    try:
        image_blob = upload_blob(product_image)
        conn = pymssql.connect(
            server=SQL_SERVER,
            user=SQL_USER,
            password=SQL_PASSWORD,
            database=SQL_DATABASE,
            timeout=10,
            login_timeout=10
        )
        with conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO dbo.produtos (nome, preco, descricao, imagem_url)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (product_name.strip(), float(product_price), product_description.strip(), image_blob))
            conn.commit()
            conn.close()

        return True        

    except Exception as e:
        st.error(f"Erro ao inserir produto: {e}")
        print(f"INSERT INTO dbo.produtos (nome, preco, descricao, imagem_url) VALUES ('{product_name}', {product_price}, '{product_description}', '{image_blob}')")
        return False
        
def list_products():
    try:
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM dbo.produtos")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao listar produto: {e}")
        return []
    
def list_products_screen():
    products = list_products()
    if products:
        card_por_linha = 3
        cols = st.columns(card_por_linha)
        for i, product in enumerate(products):
            col = cols[i % card_por_linha]
            with col:
                st.markdown(f"#### {product[1]}")
                st.write(f"** Preço: {product[2]}")    
                st.write(f"** Descrição: {product[3]}")    
                if product[4]:
                    html_img = f'<img src="{product[4]}" width="200" height="200" alt="Imagem do produto">'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.markdown("---")
                if (i+1)%card_por_linha==0 and (i+1)<len(products):
                    cols = st.columns(card_por_linha)
    else:
        st.info("Nenhum produto encontrado")

if st.button("Salvar Produto"):
    ok = insert_product (product_name, product_price, product_description, product_image)
    if ok:
        st.success("Produto salvo com sucesso!")

st.header('Produtos Cadastrados')    

if st.button("Listar Produtos"):
    list_products_screen()
    return_message = "Produtos Listados com Sucesso"
    
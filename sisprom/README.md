# Guia de Configuração Pós-Instalação do Ubuntu Server 24.04

Após a instalação do **Ubuntu Server 24.04**, siga os passos abaixo para configurar o sistema adequadamente para seu ambiente Docker com NGINX, Java, PostgreSQL, Kafka e outros serviços.

---

## 1. Ajustar o APT para Buscar o Security no Mirror 10.228.74.191

1. Abra o arquivo de fontes do APT:
    ```bash
    sudo nano /etc/apt/sources.list.d/ubuntu.sources
    ```
2. Substitua todas as ocorrências de `http://security.ubuntu.com/ubuntu/` por `http://10.228.74.191/ubuntu`.

---

## 2. Ajustar o Locale Correto para `pt_BR`

1. Gere o locale `pt_BR.UTF-8`:
    ```bash
    locale-gen pt_BR.UTF-8
    ```
2. Reconfigure os locales:
    ```bash
    dpkg-reconfigure locales
    ```

---

## 3. Atualizar e Instalar o Docker Compose

1. Atualize os pacotes do sistema:
    ```bash
    sudo apt update
    sudo apt upgrade -y
    ```
2. Instale o Docker Compose e outras ferramentas necessárias:
    ```bash
    sudo apt install docker-compose pv -y
    ```

---

## 4. Ajustar Configuração da Interface para Utilizar Bond com Diversas Interfaces

Configuração para acessar a internet compartilhando pelo NATv32 para Windows.

1. Edite o arquivo de configuração do Netplan:
    ```bash
    sudo nano /etc/netplan/01-netcfg.yaml
    ```
2. Adicione a seguinte configuração:
    ```yaml
    network:
      version: 2
      renderer: networkd
      ethernets:
        enX0:
          dhcp4: no
          dhcp6: no
        enX1:
          dhcp4: no
          dhcp6: no
      bonds:
        bond0:
          interfaces:
            - enX0
            - enX1
          addresses:
            - 10.228.74.115/24
          nameservers:
            addresses: [8.8.8.8, 10.228.74.20]
          routes:
            - to: 10.0.0.0/8
              via: 10.228.74.10
            - to: 192.168.0.0/16
              via: 10.228.74.250
            - to: 0.0.0.0/0
              via: 10.228.74.250
          parameters:
            mode: balance-rr
            mii-monitor-interval: 100
    ```

---

## 5. Aplicar as Configurações com Netplan

Execute o seguinte comando para aplicar as configurações do Netplan:
```bash
sudo netplan apply
```

---

## 6. Instalar as Ferramentas Mínimas para Acesso a Compartilhamento SMB do Storage

1. Instale o `cifs-utils` e `net-tools`:
    ```bash
    sudo apt install cifs-utils net-tools -y
    ```

---

## 7. Obter Imagens do Docker Desktop no Windows e Salvar como Arquivos

### No Windows:

1. Salve as imagens Docker em arquivos `.tar`:
    ```bash
    docker.exe save -o sisprom2-nginx-java-1.0.tar bitnami/nginx:latest_personalizada_com_java
    docker.exe save -o kafka-bitnami.tar bitnami/kafka:latest
    docker.exe save -o postgresql-bitnami.tar bitnami/postgresql:latest
    ```

---

## 8. Copiar as Imagens para o Servidor Linux via SCP ou Compartilhamento de Arquivos

### Opção 1: Usar SCP

1. Copie as imagens para o servidor Linux:
    ```bash
    scp postgresql-bitnami.tar secprom@10.228.74.115:/home/secprom
    scp nginx-bitnami.tar secprom@10.228.74.115:/home/secprom
    scp kafka-bitnami.tar secprom@10.228.74.115:/home/secprom
    ```

### Opção 2: Usar Compartilhamento SMB

1. Monte o compartilhamento SMB no Linux:
    ```bash
    sudo mount -t cifs -o username=secprom/ssu,password=5up0rt3,dir_mode=0777,file_mode=0777,vers=3.0 //10.228.74.128/servidor115 /media
    ```
2. Se a porta SMB estiver bloqueada no servidor, permita-a:
    ```bash
    sudo ufw allow 445/tcp
    sudo iptables -A INPUT -p tcp --dport 445 -j ACCEPT
    sudo netstat -tunlp | grep 445
    sudo telnet 10.228.74.250 445
    ```
3. Se não estiver conectando, acesse a interface de administração:
    ```
    https://10.228.74.10/ (admin/5up0rt3) Firewall/Regras/CPO_ADMINISTRATIVA
    ```

---

## 9. Carregar as Imagens no Linux

**Nota:** Carregar as imagens diretamente de uma pasta na rede evita duplicação de espaço em disco.

1. Carregue as imagens no Docker:
    ```bash
    sudo docker load -i postgresql-bitnami.tar
    sudo docker load -i sisprom2-nginx-java-1.0.tar
    sudo docker load -i kafka-bitnami.tar
    ```

---

## 10. Copiar os Principais Arquivos dos Serviços para `/var/opt/`

Recomenda-se copiar os arquivos dos serviços contidos em `/media` para `/var/opt/` conforme a estrutura abaixo:

- `docker-compose.yml`: Parâmetros para iniciar os três contêineres (NGINX com Java, PostgreSQL e Kafka).
- `kafka-persistence`: Volume compartilhado para o serviço de mensageria do Kafka.
- `pg_hba.conf`: Arquivo para configurar o PostgreSQL (as alterações devem ser realizadas diretamente na pasta `/opt/bitnami/...`).
- `/media`: Pasta montada que deve conter o dump da base de dados no formato SQL para a primeira inicialização.
- `Dockerfile.nginx-java`: Arquivo necessário para instalar o necessário para gerar uma build dinâmica do NGINX com Java.
- `nginx.conf`: Configurações utilizadas para o Angular.
- `OpenJDK21U-jdk_x64_linux_hotspot_21_35.tar.gz`: Versão do Java utilizada no contêiner.
- `www`: Todos os arquivos do Angular são servidos a partir desta pasta.

---

## 11. Conteúdo do `docker-compose.yml` Operacional Até a Presente Data

Edite o arquivo `docker-compose.yml` com o seguinte conteúdo:

```yaml
version: '3.8'

services:
  postgresql:
    image: bitnami/postgresql:latest
    container_name: postgresql
    environment:
      POSTGRESQL_PASSWORD: "#cp0@F@B#"
      POSTGRESQL_INITDB_LOCALE: pt_BR.UTF-8
      POSTGRESQL_INITDB_ENCODING: UTF8
    volumes:
      - /media:/media
    ports:
      - "5432:5432"
    networks:
      evaldo-full-stack:
        ipv4_address: 10.0.0.4

  nginx:
    build:
      context: .
      dockerfile: Dockerfile.nginx-java
    container_name: nginx
    environment:
      - NGINX_ENABLE_STREAM=yes
    volumes:
      - nginx_www:/opt/bitnami/nginx/html
    ports:
      - "80:80"
    networks:
      evaldo-full-stack:
        ipv4_address: 10.0.0.5

  kafka:
    image: bitnami/kafka:latest
    container_name: kafka
    environment:
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka:9093
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
    ports:
      - "9092:9092"
      - "9093:9093"
    networks:
      evaldo-full-stack:
        ipv4_address: 10.0.0.6

networks:
  evaldo-full-stack:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.0.0/24

volumes:
  nginx_www:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /var/opt/www
  nginx_conf:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /var/opt/nginx.conf
```

---

## 12. Conteúdo do Arquivo `Dockerfile.nginx-java` para Gerar uma Build Personalizada do NGINX com Java

Edite o arquivo `Dockerfile.nginx-java` com o seguinte conteúdo:

```dockerfile
FROM bitnami/nginx:latest

# Mudar para o usuário root para instalar pacotes
USER root

# Instalar dependências necessárias
RUN install_packages wget tar

# Copiar o JDK e o nginx.conf para o contêiner
COPY OpenJDK21U-jdk_x64_linux_hotspot_21_35.tar.gz /usr/java/
COPY nginx.conf /usr/java/

# Instalar o OpenJDK
RUN mkdir -p /usr/java && \
    cd /usr/java && \
    tar -xzvf OpenJDK21U-jdk_x64_linux_hotspot_21_35.tar.gz && \
    cp /usr/java/nginx.conf /opt/bitnami/nginx/conf/nginx.conf

# Definir variáveis de ambiente para o Java
ENV JAVA_HOME=/usr/java/jdk-21+35
ENV PATH=$JAVA_HOME/bin:$PATH

# Retornar ao usuário não root padrão da imagem
USER 1001

# Expor as portas necessárias
EXPOSE 80
EXPOSE 8080

# Extração dos arquivos do Angular
RUN cd /var/opt/ && \
    tar -xzvf /media/www.tar.gz && \
    mv /var/opt/var/www/* /var/opt/www/
```

---

## Passos Adicionais para Configuração e Gerenciamento

### 1. Construir e Salvar a Imagem Personalizada para o NGINX com Java

1. **Construir a imagem personalizada:**
    ```bash
    docker build -t sisprom2-nginx-java:1.0 .
    ```
2. **Salvar a imagem como um arquivo `.tar`:**
    ```bash
    docker save -o sisprom2-nginx-java-1.0.tar sisprom2-nginx-java:1.0
    ```
3. **Carregar a imagem no Linux (se ainda não carregada):**
    ```bash
    docker load -i sisprom2-nginx-java-1.0.tar
    ```

### 2. Executar Comandos para Configuração Inicial

Execute os seguintes comandos para configurar os serviços e o ambiente:

1. **Construir o serviço NGINX:**
    ```bash
    docker-compose build nginx
    ```
2. **Parar e remover o contêiner PostgreSQL:**
    ```bash
    docker-compose down -v postgresql
    ```
3. **Iniciar o contêiner NGINX:**
    ```bash
    docker-compose up -d nginx
    ```
4. **Remover o volume de dados do PostgreSQL (se necessário):**
    ```bash
    docker volume rm opt_postgresql_data
    ```
5. **Entrar no contêiner PostgreSQL:**
    ```bash
    docker exec -it postgresql /bin/bash
    ```
6. **Entrar no contêiner PostgreSQL como usuário root:**
    ```bash
    docker exec -u 0 -it postgresql /bin/bash
    ```
7. **Entrar no contêiner NGINX como usuário root:**
    ```bash
    docker exec -u 0 -it nginx-java /bin/bash
    ```
8. **Executar o script de inicialização dos serviços Java dentro do contêiner NGINX:**
    ```bash
    docker exec -u 0 -it nginx-java /opt/bitnami/nginx/html/microservicos/sispromii.sh start
    ```
9. **Navegar até o diretório dos microserviços:**
    ```bash
    cd /opt/bitnami/nginx/html/microservicos/
    ./sispromii.sh start
    ```

### 3. Configurar Locales

Configure os locais do sistema para `pt_BR.UTF-8`:

```bash
sudo locale-gen pt_BR.UTF-8
sudo dpkg-reconfigure locales
export LANG=pt_BR.UTF-8
export LANGUAGE=pt_BR:pt
export LC_ALL=pt_BR.UTF-8
```

### 4. Importar o Dump da Base de Dados no PostgreSQL

1. **Importar o dump SQL:**
    ```bash
    docker exec -e PGPASSWORD='#cp0@F@B#' -i postgresql psql -U postgres -f /media/all_databases_20241122.sql
    ```
2. **Compactar o dump com `pv` e `gzip`:**
    ```bash
    pv /media/all_databases_20241122.sql | gzip > all_databases_20241122.sql.gz
    ```

---

## Considerações Finais

### Boas Práticas para Gerenciamento de Serviços no Docker

1. **Separar Serviços em Contêineres Individuais:**
    - Mantenha cada serviço (NGINX, Java Gateway, PostgreSQL, Kafka) em seu próprio contêiner para facilitar a manutenção e escalabilidade.

2. **Utilizar Docker Compose para Orquestração:**
    - Facilita o gerenciamento de múltiplos contêineres e suas interdependências.

3. **Manter Arquivos de Configuração no Host:**
    - Utilize volumes para mapear arquivos de configuração do host para os contêineres, garantindo que as alterações sejam persistentes e versionáveis.

4. **Automatizar Scripts de Inicialização:**
    - Garanta que scripts como `sispromii.sh` estejam automatizados para iniciar os serviços necessários ao iniciar o contêiner.

5. **Gerenciar Logs de Forma Eficiente:**
    - Redirecione logs para arquivos específicos ou utilize ferramentas de monitoramento para facilitar a depuração.

### Segurança

1. **Configurar CORS Adequadamente:**
    - Verifique as configurações de CORS no `nginx.conf` para garantir que apenas origens confiáveis possam acessar os serviços.

2. **Implementar SSL/TLS:**
    - Considere configurar HTTPS para proteger as comunicações entre clientes e o servidor.

3. **Gerenciar Senhas e Credenciais com Cuidado:**
    - Utilize variáveis de ambiente ou ferramentas de gerenciamento de segredos para armazenar senhas e credenciais de forma segura.

### Monitoramento e Manutenção

1. **Monitorar o Desempenho dos Serviços:**
    - Utilize ferramentas de monitoramento para acompanhar o desempenho e a disponibilidade dos serviços.

2. **Atualizar Regularmente as Imagens Docker:**
    - Mantenha as imagens Docker atualizadas para incluir patches de segurança e melhorias de desempenho.

3. **Fazer Backups Regulares:**
    - Garanta que os dados importantes, como os bancos de dados, sejam regularmente copiados e armazenados de forma segura.

---

Seguindo este guia, você poderá configurar seu **Ubuntu Server 24.04** para operar com Docker, NGINX, Java e outros serviços essenciais, garantindo um ambiente estável e seguro para seus microserviços.

Se tiver dúvidas ou precisar de assistência adicional, sinta-se à vontade para perguntar!

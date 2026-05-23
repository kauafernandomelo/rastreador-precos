from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import sqlite3
import os

# =========================================
# CONFIGURAÇÕES
# =========================================

preco_limite = 2500

email_remetente = os.getenv("kauafernando098@gmail.com")

senha_email = os.getenv("ufmq pbow aqpg qqwd")

email_destino = os.getenv("kauafernando098@gmail.com")

url_produto = "https://www.kabum.com.br/produto/1012610/placa-de-video-msi-geforce-rtx-5060-ti-shadow-2x-oc-plus-nvidia-8gb-gddr7-128-bit-g506t-8s2cp"

# =========================================
# BANCO DE DADOS
# =========================================

conn = sqlite3.connect("banco.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS historico_precos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT,
    preco REAL
)
""")

conn.commit()

# =========================================
# PLAYWRIGHT
# =========================================

with sync_playwright() as p:

    navegador = p.chromium.launch(headless=True)

    pagina = navegador.new_page()

    pagina.goto(url_produto)

    pagina.wait_for_timeout(5000)

    html = pagina.content()

    soup = BeautifulSoup(html, "html.parser")

    # nome do produto
    nome = soup.find("h1").text.strip()

    # preço
    preco = soup.find("h4", class_="text-4xl")

    preco_texto = preco.text

    preco_texto = preco_texto.replace("R$", "")
    preco_texto = preco_texto.replace(".", "")
    preco_texto = preco_texto.replace(",", ".")
    preco_texto = preco_texto.strip()

    preco_final = float(preco_texto)

    # =========================================
    # PEGAR ÚLTIMO PREÇO
    # =========================================

    cursor.execute("""
    SELECT preco FROM historico_precos
    ORDER BY id DESC
    LIMIT 1
    """)

    ultimo_preco = cursor.fetchone()

    # =========================================
    # SALVAR PREÇO NOVO
    # =========================================

    cursor.execute("""
    INSERT INTO historico_precos (produto, preco)
    VALUES (?, ?)
    """, (nome, preco_final))

    conn.commit()

    # =========================================
    # MENOR E MAIOR PREÇO
    # =========================================

    cursor.execute("""
    SELECT MIN(preco) FROM historico_precos
    """)

    menor_preco = cursor.fetchone()[0]

    cursor.execute("""
    SELECT MAX(preco) FROM historico_precos
    """)

    maior_preco = cursor.fetchone()[0]

    # =========================================
    # STATUS DO PREÇO
    # =========================================

    status = ""

    if ultimo_preco is not None:

        ultimo_preco = ultimo_preco[0]

        if preco_final < ultimo_preco:

            status = "🔥 O preço CAIU!"

        elif preco_final > ultimo_preco:

            status = "📈 O preço AUMENTOU!"

        else:

            status = "➖ O preço NÃO mudou."

    else:

        status = "🆕 Primeiro preço registrado."

    # =========================================
    # ANALISAR SE O PREÇO ESTÁ BOM
    # =========================================

    avaliacao = ""

    if preco_final == menor_preco:

        avaliacao = "💰 MELHOR preço já encontrado!"

    elif preco_final <= preco_limite:

        avaliacao = "✅ Preço está BOM!"

    else:

        avaliacao = "❌ Preço ainda está alto."

    # =========================================
    # MOSTRAR TERMINAL
    # =========================================

    print("\nProduto:")
    print(nome)

    print("\nPreço atual:")
    print(preco_final)

    print("\nÚltimo preço:")
    print(ultimo_preco)

    print("\nMenor preço histórico:")
    print(menor_preco)

    print("\nMaior preço histórico:")
    print(maior_preco)

    print("\nStatus:")
    print(status)

    print("\nAvaliação:")
    print(avaliacao)

    # =========================================
    # ENVIAR EMAIL
    # =========================================

    mensagem = f"""
RASTREADOR DE PREÇOS

Produto:
{nome}

Preço atual:
R$ {preco_final}

Último preço:
R$ {ultimo_preco}

Menor preço histórico:
R$ {menor_preco}

Maior preço histórico:
R$ {maior_preco}

Status:
{status}

Avaliação:
{avaliacao}

Link:
{url_produto}
"""

    email = MIMEText(mensagem)

    email["Subject"] = "ATUALIZAÇÃO DE PREÇO"

    email["From"] = email_remetente

    email["To"] = email_destino

    servidor = smtplib.SMTP("smtp.gmail.com", 587)

    servidor.starttls()

    servidor.login(email_remetente, senha_email)

    servidor.send_message(email)

    servidor.quit()

    print("\nEmail enviado com sucesso!")

    navegador.close()

conn.close()
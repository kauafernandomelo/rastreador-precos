# 🛒 Rastreador de Preços Automático

Sistema de monitoramento de preços desenvolvido em Python utilizando web scraping e automação em nuvem.

O projeto acessa automaticamente páginas de produtos, captura preços em tempo real, salva o histórico em banco de dados e envia relatórios por e-mail diariamente.

---

# 🚀 Funcionalidades

* Monitoramento automático de preços
* Web scraping com Playwright
* Captura dinâmica de páginas modernas
* Histórico de preços usando SQLite
* Comparação de preços anteriores
* Detecção de aumento e queda de preço
* Avaliação do melhor preço encontrado
* Envio automático de e-mails
* Automação diária usando GitHub Actions
* Execução totalmente em nuvem

---

# 🛠 Tecnologias Utilizadas

* Python
* Playwright
* BeautifulSoup
* SQLite
* GitHub Actions
* SMTP (Gmail)

---

# ⚙️ Como Funciona

1. O GitHub Actions executa o script automaticamente todos os dias.
2. O Playwright acessa o produto monitorado.
3. O sistema captura:

   * Nome do produto
   * Preço atual
4. Os dados são salvos no banco SQLite.
5. O sistema compara os valores anteriores.
6. Um relatório completo é enviado automaticamente por e-mail.

---

# 📊 Informações Monitoradas

* Preço atual
* Último preço registrado
* Menor preço histórico
* Maior preço histórico
* Status do preço:

  * caiu
  * aumentou
  * não mudou

---

# 🖼 Demonstração do E-mail

<img width="1920" height="1080" alt="demo" src="https://github.com/user-attachments/assets/a23e1210-7438-412a-8611-61969b55eb8b" />


---

# 🔒 Segurança

As credenciais do sistema são protegidas utilizando GitHub Secrets.

---

# ☁️ Automação em Nuvem

O projeto roda automaticamente utilizando GitHub Actions, sem necessidade de deixar o computador ligado.

---

# 📌 Objetivo do Projeto

Projeto desenvolvido para estudo e prática de:

* Automação
* Web Scraping
* Python
* Banco de Dados
* GitHub Actions
* Deploy em Nuvem
* Integração com APIs e SMTP

import requests
from bs4 import BeautifulSoup
import smtplib
import email.message

# URL do produto
URL = "https://www.kabum.com.br/produto/459144/placa-de-video-rx-7600-challenger-asrock-amd-radeon-8gb-gddr6-90-ga41zz-00uanf"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}
PRECO_ALVO = 1899.91  # Defina o preço mínimo para alertar

# Função para obter o preço atual
def obter_preco():
    site = requests.get(URL, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')

    price_elements = soup.find_all("h4")
    for elem in price_elements:
        if "R$" in elem.get_text():
            price = elem.get_text(strip=True).replace("R$", "").replace(".", "").replace(",", ".")
            return float(price)
    return None  # Se não encontrar o preço

# Função para enviar email
def send_email(preco_atual):
    email_content = f"""<html>
    <body>
        <p>📉 O preço caiu para <strong>R$ {preco_atual:.2f}</strong>!</p>
        <p>Confira o produto no link abaixo:</p>
        <a href="{URL}">Ver Produto</a>
    </body>
    </html>"""

    msg = email.message.Message()
    msg['Subject'] = '📢 Alerta de Preço Baixo!'
    msg['From'] = 'contato.thiagolucascarvalho@gmail.com'
    msg['To'] = 'contato.thiagolucascarvalho@gmail.com'
    password = 'rsvf aqjn xkjc uurw'

    msg.add_header('Content-Type', 'text/html; charset=UTF-8')  # Define UTF-8 corretamente
    msg.set_payload(email_content.encode("utf-8"))  # Converte para bytes UTF-8

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
        print("✅ Email enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")

# Função para verificar e salvar o preço
def verificar_preco():
    preco_atual = obter_preco()
    
    if preco_atual is None:
        print("⚠ Erro ao obter preço!")
        return
    
    try:
        with open("ultimo_preco.txt", "r") as arquivo:
            ultimo_preco = float(arquivo.read().strip())
    except FileNotFoundError:
        ultimo_preco = None  # Se não existir, considera como None
    
    # Se o preço atual for menor que o alvo e menor que o último registrado, envia alerta
    if preco_atual < PRECO_ALVO and (ultimo_preco is None or preco_atual < ultimo_preco):
        send_email(preco_atual)
        
        # Atualiza o arquivo com o novo preço
        with open("ultimo_preco.txt", "w") as arquivo:
            arquivo.write(str(preco_atual))

# Executar a verificação
verificar_preco()
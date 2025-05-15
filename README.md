# 🛠️ PDF-Tools-Web

Este projeto é uma aplicação Flask para manipulação de arquivos PDF. Ela permite:

- Juntar e dividir PDFs
- Proteger e desbloquear com senha
- Converter HTML para PDF
- Converter PDF para Word, Excel, PowerPoint
- Fazer OCR em PDFs
- Converter imagens (JPG/PNG) para PDF

---

## 📁 Estrutura de Pastas

```
meu_app/
├── app.py
├── app.wsgi
├── requirements.txt
├── templates/
├── static/
├── uploads/         # Temporário (entrada)
├── results/         # Temporário (saída)
```

---

## 🚀 Rodando localmente (desenvolvimento)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Acesse em: [http://localhost:5000](http://localhost:5000)

---

## 🏗️ Deploy em servidor Apache (produção)

### 1. Instale dependências:

```bash
sudo apt update
sudo apt install apache2 libapache2-mod-wsgi-py3 python3-venv
```

### 2. Crie o ambiente virtual e instale os requisitos:

```bash
cd /var/www/meu_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Crie o arquivo `app.wsgi`:

```python
#!/usr/bin/python3
import sys, logging, os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/meu_app")
from app import app as application
```

### 4. Configure o Apache:

Crie o arquivo `/etc/apache2/sites-available/meu_app.conf`:

```apache
<VirtualHost *:80>
    ServerName seusite.com

    WSGIDaemonProcess meu_app python-path=/var/www/meu_app:/var/www/meu_app/venv/lib/python3.10/site-packages
    WSGIProcessGroup meu_app
    WSGIScriptAlias / /var/www/meu_app/app.wsgi

    Alias /static/ /var/www/meu_app/static/
    <Directory /var/www/meu_app/static/>
        Require all granted
    </Directory>

    <Directory /var/www/meu_app/>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/meu_app_error.log
    CustomLog ${APACHE_LOG_DIR}/meu_app_access.log combined
</VirtualHost>
```

### 5. Ative o site e reinicie o Apache:

```bash
sudo a2ensite meu_app
sudo systemctl reload apache2
```

### 6. Permissões (importantíssimo):

```bash
sudo chown -R www-data:www-data /var/www/meu_app/uploads /var/www/meu_app/results
sudo chmod -R 755 /var/www/meu_app
```

---

## 🔒 Segurança

- Nunca use `debug=True` em produção.
- Use HTTPS (Let’s Encrypt).
- Valide tipos de arquivo e tamanho.
- Gere `SECRET_KEY` real no `app.secret_key`.

---

## 📦 Requisitos

```txt
Flask
PyPDF2
pdf2docx
pdfplumber
pandas
openpyxl
weasyprint
python-pptx
pdf2image
pytesseract
Pillow
```

---

## 🧾 Licença

MIT License

---

Feito com ❤️ por [Seu Nome] – Pull Requests são bem-vindos!

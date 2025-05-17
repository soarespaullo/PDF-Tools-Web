## ⚠️ Projeto em Desenvolvimento

> Este projeto ainda está em andamento. Pode haver bugs e funcionalidades incompletas.


# 🛠️ PDFTools

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
PDFTools/
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
cd /var/www/PDFTools
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Crie o arquivo `app.wsgi`:

```python
#!/usr/bin/python3
import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/PDFTools')

from app import app as application
```

### 4. Configure o Apache:

Crie o arquivo `/etc/apache2/sites-available/PDFTools.conf`:

```apache
<VirtualHost *:80>
    ServerName localhost
    WSGIDaemonProcess PDFTools python-path=/var/www/PDFTools:/var/www/PDFTools/venv/lib/python3.10/site-packages
    WSGIProcessGroup PDFTools
    WSGIScriptAlias / /var/www/PDFTools/app.wsgi

    <Directory /var/www/PDFTools>
        Require all granted
    </Directory>

    Alias /static /var/www/PDFTools/static
    <Directory /var/www/PDFTools/static/>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/PDFTools_error.log
    CustomLog ${APACHE_LOG_DIR}/PDFTools_access.log combined
</VirtualHost>
```

### 5. Ative o site e reinicie o Apache:

```bash
sudo a2ensite PDFTools
sudo systemctl reload apache2
```

### 6. Permissões (importantíssimo):

```bash
sudo chown -R www-data:www-data /var/www/PDFTools/uploads /var/www/PDFTools/results
sudo chmod -R 755 /var/www/PDFTools
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

[`MIT License`](https://github.com/soarespaullo/PDF-Tools-Web/blob/main/LICENSE)

---

Feito com ❤️ por [Paulo Soares](https://soarespaullo.github.io/) – Pull Requests são bem-vindos!

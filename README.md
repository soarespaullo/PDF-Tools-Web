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
├── app.py                      # Arquivo principal da aplicação Flask
├── app.wsgi                    # Script WSGI usado pelo servidor (ex: Apache + mod_wsgi)
├── requirements.txt            # Arquivo com as dependências do projeto (pip install -r)
│
├── templates/                  # Templates Jinja2 renderizados pelo Flask
│   ├── base.html               # Template base (navbar, footer, etc.)
│   ├── index.html              # Página inicial
│   ├── comprimido.html         # Página de resultado para PDFs comprimidos
│   ├── desbloqueado.html       # Resultado de PDFs desbloqueados
│   ├── download.html           # Página de download de múltiplos arquivos
│   ├── download_unico.html     # Página de download individual
│   ├── paginas_convertidas.html # Resultados de PDFs convertidos para imagens, etc.
│   ├── paginas_divididas.html  # Resultado de divisão de PDF em páginas
│   ├── protegido.html          # Resultado de PDFs protegidos
│
├── static/                     # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   │   ├── style.css           # Estilos principais globais
│   │   └── download.css        # Estilos específicos para páginas de download
│   │
│   ├── js/
│   │   └── darkmode.js         # Script para alternar entre modo claro e escuro
│   │
│   └── favicon/                # Ícones para aba do navegador (favicon.ico, etc.)
│
├── uploads/                    # Pasta onde os arquivos enviados são armazenados temporariamente
├── results/                    # Pasta com os arquivos gerados (PDFs comprimidos, convertidos, etc.)
```

---

## 🚀 Rodando localmente (Desenvolvimento)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Acesse em: [http://localhost:5000](http://localhost:5000)

---

## 🏗️ Deploy em servidor Apache (Produção)

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

# Caminho para o diretório do seu app
sys.path.insert(0, '/var/www/PDFTools')

# Configurar logging para erros
logging.basicConfig(stream=sys.stderr)

# Garante que a variável de ambiente do Flask está correta
os.environ['FLASK_ENV'] = 'production'  # ou 'development' se estiver testando

# Importa o app Flask como "application" para o mod_wsgi
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
PyMuPDF
pdf2docx
PyPDF2
python-pptx
Pillow
weasyprint
pdfplumber
poppler-utils
pandas
openpyxl
pdf2image
reportlab
fpdf
pytesseract
werkzeug
```

---

## 🧾 Licença

Este projeto é licenciado sob a licença `MIT`. Veja o arquivo [**LICENSE**](https://github.com/soarespaullo/PDF-Tools-Web/blob/main/LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

Feito com ❤️ por [**Paulo Soares**](https://soarespaullo.github.io/) – `Pull Requests` são bem-vindos!

- 📧 [**soarespaullo@proton.me**](mailto:soarespaullo@proton.me)

- 💬 [**@soarespaullo**](https://t.me/soarespaullo) no Telegram

- 💻 [**GitHub**](https://github.com/soarespaullo)

---

## 📚 Recursos e Referências

- [Flask Documentation](https://flask.palletsprojects.com/) – Micro framework utilizado para criar a aplicação web.
- [PyPDF2](https://pypdf2.readthedocs.io/) – Manipulação de arquivos PDF (juntar, dividir, proteger, desbloquear).
- [WeasyPrint](https://weasyprint.org/) – Conversão de HTML/CSS para PDF.
- [pdf2docx](https://github.com/dothinking/pdf2docx) – Conversão de PDF para arquivos Word (.docx).
- [pdfplumber](https://github.com/jsvine/pdfplumber) – Extração de tabelas e dados estruturados de PDFs.
- [python-pptx](https://python-pptx.readthedocs.io/) – Geração de apresentações PowerPoint (.pptx).
- [pdf2image](https://github.com/Belval/pdf2image) – Conversão de páginas PDF para imagens (usado para OCR e slides).
- [Pillow (PIL)](https://pillow.readthedocs.io/) – Processamento de imagens em Python.
- [pytesseract](https://pypi.org/project/pytesseract/) – OCR (Reconhecimento Óptico de Caracteres) via Tesseract.
- [FPDF](https://pyfpdf.readthedocs.io/) – Geração de arquivos PDF a partir de imagens.
- [Werkzeug](https://werkzeug.palletsprojects.com/) – Utilizado para upload e segurança de arquivos.
- [Jinja2](https://jinja.palletsprojects.com/) – Template engine utilizada pelo Flask para renderizar HTML.
- [OpenPyXL](https://openpyxl.readthedocs.io/) – Escrita de arquivos Excel (.xlsx) com `pandas`.

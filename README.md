## ⚠️ Projeto em Desenvolvimento

> Este projeto ainda está em andamento. Pode haver bugs e funcionalidades incompletas.


# 📄 PDFTools

**PDFTools** é uma aplicação web feita com `Flask` que permite manipular arquivos **PDF** diretamente no navegador, de forma simples, rápida e sem instalar programas pesados.

## ✨ Funcionalidades

- 🔗 **Juntar PDFs** — Combine múltiplos arquivos PDF em um único documento.
- ✂️ **Dividir PDFs** — Separe páginas específicas de um PDF em arquivos individuais.
- 🔒 **Proteger PDF com senha** — Adicione senha para proteger documentos sensíveis.
- 🔓 **Desbloquear PDF** — Remova a senha de arquivos protegidos (quando permitido).
- 🌐 **Converter HTML para PDF** — Gere um PDF a partir de código ou páginas HTML.
- 🔁 **Converter PDF para:**
  - 📄 Word (.docx)
  - 📊 Excel (.xlsx)
  - 📽️ PowerPoint (.pptx)
- 🧠 **Aplicar OCR (Reconhecimento de Texto)** — Torne PDFs escaneados pesquisáveis.
- 🖼️ **Converter imagens para PDF** — Transforme arquivos JPG/PNG em PDFs organizados.
- 💧 **Adicionar Marca D'Água** — Insira marcas d'água personalizadas em documentos PDF.  
- 📉 **Comprimir PDF** — Reduza o tamanho do arquivo PDF mantendo a qualidade.

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
sudo python3 -m venv venv
source venv/bin/activate
sudo chown -R $USER:$USER /var/www/PDFTools/venv/
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
sudo mkdir -p /var/www/PDFTools/{uploads,results}
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
bleach
beautifulsoup4
```

---

## 🧾 Licença

Este projeto é licenciado sob a licença `MIT`. Veja o arquivo [**LICENSE**](https://github.com/soarespaullo/PDFTools/blob/main/LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

Feito com ❤️ por [**Paulo Soares**](https://soarespaullo.github.io/) – `Pull Requests` são bem-vindos!

- 📧 [**soarespaullo@proton.me**](mailto:soarespaullo@proton.me)

- 💬 [**@soarespaullo**](https://t.me/soarespaullo) no Telegram

- 💻 [**GitHub**](https://github.com/soarespaullo)

---

## 📚 Recursos e Referências

### 🔗 **Juntar PDFs**
- **Recurso:** Combine múltiplos PDFs em um único documento.
- **Tecnologias:** Python (PyPDF2, pdfrw), JavaScript (PDF-lib, pdf.js).
- **Referência:** [PyPDF2 Documentation](https://pythonhosted.org/PyPDF2/), [PDF-lib GitHub](https://github.com/Hopding/pdf-lib)

### ✂️ **Dividir PDFs**
- **Recurso:** Separe páginas específicas de um PDF em arquivos individuais.
- **Tecnologias:** Python (PyPDF2, pikepdf), JavaScript (PDF-lib).
- **Referência:** [pikepdf Documentation](https://pikepdf.readthedocs.io/), [PDF-lib GitHub](https://github.com/Hopding/pdf-lib)

### 🔒 **Proteger PDF com senha**
- **Recurso:** Adicione senha para proteger documentos sensíveis.
- **Tecnologias:** Python (PyPDF2), JavaScript (PDF-lib).
- **Referência:** [PyPDF2 - Encrypt PDF](https://pythonhosted.org/PyPDF2/PyPDF2.pdf), [PDF-lib GitHub](https://github.com/Hopding/pdf-lib)

### 🔓 **Desbloquear PDF**
- **Recurso:** Remova a senha de arquivos protegidos (quando permitido).
- **Tecnologias:** Python (PyPDF2), JavaScript (pdf.js).
- **Referência:** [PyPDF2 Decrypt PDF](https://pythonhosted.org/PyPDF2/PyPDF2.pdf), [pdf.js GitHub](https://github.com/mozilla/pdf.js)

### 🌐 **Converter HTML para PDF**
- **Recurso:** Gere um PDF a partir de código HTML ou páginas web.
- **Tecnologias:** Python (pdfkit, weasyprint), JavaScript (Puppeteer).
- **Referência:** [WeasyPrint Documentation](https://weasyprint.readthedocs.io/), [pdfkit Documentation](https://pdfkit.org/)

### 🔁 **Converter PDF para:**
- **Recurso:** Converta arquivos PDF para outros formatos como Word, Excel e PowerPoint.
- **Tecnologias:** Python (pdf2docx, xlwings), JavaScript (pdf-lib).
- **Referência:** [pdf2docx GitHub](https://github.com/modesty/pdf2docx), [xlwings Documentation](https://www.xlwings.org/)

### 🧠 **Aplicar OCR (Reconhecimento de Texto)**
- **Recurso:** Torne PDFs escaneados pesquisáveis.
- **Tecnologias:** Python (Tesseract, pytesseract), JavaScript (OCR.js).
- **Referência:** [Tesseract OCR Documentation](https://tesseract-ocr.github.io/), [OCR.js GitHub](https://github.com/odyniec/ocrad.js)

### 🖼️ **Converter Imagens para PDF**
- **Recurso:** Transforme arquivos JPG/PNG em PDFs organizados.
- **Tecnologias:** Python (Pillow, FPDF), JavaScript (jsPDF).
- **Referência:** [Pillow Documentation](https://pillow.readthedocs.io/), [jsPDF GitHub](https://github.com/parallax/jsPDF)

### 💧 **Adicionar Marca D'Água**
- **Recurso:** Insira marcas d'água personalizadas em documentos PDF.
- **Tecnologias:** Python (PyPDF2, reportlab), JavaScript (PDF-lib).
- **Referência:** [PyPDF2 - Add Watermark](https://pythonhosted.org/PyPDF2/), [PDF-lib GitHub](https://github.com/Hopding/pdf-lib)

### 📉 **Comprimir PDF**
- **Recurso:** Reduza o tamanho do arquivo PDF mantendo a qualidade.
- **Tecnologias:** Python (pikepdf, PyPDF2), JavaScript (pdf-lib).
- **Referência:** [pikepdf Documentation](https://pikepdf.readthedocs.io/), [PyPDF2 Compress PDF](https://pythonhosted.org/PyPDF2/)


# 🛠️ PDF Tools Web

Uma aplicação web simples e intuitiva para manipulação de arquivos PDF, desenvolvida com **Flask** (Python) e **Bootstrap 5**.

## 📌 Funcionalidades

- ✅ Juntar vários PDFs em um só
- ✅ Dividir PDF em páginas separadas (ZIP)
- ✅ Comprimir PDF
- ✅ Converter PDF para Word (.docx)
- ✅ Converter PDF para PowerPoint (.pptx)
- ✅ Editar conteúdo do PDF (inserir texto)
- ✅ Proteger PDF com senha
- ✅ Desbloquear PDF com senha
- ✅ Extrair imagens incorporadas de PDFs
- ✅ OCR (Reconhecimento de Texto) em PDFs escaneados *(opcional)*

---

## ⚙️ Tecnologias Utilizadas

- [Python 3.8+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [PyPDF2](https://pythonhosted.org/PyPDF2/)
- [pdf2docx](https://pypi.org/project/pdf2docx/)
- [python-pptx](https://python-pptx.readthedocs.io/)
- [pytesseract](https://pypi.org/project/pytesseract/) *(para OCR)*
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

---

## 🚀 Instalação


### Clone o repositório

```
git clone https://github.com/soarespaullo/PDF-Tools-Web.git
```

### Instale as dependências

```
pip install -r requirements.txt --break-system-packages
```

---

## ▶️ Como Usar

### Inicie o servidor Flask

```
python app.py
```

### Acesse no navegador:

```
http://localhost:5000
```

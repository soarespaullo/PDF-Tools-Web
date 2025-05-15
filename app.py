from flask import Flask, render_template, request, send_file, redirect, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from io import BytesIO
from PIL import Image
from fpdf import FPDF
from pdf2image import convert_from_path
import pytesseract
import zipfile
import PyPDF2

from weasyprint import HTML
from pdf2docx import Converter
import pdfplumber
import pandas as pd
from pptx import Presentation
from pptx.util import Inches

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

def salvar_arquivo(arquivo):
    if arquivo and arquivo.filename:
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
        arquivo.save(caminho)
        return caminho
    return None

def remover_arquivo(caminho):
    if caminho and os.path.exists(caminho):
        os.remove(caminho)

@app.errorhandler(413)
def arquivo_grande_demais(error):
    flash("Tamanho do arquivo excede o limite de 50MB.")
    return redirect('/')

@app.route('/')
def index():
    return render_template('index.html')

# ==== FUNCOES PDF ====

def send_pdf(buffer, filename):
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

@app.route('/juntar', methods=['POST'])
def juntar_pdf():
    try:
        arquivos = request.files.getlist("pdfs")
        merger = PyPDF2.PdfMerger()
        caminhos = [salvar_arquivo(a) for a in arquivos if a.filename.endswith('.pdf')]
        for c in caminhos:
            merger.append(c)
        pdf_buffer = BytesIO()
        merger.write(pdf_buffer)
        merger.close()
        for c in caminhos:
            remover_arquivo(c)
        return send_pdf(pdf_buffer, f"juntado_{datetime.now().timestamp()}.pdf")
    except Exception as e:
        flash(f"Erro ao juntar PDFs: {e}")
        return redirect('/')

@app.route('/dividir', methods=['POST'])
def dividir_pdf():
    try:
        caminho = salvar_arquivo(request.files['pdf'])
        reader = PyPDF2.PdfReader(caminho)
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for i, pagina in enumerate(reader.pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(pagina)
                pdf_bytes = BytesIO()
                writer.write(pdf_bytes)
                pdf_bytes.seek(0)
                zipf.writestr(f"pagina_{i+1}.pdf", pdf_bytes.read())
        remover_arquivo(caminho)
        zip_buffer.seek(0)
        return send_file(zip_buffer, mimetype='application/zip', as_attachment=True,
                         download_name=f"dividido_{datetime.now().timestamp()}.zip")
    except Exception as e:
        flash(f"Erro ao dividir PDF: {e}")
        return redirect('/')

@app.route('/proteger', methods=['POST'])
def proteger_pdf():
    try:
        caminho = salvar_arquivo(request.files['pdf'])
        senha = request.form.get('senha')
        reader = PyPDF2.PdfReader(caminho)
        writer = PyPDF2.PdfWriter()
        [writer.add_page(p) for p in reader.pages]
        writer.encrypt(senha)
        pdf_buffer = BytesIO()
        writer.write(pdf_buffer)
        remover_arquivo(caminho)
        return send_pdf(pdf_buffer, "protegido.pdf")
    except Exception as e:
        flash(f"Erro ao proteger PDF: {e}")
        return redirect('/')

@app.route('/desbloquear', methods=['POST'])
def desbloquear_pdf():
    try:
        caminho = salvar_arquivo(request.files['pdf'])
        senha = request.form.get('senha')
        reader = PyPDF2.PdfReader(caminho)
        if reader.is_encrypted:
            reader.decrypt(senha)
        writer = PyPDF2.PdfWriter()
        [writer.add_page(p) for p in reader.pages]
        pdf_buffer = BytesIO()
        writer.write(pdf_buffer)
        remover_arquivo(caminho)
        return send_pdf(pdf_buffer, "desbloqueado.pdf")
    except Exception as e:
        flash(f"Erro ao desbloquear PDF: {e}")
        return redirect('/')

@app.route('/html_para_pdf', methods=['POST'])
def html_para_pdf():
    try:
        html_code = request.form.get("html")
        if not html_code:
            flash("Nenhum HTML enviado.")
            return redirect('/')
        pdf_bytes = HTML(string=html_code).write_pdf()
        return send_pdf(BytesIO(pdf_bytes), "html_convertido.pdf")
    except Exception as e:
        flash(f"Erro ao converter HTML para PDF: {e}")
        return redirect('/')

@app.route('/pdf_para_word', methods=['POST'])
def pdf_para_word():
    try:
        caminho = salvar_arquivo(request.files['pdf'])
        saida = os.path.join(app.config['RESULT_FOLDER'], f"{datetime.now().timestamp()}.docx")
        Converter(caminho).convert(saida)
        remover_arquivo(caminho)
        return send_file(saida, as_attachment=True)
    except Exception as e:
        flash(f"Erro ao converter PDF para Word: {e}")
        return redirect('/')

@app.route('/pdf_para_excel', methods=['POST'])
def pdf_para_excel():
    try:
        caminho = salvar_arquivo(request.files['pdf'])
        tabelas = []
        with pdfplumber.open(caminho) as pdf:
            for pagina in pdf.pages:
                tabela = pagina.extract_table()
                if tabela:
                    df = pd.DataFrame(tabela[1:], columns=tabela[0])
                    tabelas.append(df)
        if not tabelas:
            flash("Nenhuma tabela encontrada.")
            return redirect('/')
        saida = os.path.join(app.config['RESULT_FOLDER'], f"{datetime.now().timestamp()}.xlsx")
        with pd.ExcelWriter(saida, engine='openpyxl') as writer:
            for i, df in enumerate(tabelas):
                df.to_excel(writer, sheet_name=f'Tabela_{i+1}', index=False)
        remover_arquivo(caminho)
        return send_file(saida, as_attachment=True)
    except Exception as e:
        flash(f"Erro ao converter PDF para Excel: {e}")
        return redirect('/')

@app.route('/pdf_para_ppt', methods=['POST'])
def pdf_para_ppt():
    try:
        caminho = salvar_arquivo(request.files['pdf'])
        imagens = convert_from_path(caminho)
        ppt = Presentation()
        for i, img in enumerate(imagens):
            slide = ppt.slides.add_slide(ppt.slide_layouts[6])
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], f"slide_{i+1}.jpg")
            img.save(img_path, 'JPEG')
            slide.shapes.add_picture(img_path, Inches(0), Inches(0), width=Inches(10), height=Inches(7.5))
            remover_arquivo(img_path)
        saida = os.path.join(app.config['RESULT_FOLDER'], f"{datetime.now().timestamp()}.pptx")
        ppt.save(saida)
        remover_arquivo(caminho)
        return send_file(saida, as_attachment=True)
    except Exception as e:
        flash(f"Erro ao converter PDF para PowerPoint: {e}")
        return redirect('/')

@app.route('/ocr_pdf', methods=['POST'])
def ocr_pdf():
    try:
        caminho = salvar_arquivo(request.files['pdf'])
        imagens = convert_from_path(caminho)
        texto = ''.join([pytesseract.image_to_string(img) for img in imagens])
        buffer = BytesIO()
        buffer.write(texto.encode('utf-8'))
        buffer.seek(0)
        remover_arquivo(caminho)
        return send_file(buffer, as_attachment=True, download_name="ocr.txt", mimetype="text/plain")
    except Exception as e:
        flash(f"Erro ao executar OCR: {e}")
        return redirect('/')

@app.route('/jpg_para_pdf', methods=['POST'])
def jpg_para_pdf():
    try:
        arquivos = request.files.getlist('imagens')
        imagens = []
        caminhos = []
        for a in arquivos:
            if a and a.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                caminho = salvar_arquivo(a)
                caminhos.append(caminho)
                img = Image.open(caminho).convert('RGB')
                imagens.append(img)
        if not imagens:
            flash("Nenhuma imagem válida enviada.")
            return redirect('/')
        pdf_buffer = BytesIO()
        imagens[0].save(pdf_buffer, format='PDF', save_all=True, append_images=imagens[1:])
        for c in caminhos:
            remover_arquivo(c)
        return send_pdf(pdf_buffer, f"convertido_{datetime.now().timestamp()}.pdf")
    except Exception as e:
        flash(f"Erro ao converter imagens: {e}")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=False)


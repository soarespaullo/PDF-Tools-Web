from flask import Flask, render_template, request, send_file, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os
import zipfile
import PyPDF2
import subprocess
import pytesseract
import pdfplumber
import pandas as pd
from pptx import Presentation
from pptx.util import Inches
from PyPDF2.errors import FileNotDecryptedError
from weasyprint import HTML
from datetime import datetime
from PIL import Image
from fpdf import FPDF
from pdf2image import convert_from_path
from pdf2docx import Converter
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO


# Cria a aplicação Flask
app = Flask(__name__)

# Define uma chave secreta para a aplicação
# Ela é usada para manter dados seguros nas sessões (por exemplo, cookies)
app.secret_key = 'supersecretkey'

# Define o caminho absoluto do diretório onde o arquivo atual (geralmente app.py) está localizado
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Cria o caminho completo para a pasta 'uploads', usada para armazenar arquivos enviados temporariamente
RESULT_FOLDER = os.path.join(BASE_DIR, 'results')

# Cria o caminho completo para a pasta 'results', usada para armazenar arquivos gerados pelo app
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Garante que a pasta 'uploads' exista; se não existir, será criada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Garante que a pasta 'results' exista; se não existir, será criada
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Rota principal - exibe a página inicial com o formulário
@app.route('/')
def index():
    return render_template('index.html')

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota responsável por juntar os arquivos PDF enviados
@app.route('/juntar', methods=['POST'])
def juntar_pdf():
    # Obtém a lista de arquivos enviados pelo formulário com o name="pdfs"
    arquivos = request.files.getlist("pdfs")

    # Cria um objeto PdfMerger para juntar os PDFs
    merger = PyPDF2.PdfMerger()

    # Itera sobre cada arquivo enviado
    for file in arquivos:
        # Verifica se o arquivo existe e se tem a extensão .pdf
        if file and file.filename.endswith('.pdf'):
            # Garante um nome de arquivo seguro
            filename = secure_filename(file.filename)

            # Salva o arquivo na pasta de upload
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            # Adiciona o PDF ao merger
            merger.append(path)

    # Formata a data e hora de forma legível para criar o nome do arquivo final
    data_formatada = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    output_filename = f"juntado_{data_formatada}.pdf"

    # Caminho onde o PDF final será salvo
    output_path = os.path.join(RESULT_FOLDER, output_filename)

    # Salva o PDF final com todos os arquivos juntados
    merger.write(output_path)
    merger.close()

    # Exibe uma mensagem de sucesso na próxima página renderizada
    flash("✅ PDFs juntados com sucesso!")

    # Redireciona para a página de download, passando o nome do arquivo
    return redirect(url_for('download_page', filename=output_filename))


# Rota que exibe a página HTML de download
@app.route('/download/<filename>')
def download_page(filename):
    # Renderiza o template com o link para baixar o arquivo gerado
    return render_template('download.html', filename=filename)


# Rota que envia o arquivo para download direto no navegador
@app.route('/baixar/<filename>')
def baixar_pdf(filename):
    # Monta o caminho completo do arquivo a ser baixado
    path = os.path.join(RESULT_FOLDER, filename)

    # Envia o arquivo como anexo para o navegador
    return send_file(path, as_attachment=True)

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota para processar a divisão de um PDF em páginas separadas
@app.route('/dividir', methods=['POST'])
def dividir_pdf():
    # Recebe o arquivo PDF enviado pelo formulário
    file = request.files['pdf']
    filename = secure_filename(file.filename)  # Garante um nome de arquivo seguro
    path = os.path.join(UPLOAD_FOLDER, filename)  # Caminho completo para salvar o PDF
    file.save(path)  # Salva o arquivo no diretório de uploads

    paginas_geradas = []  # Lista para armazenar os nomes dos arquivos gerados
    zip_filename = f"{os.path.splitext(filename)[0]}_paginas.zip"  # Nome do arquivo ZIP final
    zip_path = os.path.join(RESULT_FOLDER, zip_filename)  # Caminho completo do ZIP

    # Abre o PDF original
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)

        # Cria um novo arquivo ZIP para armazenar os PDFs das páginas
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for i, page in enumerate(reader.pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(page)  # Adiciona a página individual

                # Gera nome e caminho para a nova página
                output_filename = f"{os.path.splitext(filename)[0]}_pagina_{i+1}.pdf"
                output_path = os.path.join(RESULT_FOLDER, output_filename)

                # Salva a página como um novo arquivo PDF
                with open(output_path, 'wb') as out:
                    writer.write(out)

                # Adiciona o PDF ao arquivo ZIP
                zipf.write(output_path, arcname=output_filename)

                # Armazena o nome do arquivo gerado (para exibir depois)
                paginas_geradas.append(output_filename)

    # Exibe uma mensagem de sucesso na interface
    flash("✅ PDF dividido com sucesso!")

    # Redireciona para a página que exibe os links de download
    return redirect(url_for('download_paginas',
                            arquivos=','.join(paginas_geradas),
                            zipfile=zip_filename))

# Rota para exibir a página de download das páginas geradas
@app.route('/paginas-divididas')
def download_paginas():
    # Recupera os nomes dos arquivos individuais e do ZIP dos parâmetros da URL
    arquivos = request.args.get('arquivos', '').split(',')
    zipfile_name = request.args.get('zipfile', '')

    # Renderiza o template com os nomes dos arquivos
    return render_template('paginas_divididas.html', arquivos=arquivos, zipfile=zipfile_name)

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota para compressão de PDF
@app.route('/comprimir', methods=['POST'])
def comprimir_pdf():
    # Obtém o arquivo enviado pelo formulário
    file = request.files['pdf']

    # Garante um nome seguro para salvar no servidor
    filename = secure_filename(file.filename)

    # Caminho de entrada onde o arquivo original será salvo
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    # Define o nome do arquivo comprimido
    compressed_filename = f"comprimido_{filename}"

    # Caminho de saída para salvar o PDF comprimido
    output_path = os.path.join(RESULT_FOLDER, compressed_filename)

    # Comando Ghostscript para compressão
    gs_command = [
        "gs",                            # Chama o comando Ghostscript
        "-sDEVICE=pdfwrite",            # Define saída como PDF
        "-dCompatibilityLevel=1.4",     # Define compatibilidade para Adobe 5+
        "-dPDFSETTINGS=/screen",        # Nível de compressão (screen = alta compressão/baixa qualidade)
        "-dNOPAUSE",                    # Não pausa entre páginas
        "-dQUIET",                      # Reduz mensagens no terminal
        "-dBATCH",                      # Processa e sai automaticamente
        f"-sOutputFile={output_path}",  # Arquivo de saída
        input_path                      # Arquivo de entrada
    ]

    try:
        # Executa o comando para comprimir o PDF
        subprocess.run(gs_command, check=True)

        # Mensagem de sucesso ao usuário
        flash("✅ PDF comprimido com sucesso!")

        # Redireciona para página de download do arquivo comprimido
        return render_template('comprimido.html', filename=compressed_filename)

    except subprocess.CalledProcessError:
        # Se houver erro no comando (ex: Ghostscript não instalado)
        flash("❌ Erro ao comprimir o PDF. Verifique se o Ghostscript está instalado.")
        return redirect('/')

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota para proteção de PDF
@app.route('/proteger', methods=['POST'])
def proteger_pdf():
    # Obtém o arquivo enviado pelo formulário
    file = request.files['pdf']

    # Obtém a senha fornecida pelo usuário
    senha = request.form['senha']

    # Garante que o nome do arquivo seja seguro para salvar no sistema
    filename = secure_filename(file.filename)

    # Caminho completo para salvar o arquivo enviado
    input_path = os.path.join(UPLOAD_FOLDER, filename)

    # Define o nome e caminho do PDF protegido
    output_filename = f"protegido_{filename}"
    output_path = os.path.join(RESULT_FOLDER, output_filename)

    # Salva o PDF original no diretório temporário
    file.save(input_path)

    try:
        # Tenta ler o PDF salvo
        reader = PyPDF2.PdfReader(input_path)

        # Verifica se o PDF já está protegido por senha
        if reader.is_encrypted:
            flash("⚠️ Este PDF já está protegido por senha.")
            return redirect('/')

        # Cria um novo objeto PdfWriter para escrever o conteúdo com senha
        writer = PyPDF2.PdfWriter()

        # Adiciona todas as páginas do PDF original ao novo objeto
        for page in reader.pages:
            writer.add_page(page)

        # Aplica a senha de proteção no novo PDF
        writer.encrypt(senha)

        # Salva o novo PDF protegido no diretório de resultados
        with open(output_path, 'wb') as f:
            writer.write(f)

        # Mostra mensagem de sucesso e exibe a página de download
        flash("🔒 PDF protegido com sucesso!")
        return render_template('protegido.html', filename=output_filename)

    except Exception as e:
        # Se qualquer erro ocorrer, exibe uma mensagem de erro e retorna para a home
        flash(f"❌ Erro ao proteger o PDF: {str(e)}")
        return redirect('/')

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota para desbloquear PDF
@app.route('/desbloquear', methods=['POST'])
def desbloquear_pdf():
    file = request.files['pdf']
    senha = request.form['senha']

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_filename = f"desbloqueado_{filename}"
    output_path = os.path.join(RESULT_FOLDER, output_filename)

    file.save(input_path)
    reader = PyPDF2.PdfReader(input_path)

    if reader.is_encrypted:
        try:
            # Tenta descriptografar o PDF
            if not reader.decrypt(senha):
                flash("❌ Senha incorreta ou falha ao desbloquear.")
                return redirect('/')
            
            # Tenta acessar as páginas para verificar se foi desbloqueado
            _ = reader.pages[0]  # isso forçará o erro se não estiver realmente desbloqueado

        except FileNotDecryptedError:
            flash("❌ Senha incorreta. O PDF não pôde ser desbloqueado.")
            return redirect('/')
        except Exception as e:
            flash(f"❌ Erro ao processar o PDF: {str(e)}")
            return redirect('/')

    writer = PyPDF2.PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    with open(output_path, 'wb') as f:
        writer.write(f)

    flash("✅ PDF desbloqueado com sucesso!")
    return render_template('desbloqueado.html', filename=output_filename)

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota para converter HTML para PDF
@app.route('/html_para_pdf', methods=['POST'])
def html_para_pdf():
    try:
        # Pega o conteúdo HTML enviado pelo textarea
        html_content = request.form['html']
        if not html_content.strip():
            flash("❌ O campo HTML está vazio.")
            return redirect('/')

        # Define nome e caminho do PDF de saída
        output_filename = "html_convertido.pdf"
        output_path = os.path.join(RESULT_FOLDER, output_filename)

        # Converte HTML para PDF com WeasyPrint
        HTML(string=html_content).write_pdf(output_path)

        flash("✅ HTML convertido para PDF com sucesso!")
        return render_template('download_unico.html', filename=output_filename)

    except Exception as e:
        flash(f"❌ Erro ao converter HTML para PDF: {str(e)}")
        return redirect('/')

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota PDF para JPG
@app.route('/pdf_para_jpg', methods=['POST'])
def pdf_para_jpg():
    try:
        file = request.files['pdf']
        filename = secure_filename(file.filename)

        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        imagens = convert_from_path(input_path)
        arquivos_gerados = []

        for i, img in enumerate(imagens):
            output_filename = f"{filename.rsplit('.', 1)[0]}_pagina_{i+1}.jpg"
            output_path = os.path.join(RESULT_FOLDER, output_filename)
            img.save(output_path, 'JPEG')
            arquivos_gerados.append(output_filename)

        flash("✅ Conversão para JPG concluída!")
        return render_template('paginas_convertidas.html', arquivos=arquivos_gerados)

    except Exception as e:
        flash(f"❌ Erro ao converter PDF para JPG: {str(e)}")
        return redirect('/')

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota JPG para PDF
@app.route('/jpg_para_pdf', methods=['POST'])
def jpg_para_pdf():
    try:
        imagens = request.files.getlist("imagens")
        if not imagens or imagens[0].filename == '':
            flash("❌ Nenhuma imagem selecionada para conversão.")
            return redirect('/')

        pdf = FPDF()
        pdf.set_auto_page_break(0)  # Para evitar quebra automática de página

        for img in imagens:
            filename = secure_filename(img.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            img.save(path)

            # Abre a imagem e converte para RGB se necessário
            image = Image.open(path).convert('RGB')

            # Salva como JPEG temporariamente para o FPDF ler (FPDF não lê PNG diretamente)
            image_jpg_path = path.rsplit('.', 1)[0] + ".jpg"
            image.save(image_jpg_path)

            pdf.add_page()
            pdf.image(image_jpg_path, x=10, y=10, w=190)

        # Define nome único para o PDF de saída
        # Cria um nome com data e hora legível, ex: convertido_18-05-2025_14-52-30.pdf
        output_filename = f"convertido_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.pdf"
        output_path = os.path.join(RESULT_FOLDER, output_filename)

        pdf.output(output_path)

        flash("✅ Imagens convertidas para PDF com sucesso!")
        return render_template('download_unico.html', filename=output_filename)

    except Exception as e:
        flash(f"❌ Erro ao converter JPG para PDF: {str(e)}")
        return redirect('/')

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota OCR para PDF
@app.route('/ocr_pdf', methods=['POST'])
def ocr_pdf():
    try:
        # Recebe e salva o PDF enviado
        file = request.files['pdf']
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        # Converte o PDF em imagens
        imagens = convert_from_path(input_path)

        # Realiza OCR em cada imagem e junta os textos
        texto_extraido = ""
        for img in imagens:
            texto_extraido += pytesseract.image_to_string(img)

        # Cria nome de saída com data legível
        output_filename = f"ocr_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.txt"
        output_path = os.path.join(RESULT_FOLDER, output_filename)

        # Salva o texto extraído
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(texto_extraido)

        flash("✅ OCR realizado com sucesso! Texto extraído do PDF.")
        return render_template('download_unico.html', filename=output_filename)

    except Exception as e:
        flash(f"❌ Erro ao realizar OCR: {str(e)}")
        return redirect('/')

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota PDF para Word
@app.route('/pdf_para_word', methods=['POST'])
def pdf_para_word():
    try:
        # Verifica e salva o arquivo enviado
        file = request.files['pdf']
        if not file or not file.filename.endswith('.pdf'):
            flash("❌ Envie um arquivo PDF válido.")
            return redirect('/')

        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        # Define nome e caminho do arquivo Word de saída
        output_filename = f"convertido_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.docx"
        output_path = os.path.join(RESULT_FOLDER, output_filename)

        # Converte PDF para Word usando pdf2docx
        converter = Converter(input_path)
        converter.convert(output_path, start=0, end=None)
        converter.close()

        flash("✅ PDF convertido para Word com sucesso!")
        return render_template('download_unico.html', filename=output_filename)

    except Exception as e:
        flash(f"❌ Erro ao converter PDF para Word: {str(e)}")
        return redirect('/')

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota PDF para Excel
@app.route('/pdf_para_excel', methods=['POST'])
def pdf_para_excel():
    try:
        # Valida e salva o PDF enviado
        file = request.files['pdf']
        if not file or not file.filename.endswith('.pdf'):
            flash("❌ Envie um arquivo PDF válido.")
            return redirect('/')

        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        # Nome do Excel gerado
        output_filename = f"tabelas_extraidas_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.xlsx"
        output_path = os.path.join(RESULT_FOLDER, output_filename)

        # Extrai tabelas com pdfplumber
        todas_tabelas = []
        with pdfplumber.open(input_path) as pdf:
            for pagina in pdf.pages:
                tabelas = pagina.extract_tables()
                for tabela in tabelas:
                    df = pd.DataFrame(tabela[1:], columns=tabela[0])
                    todas_tabelas.append(df)

        if not todas_tabelas:
            flash("⚠️ Nenhuma tabela foi encontrada no PDF.")
            return redirect('/')

        # Escreve as tabelas em planilhas
        with pd.ExcelWriter(output_path) as writer:
            for i, tabela in enumerate(todas_tabelas):
                tabela.to_excel(writer, sheet_name=f"Tabela_{i+1}", index=False)

        flash("✅ PDF convertido para Excel com sucesso!")
        return render_template('download_unico.html', filename=output_filename)

    except Exception as e:
        flash(f"❌ Erro ao converter PDF para Excel: {str(e)}")
        return redirect('/')

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota PDF para PPT
@app.route('/pdf_para_ppt', methods=['POST'])
def pdf_para_ppt():
    try:
        # Salva o PDF enviado
        file = request.files['pdf']
        if not file or not file.filename.endswith('.pdf'):
            flash("❌ Envie um arquivo PDF válido.")
            return redirect('/')

        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        # Nome do PowerPoint de saída
        output_filename = f"apresentacao_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.pptx"
        output_path = os.path.join(RESULT_FOLDER, output_filename)

        # Converte cada página do PDF em imagem
        imagens = convert_from_path(input_path)
        prs = Presentation()

        # Tamanho padrão 16:9 (pode ajustar conforme necessário)
        prs.slide_width = Inches(13.33)
        prs.slide_height = Inches(7.5)

        for img in imagens:
            slide = prs.slides.add_slide(prs.slide_layouts[6])  # layout em branco
            img_path = os.path.join(RESULT_FOLDER, f"slide_temp_{datetime.now().timestamp()}.jpg")
            img.save(img_path, 'JPEG')

            # Adiciona imagem à apresentação
            slide.shapes.add_picture(img_path, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

        prs.save(output_path)

        flash("✅ PDF convertido para PowerPoint com sucesso!")
        return render_template('download_unico.html', filename=output_filename)

    except Exception as e:
        flash(f"❌ Erro ao converter PDF para PowerPoint: {str(e)}")
        return redirect('/')

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

# Rota PDF com Marca d'agua
@app.route('/marca_dagua', methods=['POST'])
def marca_dagua():
    try:
        file = request.files['pdf']
        texto = request.form.get('texto', '').strip()

        if not file or not file.filename.endswith('.pdf'):
            flash("❌ Envie um arquivo PDF válido.")
            return redirect('/')
        if not texto:
            flash("❌ Insira um texto para a marca d'água.")
            return redirect('/')

        # Salva o arquivo de entrada
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        # Gera o PDF com o texto da marca d'água usando reportlab
        watermark_pdf = BytesIO()
        c = canvas.Canvas(watermark_pdf, pagesize=letter)
        c.setFont("Helvetica", 40)
        c.setFillGray(0.5, 0.3)
        c.saveState()
        c.translate(300, 400)
        c.rotate(45)
        c.drawCentredString(0, 0, texto)
        c.restoreState()
        c.save()
        watermark_pdf.seek(0)

        # Cria um novo PDF com a marca d'água
        watermark = PdfReader(watermark_pdf)
        reader = PdfReader(input_path)
        writer = PdfWriter()

        watermark_page = watermark.pages[0]

        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)

        output_filename = f"marcado_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.pdf"
        output_path = os.path.join(RESULT_FOLDER, output_filename)

        with open(output_path, 'wb') as f:
            writer.write(f)

        flash("✅ Marca d'água adicionada com sucesso!")
        return render_template('download_unico.html', filename=output_filename)

    except Exception as e:
        flash(f"❌ Erro ao adicionar marca d'água: {str(e)}")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=False)


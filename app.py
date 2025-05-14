from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import fitz  # PyMuPDF
from pdf2docx import Converter
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import tempfile
import io
from zipfile import ZipFile

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = tempfile.mkdtemp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pdf_para_word', methods=['POST'])
def pdf_para_word():
    file = request.files.get('pdf')
    if not file or file.filename == '':
        flash('Selecione um arquivo PDF para converter para Word.')
        return redirect(url_for('index'))

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    output_path = filepath.replace('.pdf', '.docx')

    cv = Converter(filepath)
    cv.convert(output_path, start=0, end=None)
    cv.close()

    return send_file(output_path, as_attachment=True)

@app.route('/pdf_para_ppt', methods=['POST'])
def pdf_para_ppt():
    from pptx import Presentation
    from pptx.util import Inches

    file = request.files.get('pdf')
    if not file or file.filename == '':
        flash('Selecione um arquivo PDF para converter para PowerPoint.')
        return redirect(url_for('index'))

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    pdf_doc = fitz.open(filepath)
    ppt = Presentation()

    for page in pdf_doc:
        pix = page.get_pixmap()
        img_path = os.path.join(UPLOAD_FOLDER, f"page_{page.number}.png")
        pix.save(img_path)

        slide = ppt.slides.add_slide(ppt.slide_layouts[6])
        slide.shapes.add_picture(img_path, Inches(0), Inches(0), width=Inches(10), height=Inches(7.5))

    output_path = filepath.replace('.pdf', '.pptx')
    ppt.save(output_path)
    return send_file(output_path, as_attachment=True)

@app.route('/editar', methods=['POST'])
def editar_pdf():
    file = request.files.get('pdf')
    novo_texto = request.form.get('texto', '').strip()
    if not file or file.filename == '':
        flash('Selecione um arquivo PDF para editar.')
        return redirect(url_for('index'))
    if not novo_texto:
        flash('Digite o texto a ser inserido no PDF.')
        return redirect(url_for('index'))

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    doc = fitz.open(filepath)
    page = doc[0]
    page.insert_text((72, 72), novo_texto, fontsize=12, color=(0, 0, 0))
    output_path = filepath.replace('.pdf', '_editado.pdf')
    doc.save(output_path)
    doc.close()

    return send_file(output_path, as_attachment=True)

@app.route('/juntar', methods=['POST'])
def juntar_pdf():
    arquivos = request.files.getlist('pdfs')
    if not arquivos:
        flash('Envie pelo menos dois arquivos PDF.')
        return redirect(url_for('index'))

    merger = PdfMerger()
    for file in arquivos:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        merger.append(path)

    saida = os.path.join(UPLOAD_FOLDER, 'juntado.pdf')
    merger.write(saida)
    merger.close()

    return send_file(saida, as_attachment=True)

@app.route('/dividir', methods=['POST'])
def dividir_pdf():
    file = request.files.get('pdf')
    if not file or file.filename == '':
        flash('Selecione um arquivo PDF para dividir.')
        return redirect(url_for('index'))

    reader = PdfReader(file)
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            temp_path = os.path.join(UPLOAD_FOLDER, f"pagina_{i+1}.pdf")
            with open(temp_path, 'wb') as f:
                writer.write(f)
            zip_file.write(temp_path, arcname=f"pagina_{i+1}.pdf")

    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name="paginas.zip")

@app.route('/comprimir', methods=['POST'])
def comprimir_pdf():
    file = request.files.get('pdf')
    if not file or file.filename == '':
        flash('Selecione um arquivo PDF para comprimir.')
        return redirect(url_for('index'))

    reader = PdfReader(file)
    writer = PdfWriter()
    for pagina in reader.pages:
        writer.add_page(pagina)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return send_file(output, download_name="comprimido.pdf", as_attachment=True)

@app.route('/proteger', methods=['POST'])
def proteger_pdf():
    file = request.files.get('pdf')
    senha = request.form.get('senha')
    if not file or file.filename == '':
        flash('Selecione um arquivo PDF para proteger.')
        return redirect(url_for('index'))
    if not senha:
        flash('Digite uma senha para proteger o PDF.')
        return redirect(url_for('index'))

    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(senha)
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return send_file(output, download_name="protegido.pdf", as_attachment=True)

@app.route('/desbloquear', methods=['POST'])
def desbloquear_pdf():
    file = request.files.get('pdf')
    senha = request.form.get('senha')
    if not file or file.filename == '':
        flash('Selecione um arquivo PDF para desbloquear.')
        return redirect(url_for('index'))
    if not senha:
        flash('Digite a senha atual do PDF.')
        return redirect(url_for('index'))

    reader = PdfReader(file)
    if reader.is_encrypted:
        try:
            reader.decrypt(senha)
        except:
            flash('Senha incorreta.')
            return redirect(url_for('index'))

    writer = PdfWriter()
    for pagina in reader.pages:
        writer.add_page(pagina)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return send_file(output, download_name="desbloqueado.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


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


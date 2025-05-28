#!/usr/bin/env bash
#
# PDFTools - Script de instalação e configuração automática
#
# Descrição:
# Script interativo para instalar dependências de sistema,
# clonar o repositório PDFTools, criar ambiente virtual,
# instalar pacotes Python, configurar Apache e habilitar o site.
#
# Autor: Paulo Soares
# GitHub: https://github.com/soarespaullo/PDFTools
# Data: 2025-05-25
#
# Uso:
# ./PDFTools.sh
#
# Observação:
# Execute este script com permissões de sudo para instalações e configurações.
#
# Cores
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # Sem cor

banner() {
  echo -e "${CYAN}"
  echo '$$$$$$$\  $$$$$$$\  $$$$$$$$\ $$$$$$$$\                  $$\           '
  echo '$$  __$$\ $$  __$$\ $$  _____|\__$$  __|                 $$ |          '
  echo '$$ |  $$ |$$ |  $$ |$$ |         $$ | $$$$$$\   $$$$$$\  $$ | $$$$$$$\ '
  echo '$$$$$$$  |$$ |  $$ |$$$$$\       $$ |$$  __$$\ $$  __$$\ $$ |$$  _____|'
  echo '$$  ____/ $$ |  $$ |$$  __|      $$ |$$ /  $$ |$$ /  $$ |$$ |\$$$$$$\  '
  echo '$$ |      $$ |  $$ |$$ |         $$ |$$ |  $$ |$$ |  $$ |$$ | \____$$\ '
  echo '$$ |      $$$$$$$  |$$ |         $$ |\$$$$$$  |\$$$$$$  |$$ |$$$$$$$  |'
  echo '\__|      \_______/ \__|         \__| \______/  \______/ \__|\_______/ '
  echo -e "${YELLOW}                 Instalador Interativo para o PDFTools${NC}"
  echo
}

APP_DIR="/var/www/PDFTools"
REPO_URL="https://github.com/soarespaullo/PDFTools.git"
VENV_DIR="$APP_DIR/venv"
REQUIREMENTS="$APP_DIR/requirements.txt"
APACHE_CONF_SRC="$APP_DIR/PDFTools.conf"
APACHE_CONF_DST="/etc/apache2/sites-available/PDFTools.conf"

install_dependencies() {
  echo -e "${YELLOW}🚀 Iniciando a instalação das dependências do sistema para PDFTools...${NC}"
  sudo apt update > /dev/null 2>&1
  sudo apt install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3-venv \
    build-essential \
    libffi-dev \
    libssl-dev \
    libfreetype6-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libjpeg-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    libtiff-dev \
    zlib1g-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-dev \
    libxml2-dev \
    libxslt1-dev \
    fonts-liberation \
    fonts-freefont-ttf \
    poppler-utils \
    ghostscript \
    libgl1 \
    tesseract-ocr > /dev/null 2>&1
  echo -e "${GREEN}✅ Instalação concluída com sucesso!${NC}"
}

setup_pdf_tools() {
  if [ ! -d "$APP_DIR" ]; then
    echo -e "${YELLOW}📥 Pasta $APP_DIR não encontrada. Clonando repositório...${NC}"
    sudo git clone "$REPO_URL" "$APP_DIR" > /dev/null 2>&1
  fi

  echo -e "${YELLOW}📁 Criando pastas uploads e results em $APP_DIR (se não existirem)...${NC}"
  sudo mkdir -p "$APP_DIR/uploads" "$APP_DIR/results"

  echo -e "${YELLOW}📦 Criando ambiente virtual em $VENV_DIR...${NC}"
  python3 -m venv "$VENV_DIR"

  echo -e "${YELLOW}🐍 Ativando o ambiente virtual...${NC}"
  source "$VENV_DIR/bin/activate"

  if [ -f "$REQUIREMENTS" ]; then
    echo -e "${YELLOW}⬇️ Instalando pacotes do requirements.txt (saída oculta)...${NC}"
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r "$REQUIREMENTS" > /dev/null 2>&1
  else
    echo -e "${RED}⚠️ Arquivo requirements.txt não encontrado em $REQUIREMENTS. Abortando.${NC}"
    exit 1
  fi

  echo -e "${YELLOW}🔐 Ajustando permissões da aplicação...${NC}"
  sudo chown -R www-data:www-data "$APP_DIR"
  sudo chmod -R 755 "$APP_DIR"

  if [ -f "$APACHE_CONF_SRC" ]; then
    echo -e "${YELLOW}📄 Copiando $APACHE_CONF_SRC para $APACHE_CONF_DST...${NC}"
    sudo cp "$APACHE_CONF_SRC" "$APACHE_CONF_DST"
  else
    echo -e "${YELLOW}⚠️ Arquivo $APACHE_CONF_SRC não encontrado. Ignorando configuração Apache.${NC}"
  fi

  echo -e "${YELLOW}🔧 Habilitando site PDFTools e desabilitando 000-default.conf...${NC}"
  sudo a2ensite PDFTools.conf > /dev/null 2>&1
  sudo a2dissite 000-default.conf > /dev/null 2>&1

  echo -e "${YELLOW}🔄 Reiniciando o Apache para aplicar as mudanças...${NC}"
  sudo systemctl restart apache2

  echo -e "${GREEN}✅ Ambiente e servidor Apache configurado com sucesso!${NC}"
}

menu() {
  while true; do
    banner
    echo -e "${CYAN}Escolha uma opção:${NC}"
    echo -e "${MAGENTA}1) Instalar dependências do sistema${NC}"
    echo -e "${MAGENTA}2) Configurar e instalar PDFTools${NC}"
    echo -e "${MAGENTA}3) Sair${NC}"
    read -rp "$(echo -e "${MAGENTA}Opção:${NC} ")" opt
    case $opt in
      1) install_dependencies ;;
      2) setup_pdf_tools ;;
      3) echo -e "${YELLOW}Saindo... Até mais! 👋${NC}"; exit 0 ;;
      *) echo -e "${RED}Opção inválida. Tente novamente${NC}" ;;
    esac
    echo
    read -rp "Pressione ENTER para voltar ao menu..."
    clear
  done
}

menu

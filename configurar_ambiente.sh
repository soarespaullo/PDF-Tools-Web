#!/bin/bash

# Cores ANSI para saída colorida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # Sem cor (reset)

APP_DIR="/var/www/PDFTools"
REPO_URL="https://github.com/soarespaullo/PDFTools.git"
VENV_DIR="$APP_DIR/venv"
REQUIREMENTS="$APP_DIR/requirements.txt"
APACHE_CONF_SRC="$APP_DIR/PDFTools.conf"
APACHE_CONF_DST="/etc/apache2/sites-available/PDFTools.conf"

echo -e "${CYAN}📥 Verificando a existência do diretório $APP_DIR...${NC}"
if [ ! -d "$APP_DIR" ]; then
  echo -e "${YELLOW}Diretório não encontrado. Clonando repositório...${NC}"
  sudo git clone "$REPO_URL" "$APP_DIR" > /dev/null 2>&1
  echo -e "${GREEN}Repositório clonado com sucesso.${NC}"
else
  echo -e "${GREEN}Diretório já existe. Pulando clone.${NC}"
fi

echo -e "${CYAN}📁 Criando pastas uploads e results em $APP_DIR (se não existirem)...${NC}"
sudo mkdir -p "$APP_DIR/uploads" "$APP_DIR/results"

echo -e "${CYAN}📦 Criando ambiente virtual em $VENV_DIR...${NC}"
python3 -m venv "$VENV_DIR"

echo -e "${CYAN}🐍 Ativando o ambiente virtual...${NC}"
source "$VENV_DIR/bin/activate"

if [ -f "$REQUIREMENTS" ]; then
  echo -e "${CYAN}⬇️ Instalando pacotes do requirements.txt (saída oculta)...${NC}"
  pip install --upgrade pip > /dev/null 2>&1
  pip install -r "$REQUIREMENTS" > /dev/null 2>&1
  echo -e "${GREEN}Dependências instaladas com sucesso.${NC}"
else
  echo -e "${RED}⚠️ Arquivo requirements.txt não encontrado em $REQUIREMENTS. Abortando instalação de pacotes.${NC}"
  exit 1
fi

echo -e "${CYAN}🔐 Ajustando permissões da aplicação...${NC}"
sudo chown -R www-data:www-data "$APP_DIR"
sudo chmod -R 755 "$APP_DIR"

if [ -f "$APACHE_CONF_SRC" ]; then
  echo -e "${CYAN}📄 Copiando $APACHE_CONF_SRC para $APACHE_CONF_DST...${NC}"
  sudo cp "$APACHE_CONF_SRC" "$APACHE_CONF_DST"
  echo -e "${GREEN}Arquivo de configuração Apache copiado.${NC}"
else
  echo -e "${YELLOW}⚠️ Arquivo $APACHE_CONF_SRC não encontrado. Ignorando configuração Apache.${NC}"
fi

echo -e "${CYAN}🔧 Habilitando site PDFTools e desabilitando 000-default.conf...${NC}"
sudo a2ensite PDFTools.conf > /dev/null 2>&1
sudo a2dissite 000-default.conf > /dev/null 2>&1

echo -e "${CYAN}🔄 Reiniciando o Apache para aplicar as mudanças...${NC}"
sudo systemctl restart apache2

echo -e "${GREEN}✅ Ambiente configurado e Apache configurado com sucesso!${NC}"

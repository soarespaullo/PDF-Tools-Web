#!/usr/bin/python3
import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/meu_app')

from app import app as application


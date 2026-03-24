"""
Configuration file - loads from .env file
"""
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL Database Configuration (from .env file)
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'autocommit': True
}

# Application Configuration
APP_CONFIG = {
    'window_width': 1000,
    'window_height': 700,
    'window_min_width': 900,
    'window_min_height': 600,
    'title': 'Gestion de Stock - Store & Inventory Management System',
    'version': '1.0.0'
}

# GUI Theme Configuration
THEME_CONFIG = {
    'theme': 'dark-blue',
    'color_scheme': 'blue'
}

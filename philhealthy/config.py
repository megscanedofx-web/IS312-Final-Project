"""
PhilHealthy Configuration
Update these settings for your environment.
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'philhealthy-change-this-in-production')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'philhealthy')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

"""Masonite Lang Settings"""
from masonite.environment import env

LOCALE = env('APP_LOCALE', 'en')

LOCALES_DIR = env('APP_LOCALES_DIR', 'locales')

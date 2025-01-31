"""Masonite Lang Settings"""
from masonite.environment import env

LOCALE = env('APP_LOCALE', 'en')

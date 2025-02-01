import os
import json
from typing import Dict

from masonite.configuration import config


class Translator:

    def __init__(self, app) -> None:
        self.app = app
        self.config = config('lang')
        self._locale = self.config.get('locale')

    def current_locale(self) -> str:
        return self._locale

    def set_locale(self, locale: str) -> None:
        self._locale = locale

    def is_locale(self, locale: str) -> bool:
        return self._locale == locale

    def setup_view(self) -> None:
        self.app.make("view").share({
            "__": self.trans
        })

    def trans(self, key: str) -> str:
        translations = self._load_language_file()
        return translations.get(key, key)

    def _load_language_file(self) -> Dict:
        file_path = os.path.join(self.app.base_path, "lang", f"{self._locale}.json")

        if not os.path.exists(file_path):
            return {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            return {}

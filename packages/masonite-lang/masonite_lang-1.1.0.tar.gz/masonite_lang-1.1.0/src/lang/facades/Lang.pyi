from masonite.request.request import Request

class Lang:
    def current_locale(self) -> str:
        """Returns the current locale."""
        pass
    def set_locale(self, locale: str) -> str:
        """Sets the current locale."""
        pass
    def is_locale(self, locale: str) -> bool:
        """Returns true if the current locale is the same as the locale passed."""
        pass
    def trans(self, key: str) -> str:
        """Translates the key."""
        pass

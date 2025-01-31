"""A LangProvider Service Provider."""

from masonite.packages import PackageProvider

from ..translator import Translator


class LangProvider(PackageProvider):

    def configure(self):
        """Register objects into the Service Container."""
        (
            self.root("lang")
            .name("lang")
            .config("config/lang.py", publish=True)
        )

    def register(self):
        super().register()

        translator = Translator(app=self.application)
        self.application.bind("translator", translator)

        translator.setup_view()

    def boot(self):
        """Boots services required by the container."""
        pass

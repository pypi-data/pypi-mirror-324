"""A LangProvider Service Provider."""

from masonite.packages import PackageProvider

from ..Lang import Lang


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

        lang = Lang(app=self.application)
        self.application.bind("lang", lang)
        lang.setup_view()

    def boot(self):
        """Boots services required by the container."""
        pass

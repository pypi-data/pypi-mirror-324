
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from babel.support import Translations


# Load translations
def get_translations(locale):
    tl = Translations.load(Path(__file__).parent / "translations", [locale], domain="merged")
    return tl

# Configure Jinja2 with the i18n extension
def create_jinja_env(locale):
    translations = get_translations(locale)
    env = Environment(
        loader=FileSystemLoader("templates"),
        extensions=["jinja2.ext.i18n"],  # Enable the i18n extension
    )
    env.install_gettext_translations(translations)
    return env
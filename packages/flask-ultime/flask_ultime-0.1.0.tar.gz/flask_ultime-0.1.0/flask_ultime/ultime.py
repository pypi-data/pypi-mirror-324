import os 
from markupsafe import Markup
from flask import url_for

from .cli import tailwindcss_cli


class FlaskUltime:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.jinja_env.globals.update(ultime_css=self._get_stylesheet)
        app.jinja_env.globals.update(ultime_js=self._get_script)
        
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['ultime'] = self
        
        # Register CLI commands
        app.cli.add_command(tailwindcss_cli)

    def _get_stylesheet(self):
        """Return the stylesheet link tag."""
        if os.path.exists(os.path.join(self.app.static_folder, 'dist', 'style.css')):
            return Markup(f'<link rel="stylesheet" href="{url_for("static", filename="dist/style.css")}">')
        return ''

    def _get_script(self):
        """Return the script tag for Alpine.js and script.js."""
        if os.path.exists(os.path.join(self.app.static_folder, 'dist', 'alpine.js')) and os.path.exists(os.path.join(self.app.static_folder, 'dist', 'script.js')):
            return (
                Markup(f'<script defer src="{url_for("static", filename="dist/script.js")}"></script>')
                + Markup(f'<script defer src="{url_for("static", filename="dist/alpine.js")}"></script>'))
        return ''
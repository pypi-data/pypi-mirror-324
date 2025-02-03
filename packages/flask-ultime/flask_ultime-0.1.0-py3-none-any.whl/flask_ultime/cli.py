import os
import click
import platform
import subprocess
import requests
from flask import current_app
from flask.cli import with_appcontext

from .utils import create_directories, get_tailwind_binary_path, download_alpine_js
from .constants import TAILWIND_BINARY_URLS


@click.group('ultime')
def tailwindcss_cli():
    """TailwindCSS commands."""
    pass


@tailwindcss_cli.command('init')
@with_appcontext
def init_command():
    """Initialize TailwindCSS files."""
    static_folder = current_app.static_folder
    create_directories(static_folder)
    
    # Create style.css in src
    src_css = os.path.join(static_folder, 'src', 'style.css')
    
    if not os.path.exists(src_css):
        with open(src_css, 'w') as f:
            f.write('@import "tailwindcss";')

    # Create script.js in dist
    dist_js = os.path.join(static_folder, 'dist', 'script.js')
    
    if not os.path.exists(dist_js):
        with open(dist_js, 'w') as f:
            f.write('''
window.addEventListener("alpine:init", () => {
    Alpine.data("counter", () => ({
        count: 0,
        increment() {
            this.count++;
        },
        decrement() {
            this.count--;
        },
    }));
});''')
    
    # Create initial dist/style.css
    dist_css = os.path.join(static_folder, 'dist', 'style.css')
    
    if not os.path.exists(dist_css):
        open(dist_css, 'a').close()
    
    click.echo('TailwindCSS files initialized successfully.')


@tailwindcss_cli.command('install')
@with_appcontext
def install_command():
    """Install TailwindCSS CLI and Alpine.js."""
    static_folder = current_app.static_folder
    system = platform.system()
    
    if system not in TAILWIND_BINARY_URLS:
        click.echo(f'Unsupported operating system: {system}')
        return
    
    binary_url = TAILWIND_BINARY_URLS[system]
    binary_path = get_tailwind_binary_path(static_folder)
    
    # Download TailwindCSS binary
    response = requests.get(binary_url)
    
    with open(binary_path, 'wb') as f:
        f.write(response.content)
    
    # Make binary executable on Unix systems
    if system != 'Windows':
        os.chmod(binary_path, 0o755)
    
    # Download Alpine.js
    download_alpine_js(static_folder)
    
    click.echo('TailwindCSS CLI and Alpine.js installed successfully.')


@tailwindcss_cli.command('start')
@with_appcontext
def start_command():
    """Start TailwindCSS in watch mode."""
    static_folder = current_app.static_folder
    binary_path = get_tailwind_binary_path(static_folder)
    
    if not os.path.exists(binary_path):
        click.echo('TailwindCSS CLI not found. Please run "flask tailwindcss install" first.')
        return
    
    cmd = [
        binary_path,
        '-i', os.path.join(static_folder, 'src', 'style.css'),
        '-o', os.path.join(static_folder, 'dist', 'style.css'),
        '--watch'
    ]
    
    click.echo('Starting TailwindCSS in watch mode...')
    
    try:
        subprocess.Popen(cmd)
    
    except Exception as e:
        click.echo(f'Error starting TailwindCSS: {e}')


@tailwindcss_cli.command('build')
@with_appcontext
def build_command():
    """Build TailwindCSS for production."""
    static_folder = current_app.static_folder
    binary_path = get_tailwind_binary_path(static_folder)
    
    if not os.path.exists(binary_path):
        click.echo('TailwindCSS CLI not found. Please run "flask tailwindcss install" first.')
        return
    
    cmd = [
        binary_path,
        '-i', os.path.join(static_folder, 'src', 'style.css'),
        '-o', os.path.join(static_folder, 'dist', 'style.css'),
        '--minify'
    ]
    
    click.echo('Building TailwindCSS for production...')
    subprocess.run(cmd)
    click.echo('Build completed successfully.')
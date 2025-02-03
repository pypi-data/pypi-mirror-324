import os
import platform
import requests
from .constants import NPM_ALPINE_JS_URL


def create_directories(static_folder):
    """Create necessary directories if they don't exist."""
    os.makedirs(os.path.join(static_folder, 'src'), exist_ok=True)
    os.makedirs(os.path.join(static_folder, 'dist'), exist_ok=True)


def get_tailwind_binary_path(static_folder):
    """Get the path to the Tailwind binary."""
    binary_name = 'tailwindcss.exe' if platform.system() == 'Windows' else 'tailwindcss'
    return os.path.join(static_folder, binary_name)


def download_alpine_js(static_folder):
    """Download the latest version of Alpine.js."""
    response = requests.get(NPM_ALPINE_JS_URL)
    latest_version = response.json()['dist-tags']['latest']
    alpine_js_url = f'https://unpkg.com/alpinejs@{latest_version}/dist/cdn.min.js'
    
    alpine_js_path = os.path.join(static_folder, 'dist', 'alpine.js')
    response = requests.get(alpine_js_url)

    with open(alpine_js_path, 'wb') as f:
        f.write(response.content)
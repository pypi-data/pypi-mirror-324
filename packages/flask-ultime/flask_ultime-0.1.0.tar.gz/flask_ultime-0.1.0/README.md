# Flask Ultime

Flask Ultime is a Flask extension that integrates TailwindCSS and Alpine.js to simplify the development of your web applications.

## Installation

You can install Flask Ultime via pip:

```sh
pip install flask-ultime
```

Or, if you are developing locally, you can install it with:

```sh
pip install .
```

## Usage

To use Flask Ultime in your Flask application, you need to initialize it with your Flask app:

```python
from flask import Flask
from flask_ultime import FlaskUltime

app = Flask(__name__)
ultime = FlaskUltime(app)
```

Then, load the CSS and JS in your template:

```html
<!doctype html>
<html lang="en">
<head>
    {{ ultime_css() }}
</head>
<body>
    {{ ultime_js() }}
</body>
</html>
```

Finally, set the `FLASK_APP` environment variable and you will have access to the CLI commands: `flask ultime init`, `flask ultime install`, `flask ultime start`, and `flask ultime build`.

```sh
export FLASK_APP=your_application.py
```

Run the following commands:

```sh
flask ultime init
```

```sh
flask ultime install
```

```sh
flask ultime start
```

```sh
flask ultime build
```

## Features

- **TailwindCSS Integration**: Easily include TailwindCSS in your Flask templates.
- **Alpine.js Integration**: Use Alpine.js for reactive components in your Flask app.
- **Simple Setup**: Quick and easy setup to get started with modern web development tools.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Support

If you have any questions or need help, feel free to open an issue on the GitHub repository.

## Acknowledgements

Special thanks to the Flask, TailwindCSS, and Alpine.js communities for their amazing work.
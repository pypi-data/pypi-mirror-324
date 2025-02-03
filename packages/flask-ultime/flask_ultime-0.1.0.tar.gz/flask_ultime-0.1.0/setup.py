from setuptools import setup, find_packages

setup(
    name='flask_ultime',
    version='0.1.0',
    description='A Flask extension to integrate TailwindCSS and Alpine.js.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='codewithmpia',
    author_email='codewithmpia@gmail.com',
    url='https://github.com/codewithmpia/flask_ultime',
    packages=find_packages(),
    install_requires=[
        "Flask",
        "requests",
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Flask',
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
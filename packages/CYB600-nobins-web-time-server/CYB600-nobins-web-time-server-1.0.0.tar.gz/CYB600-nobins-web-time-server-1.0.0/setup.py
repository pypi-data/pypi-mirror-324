# setup.py
from setuptools import setup, find_packages

setup(
    name='CYB600-nobins-web-time-server',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['flask'],
    entry_points={
        'console_scripts': [
            'web-time-server=web_time_server.server:run_server',
        ],
    },
)


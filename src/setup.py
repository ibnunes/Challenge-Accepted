from distutils.core import setup, find_packages
from importlib.metadata import entry_points

setup(
    name='Challenge Accepted',
    description='System to Publish Cryptographic Challenges',
    long_description='Encryption contains excellent tools for developing challenging mystery games. \
The idea of this work is to develop a system that allows different users to publish and solve challenges.',
    version='1.0.0',
    author='C-Team',
    install_requires=[
        'prettytable',
        'Padding',
        'pycryptodome',
        'requests',
        'validate_email'
    ],
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'challenge-accepted-client = .app:main'
        ]
    }
)

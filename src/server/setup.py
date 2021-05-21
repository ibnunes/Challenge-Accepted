from distutils.core import setup, find_packages

setup(
    name='Challenge Accepted',
    description='System to Publish Cryptographic Challenges',
    long_description='Encryption contains excellent tools for developing challenging mystery games. \
The idea of this work is to develop a system that allows different users to publish and solve challenges.',
    version='1.0.0',
    author='C-Team',
    install_requires=[
        'Padding',
        'prettytable',
        'pycryptodome',
        'requests',
        'validate_email'
    ],
    packages=find_packages(),
)

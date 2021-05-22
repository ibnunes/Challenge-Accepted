from distutils.core import setup, find_packages

setup(
    name='Challenge Accepted CLI',
    description='System to Publish Cryptographic Challenges',
    long_description='Encryption contains excellent tools for developing challenging mystery games. \
The idea of this work is to develop a system that allows different users to publish and solve challenges.',
    version='1.1.0-beta',
    author='C-Team',
    license='GNU-GPL 3.0',
    install_requires=[
        'Padding',
        'prettytable',
        'pycryptodome',
        'requests',
        'validate_email',
        'sympy',
        'pycaesarcipher',
        'onetimepad',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'challenge-accepted-client = .app:main'
        ]
    }
)

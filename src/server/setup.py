from distutils.core import setup, find_packages

setup(
    name='Challenge Accepted Server',
    description='System to Publish Cryptographic Challenges',
    long_description='Encryption contains excellent tools for developing challenging mystery games. \
The idea of this work is to develop a system that allows different users to publish and solve challenges.',
    version='1.0.0-beta',
    author='C-Team',
    license='GNU-GPL 3.0',
    install_requires=[
        'flask',
        'mariadb'
    ],
    packages=find_packages()
)

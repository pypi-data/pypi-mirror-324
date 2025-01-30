from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.1'
DESCRIPTION = 'Cifrado César con añadidos de fantasia, permite encriptar y desencriptar mensajes'

# Setting up
setup(
    name="Magical_Cipher_Disk",
    version=VERSION,
    author="John Frederick Knight Berra / FrederickKnight",
    author_email="<infisefir@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/FrederickKnight/Magical_Cipher_Disk',
    license='MIT',
    packages=find_packages(),
    keywords=['python', 'cipher','encrypted','disk','magic','D&D'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=["Unidecode >= 1.3.8"],
    python_requires=">=3.12"
)
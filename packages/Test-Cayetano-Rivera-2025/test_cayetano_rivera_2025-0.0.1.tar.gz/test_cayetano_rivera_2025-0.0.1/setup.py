from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Test_Cayetano_Rivera_2025",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Cayetano Rivera",
    description="Una biblioteca para consultar cursos de hack4u.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/",
)


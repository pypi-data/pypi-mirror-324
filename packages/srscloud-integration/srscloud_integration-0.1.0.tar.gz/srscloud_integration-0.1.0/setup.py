from setuptools import setup, find_packages

setup(
    name="srscloud-integration",
    version="0.1.0",
    author="Automate Brasil",
    author_email="cx@automate.com",
    description="Integração com SRSCloud para automação de processos",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://www.automate.com.br/",
    packages=find_packages(),
    install_requires=[
        "requests",
        "urllib3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

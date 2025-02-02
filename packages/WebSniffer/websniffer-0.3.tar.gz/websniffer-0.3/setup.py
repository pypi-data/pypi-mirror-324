from setuptools import setup, find_packages

setup(
    name="WebSniffer",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "aiohttp"
    ],
    description="Пакет для парсинга веб-страниц",
    author="Shadow7x",
    author_email="loginvlad1000@gmail.com",
    url="https://github.com/Shadow7x/webscrapper",
)
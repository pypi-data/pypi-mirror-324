import setuptools
from pcdt_scraper import __version__

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name="pcdt-scraper",
    version=__version__,
    author="Jak Bin",
    description="A PyChromeDevTools based WebScraper and selenium like syntax.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jakbin/pcdt-scraper",
    project_urls={
        "Bug Tracker": "https://github.com/jakbin/pcdt-scraper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='webscraper,scraper,web-scraper,pcdt-scraper',
    python_requires=">=3.6",
    install_requires=['bs4', 'PyChromeDevTools'],
    packages=["pcdt_scraper"]
)

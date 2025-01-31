from setuptools import setup, find_packages

setup(
    name="ScrapingData",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "pytz",
        "numpy",
        "pandas",
        "google-analytics-data",
    ],
    author="Mariem Romdhane",
    author_email="romdhanemariem21@gmail.com",
    description="Un package pour le scraping de données de réseaux sociaux.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mariemromdhane21/ScrapingData",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

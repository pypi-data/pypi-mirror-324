from setuptools import setup, find_packages

setup(
    name="nuri-cms",
    version="0.1.0",
    description="A lightweight API-first CMS.",
    author="Jan Markus Langer",
    author_email="janmarkuslanger10121994@gmail.com",
    url="https://github.com/nuri-cms/nuri", 
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-login",
    ],
    entry_points={
        "console_scripts": [
            "nuri = nuri.cli:cli",  # Falls du eine CLI nutzt
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

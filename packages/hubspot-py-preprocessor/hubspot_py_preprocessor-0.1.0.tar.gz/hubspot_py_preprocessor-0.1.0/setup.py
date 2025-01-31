from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hubspot-py-preprocessor",  # Nom du package
    version="0.1.0",  # Version du package
    author="David BRAHIM",  # Votre nom
    author_email="dav.brahim@gmail.com",  # Votre email
    description="A Python tool to extract and organize custom code for HubSpot customcode workflows.",  # Description courte
    long_description=long_description,  # Description longue (README.md)
    long_description_content_type="text/markdown",  # Type de la description longue
    url="https://gitlab.com/dbm-01/hubspot-py-preprocessor",  # URL du projet
    packages=find_packages(where="src"),  # Trouve les packages dans le dossier `src`
    package_dir={"": "hubspot-py-preprocessor"},  # Indique que les packages sont dans `src`
    include_package_data=True,  # Inclut les fichiers non-Python spécifiés dans MANIFEST.in
    install_requires=[  # Dépendances du projet
        "requests>=2.32.3,<3.0.0",
    ],
    classifiers=[  # Métadonnées pour PyPI
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # Version de Python requise
    #entry_points={  # Points d'entrée pour les scripts CLI
    #    "console_scripts": [
    #        "hubspot-code-processor=hubspot_code_processor.cli:main",  # Exemple de point d'entrée
    #    ],
    #},
)
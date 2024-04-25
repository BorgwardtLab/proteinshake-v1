from setuptools import find_packages, setup

__version__ = "1.0.0"
URL = "https://proteinshake.readthedocs.io/en/latest/index.html"

install_requires = [
    "biopandas>=0.4.1",
    "pandas>=1.4.3",
    "rdkit>=2022.3.3",
    "tqdm>=4.64.0",
    "scikit-learn>=1.1.1",
    "joblib>=1.2.0",
    "requests>=2.27.1",
    "fastavro>=1.6.1",
    "freesasa>=2.2.0.post3",
    "goatools>=1.3.1",
]
test_requires = [
    "pytest",
]

setup(
    name="proteinshake",
    version=__version__,
    description="Protein structure datasets for machine learning.",
    author="Tim Kucera, Carlos Oliver, Dexiong Chen, Karsten Borgwardt",
    author_email="kucera@biochem.mpg.de",
    url=URL,
    keywords=[
        "bioinformatics",
        "deep-learning",
        "computational-biology",
        "macromolecular-structure",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
)

from setuptools import setup, find_packages

setup(
    name="barsukov",
    use_scm_version=True,
    setup_requires=["setuptools", "setuptools_scm"],

    install_requires=[
        "pytz>=2014.10",
        "numpy>1.0.0",
        "scipy>=0.9.0",
    ],

    pythhon_requires=">=3.6",
    description="Experiment Automation Package",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    url="https://barsukov.ucr.edu",

    authors=[
        {"name": "Igor Barsukov", "email": "igorb@ucr.edu"},
        {"name": "Steven Castaneda", "email": "scast206@ucr.edu}"},
    ],

    packages=find_packages(where="src"),
    package_dir={"": "src"},
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="GridSearchHelper",
    version="0.6.0",
    author="Abdulla Alimov",
    author_email="abdullaalimov555@gmail.com",
    description="Advanced hyperparameter tuning using grid search for ML models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alimovabdulla/GridSearchHelper",
    project_urls={
        "Bug Tracker": "https://github.com/alimovabdulla/GridSearchHelper/",
        "Documentation": "https://github.com/alimovabdulla/GridSearchHelper/",
    },
    packages=find_packages(include=["GridSearchHelper", "GridSearchHelper.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.6",
    install_requires=[
        "scikit-learn>=0.24.0",
        "numpy>=1.19.0",
    ],
    keywords="machine-learning grid-search hyperparameter-tuning scikit-learn",
    license="MIT",
    include_package_data=True,
    zip_safe=False,
)

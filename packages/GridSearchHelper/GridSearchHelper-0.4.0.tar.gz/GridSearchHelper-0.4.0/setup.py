from setuptools import setup, find_packages

setup(
    name="GridSearchHelper",  # Kitabxananın adı
    version="0.4.0",  # Kitabxananın versiyası
    description="A library for hyperparameter tuning using grid search for machine learning models.",
    long_description=open(
        "README.md"
    ).read(),  # Kitabxananın geniş təsviri README.md faylından alınacaq
    long_description_content_type="text/markdown",  # README faylının formatı
    author="Abdulla Alimov",  # Müəllifin adı
    author_email="abdullaalimov555@gmail.com",  # Müəllifin e-maili
    url="https://github.com/username/ModelTuner",  # GitHub repo linki
    packages=find_packages(),  # Bütün paketləri tapır
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python versiyası
    install_requires=[  # Kitabxananın asılılıqları
        "scikit-learn>=0.24.0",
        "numpy>=1.19.0",
    ],
    include_package_data=True,  # Əlavə faylları da daxil etmək
    zip_safe=False,  # Kitabxananın sıxılmasının qarşısını alır
)

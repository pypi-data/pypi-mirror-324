
from setuptools import setup, find_packages

setup(
    name='bukmacherska_lib',
    version='1.4.0',
    description='Biblioteka do analizy wyników piłkarskich z wykorzystaniem statystyki i machine learningu',
    author='Twoje Imię',
    author_email='twoj.email@example.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'matplotlib',
        'pandas',
        'xgboost',
        'tensorflow',  # Dodaj inne zależności, które są wymagane
        'seaborn',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

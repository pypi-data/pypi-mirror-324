from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='bukmacherska_lib',
    version='1.5.0',
    description='Biblioteka do analizy wyników piłkarskich z wykorzystaniem statystyki i machine learningu',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Twoje Imię',
    author_email='twoj.email@example.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'matplotlib',
        'pandas',
        'xgboost',
        'tensorflow',
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

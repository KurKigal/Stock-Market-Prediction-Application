from setuptools import setup, find_packages

setup(
    name="stock_predictor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'pandas',
        'numpy',
        'scikit-learn',
        'tensorflow',
        'requests',
        'beautifulsoup4',
        'schedule',
        'joblib',
        'yfinance'
    ],
)
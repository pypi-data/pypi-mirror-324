from setuptools import setup, find_packages

setup(
    name='pinetopy',
    version='0.0.4',
    packages=find_packages(),
    install_requires=[
        'numpy', 
        'pandas',
        'ta',
        'pytz'
    ],
)

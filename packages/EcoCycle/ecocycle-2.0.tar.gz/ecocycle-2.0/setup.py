import os
os.system("pip install setuptools wheel")
from setuptools import setup, find_packages

setup(
    name="EcoCycle",  # Your package name
    version="2.0",  # Version number
    packages=find_packages(),
    install_requires=[
        'requests',
        'ipython',
        'colorama',
        'python-dotenv',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'weatherapi',  
    ],
    entry_points={
        'console_scripts': [
            'ecocycle=ecocycle:main',  # If you have a main function in ecocycle.py
        ],
    },
    long_description=open('README.md').read(),  # Include README
    long_description_content_type='text/markdown',
    author="Shirish Pothi",
    author_email="shirish.pothi.27@gmail.com",
    description="Cycle into a greener tomorrow.",
    license="Apache 2.0",
)

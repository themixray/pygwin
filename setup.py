from setuptools import setup
import requests

setup(name='pygwin',packages=['pygwin'],version='0.1.0',author='themixray',
    description='A library for creating Python applications.',license='MIT',
    install_requires=['cython','pywin32','pygame','inputs','pydub','kivy'])

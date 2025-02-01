from setuptools import setup, find_packages

setup(
    name='funktgtools',
    version='0.1.16', # Includes last message correction on /wallet
    description='Modular TG Features',
    url='https://github.com/funkaclau',
    author='funkaclau',
    packages=find_packages(),
    install_requires=[
        "aiogram==3.2.0"
    ],
)

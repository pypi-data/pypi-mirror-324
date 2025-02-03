from setuptools import setup, find_packages

setup(
    name='data3_network_variables',
    version='0.0.9',
    packages=find_packages(),
    install_requires=[
        "redis==5.0.8",
        "requests==2.32.3"
    ],
    author='Data3 Network',
    author_email='data3network@gmail.com',
    description='Data3 Network Library for variable access',
)



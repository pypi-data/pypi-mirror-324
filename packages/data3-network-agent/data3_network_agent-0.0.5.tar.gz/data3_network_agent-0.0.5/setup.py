from setuptools import setup, find_packages

setup(
    name='data3_network_agent',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        "requests==2.32.3"
    ],
    author='Data3 Network',
    author_email='data3network@gmail.com',
    description='Data3 Network Library for agent env access',
)



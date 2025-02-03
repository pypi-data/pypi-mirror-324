from setuptools import setup,find_packages

setup( 
    name='goku-STT',
    version='0.1',
    author='Aman gaud',
    author_email='amangaud448@gmail.com',
    description='this is speech to text package created by aman gaud'
)

packages = find_packages(),
install_requirments = [
    'selenium',
    'webdriver_manager'
]

from setuptools import setup

setup(
    name='nick-stt',
    version='0.1',
    author='Nikhil Patidar ',
    author_email='nikhilpatidar004@gmail.com',
    description='this is speech to text package created by Nikhil Patidar'
)
packages= find_packages(),
install_requirements = [
    'selenium',
    'webdriver_manager',

]
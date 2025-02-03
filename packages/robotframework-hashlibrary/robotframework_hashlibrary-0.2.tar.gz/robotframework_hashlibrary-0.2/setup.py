from setuptools import setup, find_packages

setup(
    name='robotframework-hashlibrary',
    version='0.2',
    description='Robot Framework library that generates hashes based on the given input',
    author='David Italiander',
    author_email='david.italiander@gmail.com',
    packages=find_packages(),
    install_requires=[
        'robotframework',
        'pytest',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Robot Framework',
    ],
)
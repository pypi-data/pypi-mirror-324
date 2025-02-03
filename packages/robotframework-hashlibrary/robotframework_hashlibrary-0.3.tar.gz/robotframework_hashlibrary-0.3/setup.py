from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='robotframework-hashlibrary',
    version='0.3',
    description='Robot Framework library that generates hashes based on the given input',
    author='David Italiander',
    author_email='david.italiander@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'robotframework',
        'pytest',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Robot Framework',
    ],
)
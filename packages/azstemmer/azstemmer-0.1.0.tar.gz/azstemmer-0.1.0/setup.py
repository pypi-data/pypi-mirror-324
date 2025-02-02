from setuptools import setup, find_packages
setup(
    name="azstemmer",
    version="0.1.0",
    description="A stemming library for the Azerbaijani language",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Nagi Nagiyev",
    author_email="naginagiyev03@gmail.com",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    package_data={
        'azstemmer': ['azwords.txt', 'enwords.txt'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
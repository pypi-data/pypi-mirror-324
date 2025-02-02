from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Basic Greet Package'

# Setting up
setup(
    name="greetmeee",
    version=VERSION,
    author="Haseeb",
    author_email="haseebasif5@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'greet', 'greetmeee', 'greetmeee package'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
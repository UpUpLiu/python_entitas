from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="python_entitas",
    version="0.0.1",
    author="hangangliu",
    keywords=("entitas"),
    license="MIT Licence",
    author_email="hangangliurd@gmail.com",
    description="A small example package",
    long_description=long_description,
    url="https://github.com/UpUpLiu/python_entitas",
    packages= find_packages(),
    include_package_data = True,
    platforms = "any",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires = [
        'Mako >= 1.0.7',
        'lupa >= 1.8'
    ]
)
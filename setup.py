from setuptools import setup, find_packages

if __name__ == "__main__":
    with open("README.md", "r") as fh:
        long_description = fh.read()
    setup(
        name="python_entitas",
        version="0.0.10",
        author="hangangliu",
        keywords=("entitas"),
        license="MIT Licence",
        author_email="hangangliurd@gmail.com",
        description="A small example package",
        long_description=long_description,
        url="https://github.com/UpUpLiu/python_entitas",
        packages=find_packages('python_entitas'),
        package_dir={'': 'python_entitas'},
        include_package_data=True,
        platforms="any",
        classifiers=[
            "Programming Language :: Python :: 3",
        ],
        install_requires=[
            'Mako >= 1.0.7',
            'lupa >= 1.8'
        ]
    )



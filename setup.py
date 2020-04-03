from setuptools import setup, find_packages

if __name__ == "__main__":
    with open("README.md", "r", encoding='UTF-8') as fh:
        long_description = fh.read()
    setup(
        name="python_entitas",
        version="0.0.13",
        author="hangangliu",
        keywords=("entitas"),
        license="MIT Licence",
        author_email="hangangliurd@gmail.com",
        description="A small example package",
        long_description=long_description,
        url="https://github.com/UpUpLiu/python_entitas",
        packages=find_packages('src'),
        package_dir={'': 'src'},
        data_files=[('mako',
                     ['src/mako/ecs_autoinc.mako', 'src/mako/ecs_context.mako',
                      'src/mako/ecs_entity.mako', 'src/mako/ecs_make_component.mako',
                      'src/mako/ecs_service.mako', 'src/mako/ecs_service_inc.mako'])],
        include_package_data=True,
        zip_safe = False,
        platforms="any",
        classifiers=[
            "Programming Language :: Python :: 3",
        ],
        install_requires=[
            'Mako >= 1.0.7',
            'lupa >= 1.8'
        ]
    )



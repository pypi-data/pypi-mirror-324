from setuptools import setup, find_packages

setup(
    name="pokemon-world",
    version="2025.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.0",
    ],
    entry_points={
        'console_scripts': [
            'pokemon-world=pokemon_world.app:main',
        ],
    },
)
from setuptools import setup, find_packages

setup(
    name="wave_front_h2ogpte",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        "h2ogpte>=1.6.18",
    ],
)

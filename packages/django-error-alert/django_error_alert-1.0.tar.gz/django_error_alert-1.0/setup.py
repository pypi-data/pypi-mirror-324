from setuptools import setup, find_packages

from setuptools import setup, find_packages

setup(
    name="django-error-alert",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Django"],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)

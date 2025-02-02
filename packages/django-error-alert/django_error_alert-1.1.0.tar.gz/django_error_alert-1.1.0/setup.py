from setuptools import setup, find_packages

setup(
    name="django-error-alert",  # Unique package name
    version="1.1.0",  # Update with each release
    author="Rahul Soni",
    author_email="your.email@example.com",
    description="A Django package for real-time error alerting",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rahulsonikadel/django-error-alert",
    packages=find_packages(),
    install_requires=[
        "Django>=3.0",  # Add dependencies
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

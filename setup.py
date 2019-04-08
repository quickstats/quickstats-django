from setuptools import find_packages, setup

setup(
    name="django-simplestats",
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    license="MIT License",
    description="A simple stats package",
    url="https://github.com/kfdm/django-simplestats",
    author="Paul Traylor",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP",
    ],
    install_requires=[
        "Django>=2.0",
        "djangorestframework",
        "python-dateutil",
        "pytz",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "simplestats = simplestats.standalone.manage:main"
        ]
    },
)

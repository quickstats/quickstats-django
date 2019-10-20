from setuptools import find_packages, setup

setup(
    name="quickstats-django",
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    license="MIT License",
    description="A simple stats package",
    url="https://github.com/quickstats/quickstats-django",
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
        "icalendar",
        "python-dateutil",
        "celery",
        "django-environ",
        "Django>=2.0",
        "djangorestframework-csv",
        "djangorestframework",
        "drf-nested-routers",
        "python-dateutil",
        "pytz",
        "requests",
    ],
    entry_points={
        "console_scripts": ["quickstats = quickstats.standalone.manage:main"],
        "quickstats.scrape": [
            "calendar = quickstats.scrape.calendar:CalendarScraper",
            "atom = quickstats.scrape.atom:AtomScraper",
        ],
    },
)

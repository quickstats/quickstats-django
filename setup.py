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
        "celery",
        "Django>=2.0",
        "djangorestframework-csv",
        "djangorestframework",
        "drf-nested-routers",
        "icalendar",
        "pillow>=6.2.0",
        "python-dateutil",
        "pytz",
        "requests",
    ],
    extras_require={
        "standalone": [
            "celery==4.3.0",
            "django-environ",
            "prometheus-client",
            "sentry_sdk",
        ],
        "dev": [
            "black",
            "django_nose",
            "psycopg2-binary",
            "unittest-xml-reporting",
        ],
    },
    entry_points={
        "console_scripts": ["quickstats = quickstats.standalone.manage:main"],
        "quickstats.scrape": [
            "calendar = quickstats.scrape.calendar:CalendarScraper",
            "atom = quickstats.scrape.atom:AtomScraper",
        ],
    },
)

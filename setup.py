from setuptools import find_packages, setup
from simplestats import __version__

setup(
    name='django-simplestats',
    version=__version__,
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    license='MIT License',
    description='A simple stats package',
    url='https://github.com/kfdm/django-simplestats',
    author='Paul Traylor',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'djangorestframework',
        'djangorestframework-word-filter',
        'icalendar',
        'pytz',
        'requests',
    ],
    entry_points={
        'powerplug.apps': ['stats = simplestats'],
        'simplestats.hourly': ['wanikani = simplestats.plugins.wanikani:WaniKani'],
        'simplestats.signals': ['location = simplestats.signals.location'],
    },
)

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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'django-filter',
        'Django',
        'djangorestframework-word-filter',
        'djangorestframework',
        'icalendar',
        'Pillow',
        'python-dateutil',
        'pytz',
        'requests',
    ],
    extras_require={
        'standalone': [
            'dj_database_url',
            'envdir',
            'social-auth-app-django',
        ]
    },
    entry_points={
        'console_scripts': [
            'simplestats = simplestats.standalone.manage:main[standalone]',
        ],
        'powerplug.apps': ['stats = simplestats'],
        'powerplug.urls': ['stats = simplestats.urls'],
        'powerplug.rest': [
            'chart = simplestats.rest:ChartViewSet',
            'countdown = simplestats.rest:CountdownViewSet',
            'location = simplestats.rest:LocationViewSet',
            'report = simplestats.rest:ReportViewSet',
        ],
        'powerplug.task': [
            'chart = simplestats.tasks.chart',
            'countdown = simplestats.tasks.countdown',
            'reports = simplestats.tasks.reports',
            'utility = simplestats.tasks.utility',
        ]
    },
)

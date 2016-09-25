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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'Django',
        'django-filter',
        'djangorestframework-word-filter',
        'djangorestframework',
        'icalendar',
        'Pillow',
        'pytz',
        'requests',
    ],
    extras_require={
        'standalone': [
            'envdir',
            'dj_database_url',
            'python-social-auth',
        ]
    },
    entry_points={
        'console_scripts': [
            'simplestats = simplestats.standalone.manage:main[standalone]',
        ],
        'powerplug.apps': ['stats = simplestats'],
        'powerplug.subnav': ['stats = simplestats.urls:subnav'],
        'powerplug.urls': ['stats = simplestats.urls'],
        'powerplug.rest': [
            'chart = simplestats.rest:ChartViewSet',
            'countdown = simplestats.rest:CountdownViewSet',
            'stat = simplestats.rest:StatViewSet',
        ],
    },
)

import imp
from os import path

from setuptools import find_packages, setup


VERSION = imp.load_source('version', path.join('.', 'osreporter', 'version.py'))
VERSION = VERSION.__version__

REQUIRES = [
    'openpyxl==2.4.5',
    'requests==2.12.5',
    'requests-futures==0.9.7',
    'rethinkdb==2.3.0.post6',
    'ruamel.yaml==0.13.10'
]

setup(
    name='osreporter',
    version=VERSION,
    description='Reporting tool for private OpenStack Clouds',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='openstack reporting rethinkdb elasticcloud http cloud',
    author='Paul Stevens',
    author_email='ps@xnode.co.za',
    url='https://xnode.co.za/',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRES,
    setup_requires=[],
    entry_points={
        'console_scripts': [
            'osreporter = osreporter.cmd.osreporter:main',
        ]
    }
)

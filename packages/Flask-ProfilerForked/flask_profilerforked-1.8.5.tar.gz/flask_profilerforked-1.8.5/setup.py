"""
Flask-ProfilerForked
-------------

Flask Profiler Forked

Links
* `development version <http://github.com/Kalmai221/flask-profiler/>`
"""

import sys
from setuptools import setup

install_requires = [
    'Flask',
    'Flask-Login',
    'simplejson'
]

setup(
    name='Flask-ProfilerForked',
    version='1.8.5',
    url='https://github.com/Kalmai221/FlaskProfilerForked',
    license=open('LICENSE').read(),
    author='Kalmai221',
    author_email='Kalmai221PlaysOfficial@gmail.com',
    description='API endpoint profiler for Flask framework',
    keywords=[
        'profiler', 'flask', 'performance', 'optimization'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', 
    packages=['flask_profiler'],
    package_data={
        'flask_profiler': [
            'storage/*',
            'static/dist/fonts/*',
            'static/dist/css/*',
            'static/dist/js/*',
            'static/dist/images/*',
            'static/dist/*',
            'static/dist/index.html',
        ]
    },
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

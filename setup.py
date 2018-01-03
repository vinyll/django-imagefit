# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='django-imagefit',
    version='0.6',
    description='Render an optimized version of your original image on display. Ability to resize and crop.',
    long_description=open('README.md').read(),
    author='Vincent Agnano',
    author_email='vincent.agnano@scopyleft.fr',
    url='http://github.com/vinyll/django-imagefit',
    license='BSD',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['django-appconf'],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ]
)

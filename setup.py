#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="effreq",
    version="0.1a1",
    description="Purely functional HTTP client, using the Effect library",
    long_description=open('README.rst').read(),
    url="http://github.com/radix/effreq/",
    author="Christopher Armstrong",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        ],
    packages=['effreq'],
    install_requires=['effect'],
    )

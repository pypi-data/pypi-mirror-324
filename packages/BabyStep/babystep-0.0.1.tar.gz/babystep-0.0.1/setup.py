#!/usr/bin/env python

import os
from setuptools import setup

VERSION = "0.0.1"

with open('README.md') as f:
    LONG_DESCR = f.read()

setup(
    name='BabyStep',
    version=VERSION,
    description='All Basic sorting and search',
    long_description=LONG_DESCR,
    long_description_content_type='text/markdown',
    author='Muthukumaran',
    author_email='titansmuthu@gmail.com',
    url='https://github.com/titans2024/baby.git',
    download_url='https://github.com/titans2024/baby/archive/refs/heads/main.zip',
    py_modules=['list', 'search'],  # Explicitly mention your top-level modules here
    license='MIT License',  # Correct field for the license
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
    ],
    keywords='baby sorting and search',
    entry_points={
        'console_scripts': ['mandoline=mandoline:main'],
    },
    install_requires=[
        'setuptools',
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
    include_package_data=True,
)

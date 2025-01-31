# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='kaizen-deploy',
    version='1.2.4',
    license='MIT',
    description="kaizen-deploy is a Configuration Management tool used for installing Heimdall.",
    maintainer="Arjun Babu",
    maintainer_email='arbnair97@gmail.com',
    author="Arjun Babu",
    author_email='arbnair97@gmail.com',
    include_package_data=True,
    packages=['src', 'templates'],
    package_dir={'src': 'src', 'templates': 'src/templates'},
    package_data={'src': ['src/main.py'], 'templates': ['src/templates/manifest.yaml']},
    data_files=[
        ('Lib/kaizen-deploy', ['src/main.py']),
        ('Lib/kaizen-deploy/templates', ['src/templates/manifest.yaml'])
    ],
    keywords='kaizen-deploy',
    install_requires=[
        'pyyaml',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable'
    ],
    entry_points={
        'console_scripts': [
            'kaizen-deploy=src.main:main',
        ],
    },
    python_requires='>=3.6'
)
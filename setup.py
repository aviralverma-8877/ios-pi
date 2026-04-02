#!/usr/bin/env python3
"""
Setup script for Pi iOS Launcher
"""

from setuptools import setup, find_packages

setup(
    name='pi-ios-launcher',
    version='1.0.0',
    description='iOS-like interface for Raspberry Pi with 4.3" display',
    author='Pi iOS Team',
    author_email='info@pi-ios.local',
    py_modules=['pi_ios_launcher'],
    install_requires=[
        'PyQt5>=5.15.0',
    ],
    entry_points={
        'console_scripts': [
            'pi-ios-launcher=pi_ios_launcher:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

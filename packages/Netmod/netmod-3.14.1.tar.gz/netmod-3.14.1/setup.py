from setuptools import setup, find_packages
setup(
name='Netmod',
version='3.14.1',
author='Kaytun Watson',
author_email='kaytunlw2021@hotmail.com',
description='NetMod, A network moderation package created to build territorial command across the internet locally.',
packages=find_packages(),
install_requires=[
    'argparse',
    'scapy',
    'socket',
    'os',
    'webbrowser'
],
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.14',
)
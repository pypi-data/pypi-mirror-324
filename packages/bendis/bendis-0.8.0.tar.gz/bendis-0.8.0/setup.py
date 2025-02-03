# setup.py

from setuptools import setup, find_packages

setup(
    name='bendis',
    version='0.8.0',
    packages=find_packages(),
    install_requires=[
        'gym',
        'pybullet',
        'numpy',
        'opencv-python'
    ],
    description='A custom robotic arm environment for reinforcement learning.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://your-repository-link.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

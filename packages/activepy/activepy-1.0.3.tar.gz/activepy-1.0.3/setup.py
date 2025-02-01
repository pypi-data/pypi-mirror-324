from setuptools import setup, find_packages

setup(
    name='activepy',
    version='1.0.3',  # Update version as needed
    author='Simone',
    author_email='cardellasimone10@gmail.com',
    description='A command-line utility for creating and managing Python webapp applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Automatically find packages in the project
    install_requires=[
        'colorama',  # List of required packages
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Define the Python version required
    entry_points={
        'console_scripts': [
            'actpy=activepy.cli:main',  # Entry point for the command-line interface
        ],
    },
)
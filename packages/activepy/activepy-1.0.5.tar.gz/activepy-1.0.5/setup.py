from setuptools import setup, find_packages

setup(
    name='activepy',
    version='1.0.5',  # Ensure this is incremented for each release
    author='Simone',
    author_email='cardellasimone10@gmail.com',
    description='A command-line utility for creating and managing Python webapp applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        'activepy': ['templates/*', 'templates/models/*', 'templates/settings/*'],  # Include templates
    },
    install_requires=[
        'colorama',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'actpy=activepy.cli:main',
        ],
    },
)
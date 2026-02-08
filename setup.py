from setuptools import setup, find_packages

setup(
    name='socratic-stress-test',
    version='0.1.0',
    author='Silvestro26',
    author_email='your.email@example.com',
    description='A package for Socratic stress testing',
    packages=find_packages(),
    install_requires=[
        # Add package dependencies here
        'requests',
        'numpy',
        'pandas',
        # etc.
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
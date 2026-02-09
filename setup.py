from setuptools import setup, find_packages

setup(
    name='socratic-stress-test',
    version='0.1.0',
    author='Silvestro26',
    author_email='your.email@example.com',
    description='A framework for auditing epistemic reliability through Socratic methodology',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Silvestro26/socratic-stress-test',
    packages=find_packages(),
    install_requires=[
        # No runtime dependencies required
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
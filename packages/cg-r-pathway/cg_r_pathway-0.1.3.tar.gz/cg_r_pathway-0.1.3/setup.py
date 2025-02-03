from setuptools import setup, find_packages

# Read the README file with UTF-8 encoding
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cg-r-pathway',  # Changed to hyphenated name for PyPI compatibility
    version='0.1.3',      # Updated version to match __version__ in your code
    author='Bernard Kwadwo Essuman',
    author_email='simura.pathway@gmail.com',
    description='A comprehensive protein reaction coordinate optimization framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/simura-works/cg_r_pathway',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'torch',
        'numba',
    ],
    entry_points={
        'console_scripts': [
            'cg-r-pathway = cg_r_pathway.cli:main',  # Adjusted to match the new name format
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',  # Reflecting the custom SIMURA License
        'Operating System :: OS Independent',
    ],
    license='SIMURA License',  # Custom license name
    python_requires='>=3.6',
)

from setuptools import setup, find_packages

# Dynamically load the version
version = {}
with open("src/cg_r_pathway/version.py") as f:
    exec(f.read(), version)

# Read the README for long description
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cg-r-pathway',
    version=version['__version__'],
    author='Bernard Kwadwo Essuman',
    author_email='simura.pathway@gmail.com',
    description='A comprehensive protein reaction coordinate optimization framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/simura-works/cg_r_pathway',
    package_dir={'': 'src'},  # Tells setuptools to look inside 'src'
    packages=find_packages(where='src'),  # Finds all packages inside 'src'
    include_package_data=True,
    install_requires=[
        'numpy',
        'matplotlib',
        'torch',
        'numba',
    ],
    entry_points={
        'console_scripts': [
            'cg-r-pathway = cg_r_pathway.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
